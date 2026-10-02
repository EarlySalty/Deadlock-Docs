use deadlock_docs_brain_adapter::infisical::AdapterConfig;
use deadlock_docs_brain_adapter::{direct_query, read_query, AdapterError, DocsBrainAdapter};
use std::{path::Path, process::ExitCode};

async fn configured_adapter(path: &str) -> Result<DocsBrainAdapter, AdapterError> {
    let config = AdapterConfig::load(Path::new(path))?;
    let token = config.load_token().await?;
    DocsBrainAdapter::new(&config.endpoint, &token, config.timeout())
}

async fn run(args: &[String]) -> Result<(), AdapterError> {
    match args {
        [command] if command == "--help" => {
            println!("brain-adapter prepare < query.json\nbrain-adapter answer CONFIG_JSON < query.json\nbrain-adapter query CONFIG_JSON QUESTION...\nanswer/query laden den freigegebenen Brain-Token direkt aus Infisical. prepare nutzt kein Netz. Kein Corpus-Import, kein Publishing, kein Deployment.");
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
        [command, path] if command == "answer" => {
            let query = read_query(std::io::stdin().lock())?;
            let adapter = configured_adapter(path).await?;
            let response = adapter.answer(&query).await?;
            println!(
                "{}",
                serde_json::to_string(&response).map_err(|_| AdapterError::Transport)?
            );
            Ok(())
        }
        [command, path, question @ ..] if command == "query" && !question.is_empty() => {
            let query = direct_query(&question.join(" "))?;
            let adapter = configured_adapter(path).await?;
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
