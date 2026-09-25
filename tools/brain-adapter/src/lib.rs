#![forbid(unsafe_code)]
//! Explicit public documentation query port. Never scans, uploads or publishes the corpus.
use brain_client::{AsyncBrainClient, PublicAnswerResponse, Query, MAX_REQUEST_BYTES};
use std::{collections::BTreeSet, io::Read, time::Duration};

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
}
