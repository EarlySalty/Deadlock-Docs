use serde_json::{json, Value};
use std::{
    io::Write,
    process::{Command, Output, Stdio},
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
    child.wait_with_output().unwrap()
}

#[test]
fn help_has_no_runtime_prerequisites_or_environment_secret_path() {
    let output = invoke(&["--help"], "");
    assert!(output.status.success());
    let help = String::from_utf8(output.stdout).unwrap();
    assert!(help.contains("CONFIG_JSON"));
    assert!(!help.contains("BRAIN_ADAPTER_TOKEN"));
}

#[test]
fn prepare_works_without_a_token_and_retains_the_typed_query() {
    let output = invoke(&["prepare"], &query());
    assert!(output.status.success());
    let wire: Value = serde_json::from_slice(&output.stdout).unwrap();
    assert_eq!(wire["request_id"], "fixture-r");
    assert_eq!(wire["requested_scopes"], json!(["docs.public"]));
    assert!(wire.get("principal").is_none());
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
