//! Öffentliche Brain-Credential über den bestehenden lokalen Infisical-Transport.
//! Bootstrap-Credential und ausgewähltes Secret gelangen nicht in die Prozessumgebung.
use crate::AdapterError;
use nix::fcntl::{fcntl, FcntlArg, FdFlag};
use serde::Deserialize;
use std::{
    fs::{File, OpenOptions},
    io::Read,
    os::unix::fs::{FileExt, OpenOptionsExt, PermissionsExt},
    path::{Path, PathBuf},
    time::Duration,
};
use zeroize::{Zeroize, Zeroizing};

const MAX_CONFIG_BYTES: u64 = 16 * 1024;
const MAX_CREDENTIAL_BYTES: u64 = 8192;
const MAX_REPLY_BYTES: usize = 2 * 1024 * 1024;

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct BotConfig {
    brain: BrainConfig,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct BrainConfig {
    docs: AdapterConfig,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
pub struct AdapterConfig {
    pub endpoint: String,
    pub timeout_ms: u64,
    pub infisical: InfisicalConfig,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
pub struct InfisicalConfig {
    project_id: String,
    environment: String,
    secret_path: String,
    socket_path: PathBuf,
    credential_file: Option<PathBuf>,
    credential_fd: Option<i32>,
    token_secret: String,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct Reply {
    secret: Entry,
}

#[derive(Deserialize)]
struct Entry {
    #[serde(rename = "secretKey")]
    name: String,
    #[serde(rename = "secretValue")]
    value: Option<String>,
}

impl Drop for Entry {
    fn drop(&mut self) {
        if let Some(value) = &mut self.value {
            value.zeroize();
        }
    }
}

impl AdapterConfig {
    pub fn load(path: &Path) -> Result<Self, AdapterError> {
        let file = OpenOptions::new()
            .read(true)
            .custom_flags(libc::O_NOFOLLOW | libc::O_CLOEXEC)
            .open(path)
            .map_err(|_| AdapterError::Configuration)?;
        let mut bytes = Vec::new();
        file.take(MAX_CONFIG_BYTES + 1)
            .read_to_end(&mut bytes)
            .map_err(|_| AdapterError::Configuration)?;
        if bytes.len() as u64 > MAX_CONFIG_BYTES {
            return Err(AdapterError::Configuration);
        }
        let text = std::str::from_utf8(&bytes).map_err(|_| AdapterError::Configuration)?;
        let config: BotConfig = toml::from_str(text).map_err(|_| AdapterError::Configuration)?;
        let config = config.brain.docs;
        config.validate()?;
        Ok(config)
    }

    fn validate(&self) -> Result<(), AdapterError> {
        let valid_credential_source = match (
            &self.infisical.credential_file,
            self.infisical.credential_fd,
        ) {
            (Some(path), None) => path.is_absolute(),
            (None, Some(fd)) => fd >= 3,
            _ => false,
        };
        if !(100..=30_000).contains(&self.timeout_ms)
            || self.endpoint.len() > 256
            || !self
                .infisical
                .project_id
                .bytes()
                .all(|c| c.is_ascii_hexdigit() || c == b'-')
            || self.infisical.project_id.is_empty()
            || !self
                .infisical
                .environment
                .bytes()
                .all(|c| c.is_ascii_alphanumeric() || c == b'-')
            || self.infisical.environment.is_empty()
            || !self.infisical.secret_path.starts_with('/')
            || self.infisical.secret_path.contains("..")
            || self.infisical.secret_path.len() > 256
            || !valid_credential_source
            || !self.infisical.token_secret.starts_with("BRAIN_SERVE_")
            || !self.infisical.token_secret.ends_with("_TOKEN")
            || self.infisical.token_secret.len() > 96
            || !self
                .infisical
                .token_secret
                .bytes()
                .all(|c| c.is_ascii_uppercase() || c.is_ascii_digit() || c == b'_')
        {
            return Err(AdapterError::Configuration);
        }
        // Der typisierte Client prüft Loopback, Credential und Frist ohne Egress.
        brain_client::AsyncBrainClient::new_local(
            &self.endpoint,
            "validation-only-token",
            Duration::from_millis(self.timeout_ms),
        )
        .map_err(|_| AdapterError::Configuration)?;
        Ok(())
    }

    pub fn timeout(&self) -> Duration {
        Duration::from_millis(self.timeout_ms)
    }

    pub async fn load_token(&self) -> Result<Zeroizing<String>, AdapterError> {
        self.infisical.load_token(0).await
    }
}

impl InfisicalConfig {
    async fn load_token(&self, socket_owner: u32) -> Result<Zeroizing<String>, AdapterError> {
        let bootstrap = match (&self.credential_file, self.credential_fd) {
            (Some(path), None) => read_credential(path)?,
            (None, Some(fd)) => read_credential_fd(fd)?,
            _ => return Err(AdapterError::Configuration),
        };
        let client = uplink_infisical_transport::client_builder(&self.socket_path, socket_owner)
            .map_err(|_| AdapterError::Configuration)?
            .timeout(Duration::from_secs(10))
            .build()
            .map_err(|_| AdapterError::Configuration)?;
        let mut response = client
            .get(format!(
                "{}/api/v4/secrets/{}",
                uplink_infisical_transport::BASE_URL,
                self.token_secret
            ))
            .query(&[
                ("projectId", self.project_id.as_str()),
                ("environment", self.environment.as_str()),
                ("secretPath", self.secret_path.as_str()),
                ("viewSecretValue", "true"),
                ("includeImports", "false"),
                ("expandSecretReferences", "false"),
            ])
            .bearer_auth(bootstrap.as_str())
            .send()
            .await
            .map_err(|_| AdapterError::Configuration)?;
        if !response.status().is_success() {
            return Err(AdapterError::Configuration);
        }
        let mut body = Zeroizing::new(Vec::new());
        while let Some(chunk) = response
            .chunk()
            .await
            .map_err(|_| AdapterError::Configuration)?
        {
            if body.len().saturating_add(chunk.len()) > MAX_REPLY_BYTES {
                return Err(AdapterError::Configuration);
            }
            body.extend_from_slice(&chunk);
        }
        let reply: Reply =
            serde_json::from_slice(&body).map_err(|_| AdapterError::Configuration)?;
        selected_token(reply, &self.token_secret)
    }
}

fn read_credential(path: &Path) -> Result<Zeroizing<String>, AdapterError> {
    let file = OpenOptions::new()
        .read(true)
        .custom_flags(libc::O_NOFOLLOW | libc::O_CLOEXEC)
        .open(path)
        .map_err(|_| AdapterError::Configuration)?;
    read_credential_contents(&file)
}

fn read_credential_fd(fd: i32) -> Result<Zeroizing<String>, AdapterError> {
    if fd < 3 {
        return Err(AdapterError::Configuration);
    }
    // fcntl prüft den vom Starter übergebenen Deskriptor ohne Besitzübernahme.
    let flags = fcntl(fd, FcntlArg::F_GETFD).map_err(|_| AdapterError::Configuration)?;
    fcntl(
        fd,
        FcntlArg::F_SETFD(FdFlag::from_bits_retain(flags) | FdFlag::FD_CLOEXEC),
    )
    .map_err(|_| AdapterError::Configuration)?;
    // Nur die eigene Kopie wird geschlossen; beide Deskriptoren bleiben CLOEXEC.
    let descriptor =
        filedescriptor::FileDescriptor::dup(&fd).map_err(|_| AdapterError::Configuration)?;
    let file = descriptor
        .as_file()
        .map_err(|_| AdapterError::Configuration)?;
    read_credential_contents(&file)
}

fn read_credential_contents(file: &File) -> Result<Zeroizing<String>, AdapterError> {
    let metadata = file.metadata().map_err(|_| AdapterError::Configuration)?;
    if !metadata.is_file() || metadata.permissions().mode() & 0o077 != 0 {
        return Err(AdapterError::Configuration);
    }
    // Positionsunabhängiges Lesen erhält den Offset des geerbten Originals.
    let mut bytes = Zeroizing::new(vec![0; (MAX_CREDENTIAL_BYTES + 1) as usize]);
    let mut length = 0;
    while length < bytes.len() {
        let read = file
            .read_at(&mut bytes[length..], length as u64)
            .map_err(|_| AdapterError::Configuration)?;
        if read == 0 {
            break;
        }
        length += read;
    }
    bytes.truncate(length);
    if length as u64 > MAX_CREDENTIAL_BYTES {
        return Err(AdapterError::Configuration);
    }
    let text = std::str::from_utf8(&bytes).map_err(|_| AdapterError::Configuration)?;
    let text = text.trim_end_matches(['\r', '\n']);
    if text.is_empty() || !text.bytes().all(|c| c.is_ascii_graphic()) {
        return Err(AdapterError::Configuration);
    }
    Ok(Zeroizing::new(text.to_owned()))
}

fn selected_token(reply: Reply, name: &str) -> Result<Zeroizing<String>, AdapterError> {
    let mut entry = reply.secret;
    if entry.name != name {
        return Err(AdapterError::Configuration);
    }
    let value = Zeroizing::new(entry.value.take().ok_or(AdapterError::Configuration)?);
    if value.is_empty() || value.len() > 4096 || !value.bytes().all(|c| c.is_ascii_graphic()) {
        return Err(AdapterError::Configuration);
    }
    Ok(value)
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;
    use std::{
        fs,
        io::{Read, Write},
        os::{
            fd::AsRawFd,
            unix::{fs::MetadataExt, net::UnixListener},
        },
        thread,
    };

    fn config(socket: PathBuf, credential: PathBuf) -> AdapterConfig {
        AdapterConfig {
            endpoint: "http://127.0.0.1:8787".into(),
            timeout_ms: 5000,
            infisical: InfisicalConfig {
                project_id: "00000000-0000-0000-0000-000000000000".into(),
                environment: "prod".into(),
                secret_path: "/".into(),
                socket_path: socket,
                credential_file: Some(credential),
                credential_fd: None,
                token_secret: "BRAIN_SERVE_OTHER_TOKEN".into(),
            },
        }
    }

    #[test]
    fn config_is_explicit_and_cannot_select_external_endpoints_or_arbitrary_secrets() {
        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("bot.toml");
        let mut value = serde_json::to_value(json!({
            "brain":{"docs":{
            "endpoint":"http://127.0.0.1:8787", "timeout_ms":5000,
            "infisical":{
                "project_id":"00000000-0000-0000-0000-000000000000", "environment":"prod",
                "secret_path":"/", "socket_path":"/run/uplink-infisical/api.sock",
                "credential_file":"/run/credentials/docs/infisical-token",
                "token_secret":"BRAIN_SERVE_OTHER_TOKEN"
            }}}
        }))
        .unwrap();
        fs::write(&path, toml::to_string(&value).unwrap()).unwrap();
        assert!(AdapterConfig::load(&path).is_ok());
        value["brain"]["docs"]["endpoint"] = json!("https://external.example.invalid");
        fs::write(&path, toml::to_string(&value).unwrap()).unwrap();
        assert!(AdapterConfig::load(&path).is_err());
        value["brain"]["docs"]["endpoint"] = json!("http://127.0.0.1:8787");
        value["brain"]["docs"]["infisical"]["token_secret"] = json!("DEADLOCK_CENTRAL_DSN");
        fs::write(&path, toml::to_string(&value).unwrap()).unwrap();
        assert!(AdapterConfig::load(&path).is_err());
        value["brain"]["docs"]["infisical"]["token_secret"] = json!("BRAIN_SERVE_OTHER_TOKEN");
        value["brain"]["docs"]["infisical"]["unexpected"] = json!("not allowed");
        fs::write(&path, toml::to_string(&value).unwrap()).unwrap();
        assert!(AdapterConfig::load(&path).is_err());
    }

    #[test]
    fn normal_bot_toml_has_no_json_or_client_authority_fallback() {
        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("bot.toml");
        let example = include_str!("../config.example.toml");
        fs::write(&path, example).unwrap();
        let config = AdapterConfig::load(&path).unwrap();
        assert_eq!(config.infisical.credential_fd, Some(5));
        assert!(config.infisical.credential_file.is_none());
        for invalid in [
            json!({"endpoint":"http://127.0.0.1:8788","timeout_ms":5000}).to_string(),
            example.replace("[brain.docs]", "[docs]"),
            example.replace(
                "timeout_ms = 5000",
                "timeout_ms = 5000\nprincipal = \"NEVER_ECHO\"",
            ),
            example.replace(
                "timeout_ms = 5000",
                "timeout_ms = 5000\nrequested_scopes = [\"second_brain.internal\"]",
            ),
            example.replace(
                "timeout_ms = 5000",
                "timeout_ms = 5000\nknowledge_release = \"internal-release\"",
            ),
            example.replace(
                "credential_fd = 5",
                "credential_fd = 5\ncredential_file = \"/run/credentials/docs/infisical-token\"",
            ),
            String::new(),
            "#".repeat((MAX_CONFIG_BYTES + 1) as usize),
        ] {
            fs::write(&path, invalid).unwrap();
            let error = AdapterConfig::load(&path).err().unwrap();
            assert_eq!(error, AdapterError::Configuration);
            assert!(!error.to_string().contains("NEVER_ECHO"));
        }
        fs::write(&path, [0xff]).unwrap();
        assert!(AdapterConfig::load(&path).is_err());
    }

    #[test]
    fn credential_file_must_be_private_and_not_a_symlink() {
        let directory = tempfile::tempdir().unwrap();
        fs::set_permissions(directory.path(), fs::Permissions::from_mode(0o700)).unwrap();
        let credential = directory.path().join("credential");
        fs::write(&credential, "synthetic-bootstrap\n").unwrap();
        fs::set_permissions(&credential, fs::Permissions::from_mode(0o600)).unwrap();
        assert_eq!(
            read_credential(&credential).unwrap().as_str(),
            "synthetic-bootstrap"
        );
        fs::set_permissions(&credential, fs::Permissions::from_mode(0o644)).unwrap();
        assert!(read_credential(&credential).is_err());
        fs::set_permissions(&credential, fs::Permissions::from_mode(0o600)).unwrap();
        let alias = directory.path().join("alias");
        std::os::unix::fs::symlink(&credential, &alias).unwrap();
        assert!(read_credential(&alias).is_err());
    }

    #[test]
    fn credential_source_is_exactly_one_private_file_or_inherited_fd() {
        let example: BotConfig = toml::from_str(include_str!("../config.example.toml")).unwrap();
        let example = example.brain.docs;
        assert!(example.validate().is_ok());
        assert_eq!(example.infisical.credential_fd, Some(5));
        assert!(example.infisical.credential_file.is_none());
        let mut value = json!({
            "endpoint":"http://127.0.0.1:8788", "timeout_ms":5000,
            "infisical":{
                "project_id":"00000000-0000-0000-0000-000000000000", "environment":"prod",
                "secret_path":"/", "socket_path":"/run/uplink-infisical/api.sock",
                "credential_fd":5, "token_secret":"BRAIN_SERVE_DOCS_PUBLIC_TOKEN"
            }
        });
        let valid: AdapterConfig = serde_json::from_value(value.clone()).unwrap();
        assert!(valid.validate().is_ok());
        for fd in [-1, 0, 1, 2] {
            value["infisical"]["credential_fd"] = json!(fd);
            let invalid: AdapterConfig = serde_json::from_value(value.clone()).unwrap();
            assert!(invalid.validate().is_err());
        }
        value["infisical"]["credential_fd"] = json!(5);
        value["infisical"]["credential_file"] = json!("/run/credentials/docs/infisical-token");
        let ambiguous: AdapterConfig = serde_json::from_value(value.clone()).unwrap();
        assert!(ambiguous.validate().is_err());
        value["infisical"]
            .as_object_mut()
            .unwrap()
            .remove("credential_fd");
        let file: AdapterConfig = serde_json::from_value(value.clone()).unwrap();
        assert!(file.validate().is_ok());
        value["infisical"]
            .as_object_mut()
            .unwrap()
            .remove("credential_file");
        let missing: AdapterConfig = serde_json::from_value(value).unwrap();
        assert!(missing.validate().is_err());
    }

    #[test]
    fn inherited_credential_fd_preserves_offset_and_remains_owned_by_starter() {
        use std::io::{Seek, SeekFrom};
        use std::os::fd::AsRawFd;

        let mut file = tempfile::tempfile().unwrap();
        file.write_all(b"synthetic-bootstrap\n").unwrap();
        file.set_permissions(fs::Permissions::from_mode(0o400))
            .unwrap();
        file.seek(SeekFrom::End(0)).unwrap();
        let offset = file.stream_position().unwrap();
        let fd = file.as_raw_fd();
        // Der Fixture-Deskriptor bleibt während beider Ladevorgänge geöffnet.
        fcntl(fd, FcntlArg::F_SETFD(FdFlag::empty())).unwrap();
        for _ in 0..2 {
            assert_eq!(
                read_credential_fd(fd).unwrap().as_str(),
                "synthetic-bootstrap"
            );
            assert_eq!(file.stream_position().unwrap(), offset);
        }
        assert_ne!(
            fcntl(fd, FcntlArg::F_GETFD).unwrap() & FdFlag::FD_CLOEXEC.bits(),
            0
        );
    }

    #[test]
    fn inherited_credential_fd_rejects_absent_public_or_nonregular_sources() {
        use std::os::fd::AsRawFd;

        assert!(read_credential_fd(-1).is_err());
        assert!(read_credential_fd(i32::MAX).is_err());
        let file = tempfile::tempfile().unwrap();
        file.set_permissions(fs::Permissions::from_mode(0o644))
            .unwrap();
        assert!(read_credential_fd(file.as_raw_fd()).is_err());
        let (socket, _peer) = std::os::unix::net::UnixStream::pair().unwrap();
        assert!(read_credential_fd(socket.as_raw_fd()).is_err());
        let directory = tempfile::tempdir().unwrap();
        let write_only = File::create(directory.path().join("credential")).unwrap();
        write_only
            .set_permissions(fs::Permissions::from_mode(0o600))
            .unwrap();
        assert!(read_credential_fd(write_only.as_raw_fd()).is_err());
    }

    #[tokio::test]
    async fn existing_unix_transport_fetches_only_one_explicit_token_without_logging_it() {
        for use_fd in [false, true] {
            let directory = tempfile::tempdir().unwrap();
            fs::set_permissions(directory.path(), fs::Permissions::from_mode(0o700)).unwrap();
            let credential = directory.path().join("credential");
            fs::write(&credential, "synthetic-bootstrap").unwrap();
            fs::set_permissions(&credential, fs::Permissions::from_mode(0o600)).unwrap();
            let socket = directory.path().join("api.sock");
            let listener = UnixListener::bind(&socket).unwrap();
            fs::set_permissions(&socket, fs::Permissions::from_mode(0o600)).unwrap();
            let owner = fs::metadata(directory.path()).unwrap().uid();
            assert!(read_credential(&credential).is_ok());
            assert!(
                uplink_infisical_transport::validate_socket(&socket, owner).is_ok(),
                "socket path: {}",
                socket.display()
            );
            let server = thread::spawn(move || {
                let (mut stream, _) = listener.accept().unwrap();
                stream
                    .set_read_timeout(Some(Duration::from_secs(3)))
                    .unwrap();
                let mut request = Vec::new();
                let mut chunk = [0; 4096];
                while !request.windows(4).any(|part| part == b"\r\n\r\n") {
                    let read = stream.read(&mut chunk).unwrap();
                    assert!(read > 0 && request.len() + read < 16 * 1024);
                    request.extend_from_slice(&chunk[..read]);
                }
                let text = String::from_utf8(request).unwrap();
                assert!(text.starts_with("GET /api/v4/secrets/BRAIN_SERVE_OTHER_TOKEN?"));
                assert!(text.contains("projectId=00000000-0000-0000-0000-000000000000"));
                assert!(text.contains("environment=prod"));
                assert!(text.contains("includeImports=false"));
                assert!(text
                    .lines()
                    .any(|line| line
                        .eq_ignore_ascii_case("authorization: Bearer synthetic-bootstrap")));
                let body = json!({"secret":{"secretKey":"BRAIN_SERVE_OTHER_TOKEN", "secretValue":"synthetic-docs-token"}}).to_string();
                write!(stream, "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{body}", body.len()).unwrap();
            });
            let bootstrap_file = File::open(&credential).unwrap();
            let mut infisical = config(socket, credential).infisical;
            if use_fd {
                infisical.credential_file = None;
                infisical.credential_fd = Some(bootstrap_file.as_raw_fd());
            }
            let token = infisical.load_token(owner).await.unwrap();
            server.join().unwrap();
            assert_eq!(token.as_str(), "synthetic-docs-token");
            assert!(!format!("{:?}", AdapterError::Configuration).contains("synthetic-docs-token"));
        }
    }

    #[test]
    fn missing_or_mismatched_public_token_fails_closed() {
        for body in [
            json!({"secret":{"secretKey":"BRAIN_SERVE_OTHER_TOKEN", "secretValue":""}}),
            json!({"secret":{"secretKey":"BRAIN_SERVE_API_TOKEN", "secretValue":"wrong-grant"}}),
        ] {
            let reply = serde_json::from_value(body).unwrap();
            assert!(selected_token(reply, "BRAIN_SERVE_OTHER_TOKEN").is_err());
        }
        assert!(serde_json::from_value::<Reply>(json!({})).is_err());
        assert!(serde_json::from_value::<Reply>(json!({"secret":{"secretKey":"BRAIN_SERVE_OTHER_TOKEN", "secretValue":"x"}, "imports":[]})).is_err());
    }
}
