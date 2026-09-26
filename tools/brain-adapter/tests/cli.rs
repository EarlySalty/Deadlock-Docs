use serde_json::{json, Value};
use std::{
    io::{Read, Write},
    net::TcpListener,
    process::{Command, Output, Stdio},
    thread,
    time::{Duration, Instant},
};
fn query() -> String {
    json!({"request_id":"fixture-r", "conversation_id":"fixture-c", "text":"Dokumentierte Testfrage", "requested_scopes":["docs.public"], "profile":"explain"}).to_string()
}
fn invoke(args: &[&str], input: &str, token: Option<&str>) -> Output {
    let mut command = Command::new(env!("CARGO_BIN_EXE_deadlock-docs-brain-adapter"));
    command
        .env_clear()
        .args(args)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped());
    if let Some(token) = token {
        command.env("BRAIN_ADAPTER_TOKEN", token);
    }
    let mut child = command.spawn().unwrap();
    if let Some(mut stdin) = child.stdin.take() {
        let _ = stdin.write_all(input.as_bytes());
    }
    child.wait_with_output().unwrap()
}
#[test]
fn help_has_no_runtime_prerequisites() {
    assert!(invoke(&["--help"], "", None).status.success());
}
#[test]
fn prepare_works_without_a_token_and_retains_the_typed_query() {
    let output = invoke(&["prepare"], &query(), None);
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
    let output = invoke(&["prepare"], &q.to_string(), None);
    assert!(!output.status.success());
    assert!(output.stdout.is_empty());
    assert!(!String::from_utf8_lossy(&output.stderr).contains("NEVER_ECHO"));
}
#[test]
fn answer_requires_explicit_credentials_before_reading_a_question() {
    let output = invoke(&["answer", "http://127.0.0.1:1", "1000"], "", None);
    assert!(!output.status.success());
    assert!(output.stdout.is_empty());
}
#[test]
fn direct_query_path_requires_explicit_credentials() {
    let output = invoke(
        &[
            "query",
            "http://127.0.0.1:1",
            "1000",
            "Was",
            "ist",
            "dokumentiert?",
        ],
        "",
        None,
    );
    assert!(!output.status.success());
    assert!(output.stdout.is_empty());
}

#[test]
fn explicit_answer_uses_only_the_loopback_fixture_and_public_wire_contract() {
    let listener = TcpListener::bind("127.0.0.1:0").unwrap();
    listener.set_nonblocking(true).unwrap();
    let endpoint = format!("http://{}", listener.local_addr().unwrap());
    let server = thread::spawn(move || {
        let until = Instant::now() + Duration::from_secs(5);
        let mut stream = loop {
            match listener.accept() {
                Ok((stream, _)) => break stream,
                Err(error)
                    if error.kind() == std::io::ErrorKind::WouldBlock && Instant::now() < until =>
                {
                    thread::sleep(Duration::from_millis(10))
                }
                Err(error) => panic!("fixture accept: {error}"),
            }
        };
        stream
            .set_read_timeout(Some(Duration::from_secs(3)))
            .unwrap();
        let mut bytes = Vec::new();
        let mut buffer = [0; 4096];
        loop {
            let count = stream.read(&mut buffer).unwrap();
            assert!(count > 0);
            bytes.extend_from_slice(&buffer[..count]);
            if let Some(end) = bytes.windows(4).position(|w| w == b"\r\n\r\n") {
                let headers = String::from_utf8_lossy(&bytes[..end]);
                assert!(headers.starts_with("POST /v1/answer HTTP/1.1"));
                assert!(headers
                    .lines()
                    .any(|l| l.eq_ignore_ascii_case("authorization: Bearer fixture-token")));
                let len: usize = headers
                    .lines()
                    .find_map(|l| {
                        l.to_ascii_lowercase()
                            .strip_prefix("content-length:")
                            .map(|s| s.trim().parse().unwrap())
                    })
                    .unwrap();
                if bytes.len() >= end + 4 + len {
                    let query: Value = serde_json::from_slice(&bytes[end + 4..]).unwrap();
                    assert_eq!(query["requested_scopes"], json!(["docs.public"]));
                    break;
                }
            }
            assert!(bytes.len() < 70 * 1024);
        }
        let body = json!({"contract_version":"brain.public.v1", "request_id":"fixture-r", "knowledge_release":"fixture-release", "status":"insufficient_evidence", "text":"", "citations":[]}).to_string();
        write!(stream, "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{body}", body.len()).unwrap();
    });
    let output = invoke(
        &["answer", &endpoint, "1500"],
        &query(),
        Some("fixture-token"),
    );
    server.join().unwrap();
    assert!(
        output.status.success(),
        "{}",
        String::from_utf8_lossy(&output.stderr)
    );
    let response: Value = serde_json::from_slice(&output.stdout).unwrap();
    assert_eq!(response["status"], "insufficient_evidence");
    assert!(!String::from_utf8_lossy(&output.stdout).contains("fixture-token"));
}
