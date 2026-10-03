use serde_json::{json, Value};
use std::{
    io::Write,
    process::{Command, Output, Stdio},
    time::{Duration, Instant},
};

fn query() -> String {
    json!({"request_id":"fixture-r", "conversation_id":"fixture-c", "text":"Dokumentierte Testfrage", "requested_scopes":["docs.public"], "profile":"explain"}).to_string()
}

fn invoke(args: &[&str], input: &str) -> Output {
    let mut child = Command::new(env!("CARGO_BIN_EXE_deadlock-docs-brain-adapter"))
        .env_clear()
        .args(args)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .unwrap();
    if let Some(mut stdin) = child.stdin.take() {
        let _ = stdin.write_all(input.as_bytes());
    }
    let deadline = Instant::now() + Duration::from_secs(2);
    while child.try_wait().unwrap().is_none() {
        if Instant::now() >= deadline {
            child.kill().unwrap();
            child.wait().unwrap();
            panic!("CLI-Aufruf hat das Zeitlimit überschritten");
        }
        std::thread::sleep(Duration::from_millis(10));
    }
    child.wait_with_output().unwrap()
}

#[test]
fn help_has_no_runtime_prerequisites_or_environment_secret_path() {
    let output = invoke(&["--help"], "");
    assert!(output.status.success());
    let help = String::from_utf8(output.stdout).unwrap();
    assert!(help.contains("CONFIG_TOML"));
    assert!(!help.contains("BRAIN_ADAPTER_TOKEN"));
}

#[test]
fn prepare_works_without_a_token_and_retains_the_typed_query() {
    for scope in ["docs.public", "bot.public"] {
        let mut input: Value = serde_json::from_str(&query()).unwrap();
        input["requested_scopes"] = json!([scope]);
        let output = invoke(&["prepare"], &input.to_string());
        assert!(output.status.success());
        let wire: Value = serde_json::from_slice(&output.stdout).unwrap();
        assert_eq!(wire["request_id"], "fixture-r");
        assert_eq!(wire["requested_scopes"], json!([scope]));
        assert!(wire.get("principal").is_none());
    }
}

#[test]
fn answer_rejects_a_scope_that_differs_from_config_before_loading_credentials() {
    let directory = tempfile::tempdir().unwrap();
    let path = directory.path().join("bot.toml");
    let config = include_str!("../config.example.toml").replace(
        "[brain.docs]",
        "[brain.docs]\npublic_scope = \"bot.public\"",
    );
    std::fs::write(&path, config).unwrap();
    let output = invoke(&["answer", path.to_str().unwrap()], &query());
    assert_eq!(output.status.code(), Some(64));
    assert!(output.stdout.is_empty());
    assert_eq!(
        String::from_utf8(output.stderr).unwrap().trim(),
        deadlock_docs_brain_adapter::AdapterError::ScopePolicy.to_string()
    );
}

#[test]
fn scope_injection_is_rejected_without_echoing_input() {
    let mut q: Value = serde_json::from_str(&query()).unwrap();
    q["principal"] = json!({"secret":"NEVER_ECHO"});
    let output = invoke(&["prepare"], &q.to_string());
    assert!(!output.status.success());
    assert!(output.stdout.is_empty());
    assert!(!String::from_utf8_lossy(&output.stderr).contains("NEVER_ECHO"));
}

#[test]
fn answer_requires_a_config_before_any_transport_or_output() {
    let output = invoke(&["answer", "/path/that/does/not/exist"], &query());
    assert!(!output.status.success());
    assert!(output.stdout.is_empty());
    let directory = tempfile::tempdir().unwrap();
    let config_fifo = directory.path().join("config-fifo");
    let credential_fifo = directory.path().join("credential-fifo");
    let mode = nix::sys::stat::Mode::S_IRUSR | nix::sys::stat::Mode::S_IWUSR;
    nix::unistd::mkfifo(&config_fifo, mode).unwrap();
    nix::unistd::mkfifo(&credential_fifo, mode).unwrap();
    let mut config: Value = toml::from_str(include_str!("../config.example.toml")).unwrap();
    config["brain"]["docs"]["infisical"]
        .as_object_mut()
        .unwrap()
        .remove("credential_fd");
    config["brain"]["docs"]["infisical"]["credential_file"] = json!(credential_fifo);
    let config_path = directory.path().join("bot.toml");
    std::fs::write(&config_path, toml::to_string(&config).unwrap()).unwrap();
    for path in [&config_fifo, &config_path] {
        let output = invoke(&["answer", path.to_str().unwrap()], &query());
        assert_eq!(output.status.code(), Some(64));
        assert!(output.stdout.is_empty());
    }
}

#[test]
fn direct_query_requires_a_config_before_any_transport_or_output() {
    let output = invoke(
        &[
            "query",
            "/path/that/does/not/exist",
            "Was",
            "ist",
            "dokumentiert?",
        ],
        "",
    );
    assert!(!output.status.success());
    assert!(output.stdout.is_empty());
}

#[test]
fn old_endpoint_and_timeout_arguments_no_longer_enable_environment_auth() {
    let output = invoke(&["query", "http://127.0.0.1:1", "1000", "Frage"], "");
    assert!(!output.status.success());
    assert!(output.stdout.is_empty());
}
