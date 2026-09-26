use deadlock_docs_brain_adapter::{direct_query, read_query, AdapterError, DocsBrainAdapter};
use std::{process::ExitCode, time::Duration};

async fn run(args: &[String]) -> Result<(), AdapterError> {
    match args {
        [command] if command == "--help" => {
            println!("brain-adapter prepare < query.json\nbrain-adapter answer LOOPBACK_ENDPOINT TIMEOUT_MS < query.json\nbrain-adapter query LOOPBACK_ENDPOINT TIMEOUT_MS QUESTION...\nanswer/query benötigen das explizit gesetzte BRAIN_ADAPTER_TOKEN. prepare nutzt kein Netz. Kein Corpus-Import, kein Publishing, kein Deployment.");
            Ok(())
        }
        [command] if command == "prepare" => {
            let query = read_query(std::io::stdin().lock())?;
            println!(
                "{}",
                serde_json::to_string(&query).map_err(|_| AdapterError::InvalidInput)?
            );
            Ok(())
        }
        [command, endpoint, timeout] if command == "answer" => {
            let timeout = timeout
                .parse::<u64>()
                .map_err(|_| AdapterError::Configuration)?;
            let token =
                std::env::var("BRAIN_ADAPTER_TOKEN").map_err(|_| AdapterError::Configuration)?;
            let adapter = DocsBrainAdapter::new(endpoint, &token, Duration::from_millis(timeout))?;
            let query = read_query(std::io::stdin().lock())?;
            let response = adapter.answer(&query).await?;
            println!(
                "{}",
                serde_json::to_string(&response).map_err(|_| AdapterError::Transport)?
            );
            Ok(())
        }
        [command, endpoint, timeout, question @ ..]
            if command == "query" && !question.is_empty() =>
        {
            let timeout = timeout
                .parse::<u64>()
                .map_err(|_| AdapterError::Configuration)?;
            let token =
                std::env::var("BRAIN_ADAPTER_TOKEN").map_err(|_| AdapterError::Configuration)?;
            let adapter = DocsBrainAdapter::new(endpoint, &token, Duration::from_millis(timeout))?;
            let query = direct_query(&question.join(" "))?;
            let response = adapter.answer(&query).await?;
            println!(
                "{}",
                serde_json::to_string(&response).map_err(|_| AdapterError::Transport)?
            );
            Ok(())
        }
        _ => Err(AdapterError::InvalidInput),
    }
}
#[tokio::main(flavor = "current_thread")]
async fn main() -> ExitCode {
    let args = std::env::args_os()
        .skip(1)
        .map(|arg| arg.into_string().map_err(|_| AdapterError::InvalidInput))
        .collect::<Result<Vec<_>, _>>();
    let result = match args {
        Ok(args) => run(&args).await,
        Err(error) => Err(error),
    };
    match result {
        Ok(()) => ExitCode::SUCCESS,
        Err(error) => {
            eprintln!("{error}");
            ExitCode::from(64)
        }
    }
}
