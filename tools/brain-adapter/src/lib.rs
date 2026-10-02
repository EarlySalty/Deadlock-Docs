#![forbid(unsafe_code)]
//! Explicit public documentation query port. Never scans, uploads or publishes the corpus.
use brain_client::{
    AnswerProfile, AsyncBrainClient, PublicAnswerResponse, Query, MAX_REQUEST_BYTES,
};
use std::{collections::BTreeSet, io::Read, time::Duration};
pub mod infisical;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AdapterError {
    InvalidInput,
    ScopePolicy,
    Configuration,
    Transport,
}
impl std::fmt::Display for AdapterError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(match self {
            Self::InvalidInput => "Ungültige oder zu große Brain-Anfrage",
            Self::ScopePolicy => "Nur der explizite öffentliche Dokumentationsbereich ist erlaubt",
            Self::Configuration => "Explizite lokale Brain-Konfiguration erforderlich",
            Self::Transport => "Brain-Transport oder Antwortvertrag fehlgeschlagen",
        })
    }
}
impl std::error::Error for AdapterError {}

pub fn validate_query(query: &Query) -> Result<(), AdapterError> {
    query.validate().map_err(|_| AdapterError::InvalidInput)?;
    if query.requested_scopes != BTreeSet::from(["docs.public".to_owned()]) {
        return Err(AdapterError::ScopePolicy);
    }
    Ok(())
}
pub fn direct_query(text: &str) -> Result<Query, AdapterError> {
    let text = text.trim();
    if text.is_empty() {
        return Err(AdapterError::InvalidInput);
    }
    let nonce = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .map_err(|_| AdapterError::InvalidInput)?
        .as_nanos();
    let id = format!("docs-brain-{}-{nonce}", std::process::id());
    let query = Query {
        request_id: id.clone(),
        conversation_id: id,
        text: text.to_string(),
        domain: None,
        requested_scopes: BTreeSet::from(["docs.public".to_owned()]),
        profile: AnswerProfile::Explain,
        patch: None,
        mode: None,
    };
    validate_query(&query)?;
    Ok(query)
}

pub fn read_query(input: impl Read) -> Result<Query, AdapterError> {
    let mut bytes = Vec::new();
    input
        .take(MAX_REQUEST_BYTES as u64 + 1)
        .read_to_end(&mut bytes)
        .map_err(|_| AdapterError::InvalidInput)?;
    if bytes.len() > MAX_REQUEST_BYTES {
        return Err(AdapterError::InvalidInput);
    }
    let query: Query = serde_json::from_slice(&bytes).map_err(|_| AdapterError::InvalidInput)?;
    validate_query(&query)?;
    Ok(query)
}
pub struct DocsBrainAdapter {
    client: AsyncBrainClient,
}
impl DocsBrainAdapter {
    pub fn new(endpoint: &str, token: &str, timeout: Duration) -> Result<Self, AdapterError> {
        Ok(Self {
            client: AsyncBrainClient::new_local(endpoint, token, timeout)
                .map_err(|_| AdapterError::Configuration)?,
        })
    }
    pub async fn answer(&self, query: &Query) -> Result<PublicAnswerResponse, AdapterError> {
        validate_query(query)?;
        self.client
            .answer(query)
            .await
            .map_err(|_| AdapterError::Transport)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use brain_client::AnswerProfile;
    fn query() -> Query {
        Query {
            request_id: "fixture-request".into(),
            conversation_id: "fixture-conversation".into(),
            text: "Dokumentierte Frage äöü".into(),
            domain: None,
            requested_scopes: BTreeSet::from(["docs.public".into()]),
            profile: AnswerProfile::Explain,
            patch: None,
            mode: None,
        }
    }
    #[test]
    fn typed_query_is_preserved_without_synthesizing_authority() {
        let expected = query();
        let bytes = serde_json::to_vec(&expected).unwrap();
        assert_eq!(read_query(bytes.as_slice()).unwrap(), expected);
    }
    #[test]
    fn private_and_implicit_scopes_are_not_publicly_reinterpreted() {
        for scopes in [
            BTreeSet::new(),
            BTreeSet::from(["docs.internal".into()]),
            BTreeSet::from(["docs.public".into(), "docs.internal".into()]),
        ] {
            let mut query = query();
            query.requested_scopes = scopes;
            assert_eq!(validate_query(&query), Err(AdapterError::ScopePolicy));
        }
    }
    #[test]
    fn injected_principal_and_oversized_input_fail_before_transport() {
        let mut value = serde_json::to_value(query()).unwrap();
        value["principal"] = serde_json::json!({"admin":true});
        assert_eq!(
            read_query(value.to_string().as_bytes()),
            Err(AdapterError::InvalidInput)
        );
        assert_eq!(
            read_query("x".repeat(MAX_REQUEST_BYTES + 1).as_bytes()),
            Err(AdapterError::InvalidInput)
        );
    }

    #[test]
    fn direct_query_is_an_actual_public_brain_client_request() {
        let query = direct_query("Was ist dokumentiert?").unwrap();
        assert_eq!(
            query.requested_scopes,
            BTreeSet::from(["docs.public".into()])
        );
        assert!(query.domain.is_none());
        assert!(query.request_id.starts_with("docs-brain-"));
        assert_eq!(query.request_id, query.conversation_id);
    }
    #[test]
    fn unavailable_and_build_rejected_are_part_of_the_pinned_wire_contract() {
        assert_eq!(
            serde_json::to_string(&brain_client::AnswerStatus::Unavailable).unwrap(),
            "\"unavailable\""
        );
        assert_eq!(
            serde_json::to_string(&brain_client::AnswerStatus::BuildRejected).unwrap(),
            "\"build_rejected\""
        );
    }

    #[test]
    fn external_https_is_not_implicit_permission_to_export_questions() {
        assert!(matches!(
            DocsBrainAdapter::new(
                "https://example.invalid",
                "fixture-token",
                Duration::from_secs(1)
            ),
            Err(AdapterError::Configuration)
        ));
    }
    #[tokio::test]
    async fn transport_failure_never_falls_back_to_local_corpus_or_model() {
        let adapter = DocsBrainAdapter::new(
            "http://127.0.0.1:1",
            "fixture-token",
            Duration::from_secs(1),
        )
        .unwrap();
        assert_eq!(adapter.answer(&query()).await, Err(AdapterError::Transport));
    }

    #[tokio::test]
    async fn public_query_uses_typed_loopback_transport_without_client_supplied_authority() {
        use std::{
            io::{Read, Write},
            net::TcpListener,
            thread,
        };
        let listener = TcpListener::bind("127.0.0.1:0").unwrap();
        let endpoint = format!("http://{}", listener.local_addr().unwrap());
        let server = thread::spawn(move || {
            let (mut stream, _) = listener.accept().unwrap();
            stream
                .set_read_timeout(Some(Duration::from_secs(3)))
                .unwrap();
            let mut bytes = Vec::new();
            let mut buffer = [0; 4096];
            loop {
                let count = stream.read(&mut buffer).unwrap();
                assert!(count > 0 && bytes.len() + count < 70 * 1024);
                bytes.extend_from_slice(&buffer[..count]);
                if let Some(end) = bytes.windows(4).position(|part| part == b"\r\n\r\n") {
                    let header = String::from_utf8_lossy(&bytes[..end]);
                    assert!(header.starts_with("POST /v1/answer HTTP/1.1"));
                    assert!(header.lines().any(|line| line
                        .eq_ignore_ascii_case("authorization: Bearer synthetic-docs-token")));
                    let length: usize = header
                        .lines()
                        .find_map(|line| {
                            line.to_ascii_lowercase()
                                .strip_prefix("content-length:")
                                .map(|part| part.trim().parse().unwrap())
                        })
                        .unwrap();
                    if bytes.len() >= end + 4 + length {
                        let value: serde_json::Value =
                            serde_json::from_slice(&bytes[end + 4..]).unwrap();
                        assert_eq!(
                            value["requested_scopes"],
                            serde_json::json!(["docs.public"])
                        );
                        assert!(value.get("principal").is_none());
                        break;
                    }
                }
            }
            let body = serde_json::json!({"contract_version":"brain.public.v1", "request_id":"fixture-request", "knowledge_release":"fixture-release", "status":"insufficient_evidence", "text":"", "citations":[]}).to_string();
            write!(stream, "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{body}", body.len()).unwrap();
        });
        let adapter =
            DocsBrainAdapter::new(&endpoint, "synthetic-docs-token", Duration::from_secs(2))
                .unwrap();
        let response = adapter.answer(&query()).await.unwrap();
        server.join().unwrap();
        assert_eq!(
            response.status,
            brain_client::AnswerStatus::InsufficientEvidence
        );
        assert_eq!(response.knowledge_release, "fixture-release");
    }
}
