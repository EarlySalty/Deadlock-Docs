# dl-ai: zentrale LLM-Provider-Schicht

Interne Referenz für KI-Support-Agenten. Beschrieben ist der gelesene Quellstand, nicht die aktive Deployment-Konfiguration oder eine live geprüfte Anbieter-Verfügbarkeit.

## Kurzantwort

- **Anbieter und Modell:** Für `BotPate`, `Faq` und `BrainAntwort` ist Fireworks der Anbieter-Standard. Der gemeinsame Modell-Standard ist **DeepSeek V4 Flash**, konkret `accounts/fireworks/models/deepseek-v4-flash-0731`. Anbieter und Modell lassen sich überschreiben. [chat_provider.rs:594–612; lib.rs:30–42]
- **Modellauflösung:** Der Modellname wird aus Anfrage beziehungsweise Konfiguration übernommen, nicht über einen Modellkatalog ermittelt. Es gibt entgegen der Annahme „statt einkompiliert“ einen **einkompilierten Rückfallwert**. Ein konfiguriertes Modell kann ohne Änderung dieser Konstante verwendet werden. [chat_provider.rs:572–583, 687–711, 765–768; lib.rs:434–465, 501–506]
- **Timeout:** Entgegen der Erwartung „kein hartes Timeout“ setzt der Code explizite HTTP-Zeitlimits: **110 Sekunden für `BotPate`**, **45 Sekunden für die übrigen Fälle im Provider-Fabrikweg**, **60 Sekunden beim direkten `FireworksClient`**. Eine Timeout-Umgebungsvariable wird in diesen Bauwegen nicht ausgewertet. [chat_provider.rs:11–26, 562–569, 1066–1088; lib.rs:434–465]
- **Gemeinsame Textschnittstelle:** `TextGenerator::generate_text(GenerateRequest) -> Option<String>`. Die Brücke `ChatTextGenerator` verbindet diese Konsumentenschnittstelle mit dem typisierten `ChatProvider`. [lib.rs:54–63, 117–121; chat_text.rs:1–21, 58–100]
- **Denkmodus:** Der direkte `FireworksClient` übermittelt ein gesetztes `reasoning_effort`. `ChatTextGenerator` reicht es ausdrücklich **nicht** weiter und protokolliert eine Warnung. Das Weglassen ist keine belegte Abschaltung des Denkmodus. [lib.rs:520–522; chat_text.rs:60–67]

## Quellen und Geltungsbereich

Alle folgenden Referenzen beziehen sich auf Dateien unter:

`Deadlock-Bots/rust/crates/dl-ai/src/`

- `lib.rs`: öffentliche Textschnittstelle, direkter `FireworksClient`, Modellkonstanten.
- `chat_provider.rs`: Provider-Trait, Auswahl und Fabrik, HTTP-Requests, Retries und Antwortparser.
- `chat_text.rs`: Adapter vom `ChatProvider` auf `TextGenerator`.

Die Referenz erklärt die gemeinsame Provider-Seite für dl-knowledge und Concierge. Deren konkrete Konstruktoraufrufe, eingesetzte Adapter, Anfrageparameter und zusätzliche Anwendungszeitlimits wurden außerhalb von `dl-ai` nicht geprüft. Deshalb nicht allein aus dem Konsumentennamen auf einen der folgenden Bauwege schließen.

## 1. Zwei Bauwege, dieselbe Textschnittstelle

### Provider-Fabrik mit Adapter

```text
LlmProviderConfig::from_env
  → build_provider_for_env(use_case, lookup)
  → Anbieterprüfung + Modellkonfiguration + RetryConfig
  → OpenAiChatProvider::from_fireworks_env bei Anbieter Fireworks
  → Transparenz-Wrapper
  → ChatTextGenerator::new oder ::new_json
  → Arc<dyn TextGenerator>
```

Die Fabrik liefert zunächst `Arc<dyn ChatProvider>`. Die Verpackung als `ChatTextGenerator` ist ein separater Schritt. Fireworks verwendet hier den OpenAI-kompatiblen `OpenAiChatProvider`, bleibt im Logging aber als `fireworks` gekennzeichnet. Der Typname bedeutet also nicht, dass die Anfrage an OpenAI geht. [chat_provider.rs:462–485, 655–663, 687–711, 791–805; chat_text.rs:24–41]

Der Adapter ist laut Modulbeschreibung die Brücke für bestehende Konsumenten, damit diese nicht durch direkten Clientbau die Anbieterprüfung umgehen. Er baut aus `prompt` eine User-Nachricht und überträgt System-Prompt, Modell, Temperatur und Ausgabelimit in `ChatParams`. `new` erzwingt kein JSON, `new_json` setzt den JSON-Modus. [chat_text.rs:1–6, 24–74]

### Direkter Client

`FireworksClient::from_env` beziehungsweise `FireworksClient::new` baut einen eigenständigen Client. Dieser implementiert `TextGenerator` direkt, ohne den oben beschriebenen Fabrik-, Retry- oder Transparenzpfad automatisch zu durchlaufen. Er setzt bei jeder Anfrage `response_format: {"type": "json_object"}`. Sein HTTP-Aufruf erfolgt einmalig; ein eigener Retry-Loop ist dort nicht vorhanden. [lib.rs:434–465, 500–544]

### Vertrag der Traits

```rust
#[async_trait::async_trait]
pub trait TextGenerator: Send + Sync {
    async fn generate_text(&self, request: GenerateRequest) -> Option<String>;
}
```

`GenerateRequest` enthält `prompt`, `system_prompt: Option<String>`, `model: Option<String>`, `max_output_tokens: Option<u32>`, `reasoning_effort: Option<String>` und `temperature: f64`. Der Trait liefert weder einen typisierten Fehler noch Modell- oder Verbrauchsmetadaten. [lib.rs:54–63, 117–121]

Die darunterliegende Schnittstelle ist:

```rust
async fn chat(
    &self,
    messages: &[ChatMessage],
    params: ChatParams,
) -> Result<ChatResponse, ChatProviderError>;

fn effective_model(&self, params: &ChatParams) -> Option<String>;
```

`ChatProvider` verlangt ebenfalls `Send + Sync`. `ChatResponse` enthält Text, optionalen Modellnamen und Verbrauchsmetadaten; Fehler umfassen `Timeout`, `RateLimit`, `Auth` und `Provider`. Der Adapter macht aus einem Fehler oder leerem Antworttext `None`, ansonsten `Some(content)`. Welche Ersatzantwort die Anwendung daraufhin ausgibt, entscheidet nicht dieser Trait. [chat_provider.rs:114–151, 178–202; chat_text.rs:75–97]

**Wichtig zum Ausgabelimit:** `max_output_tokens: None` bedeutet beim direkten `FireworksClient` und beim Adapter jeweils den Standard von 800 Ausgabetokens. Nur ein direkter `ChatProvider`-Aufruf mit `ChatParams.max_tokens: None` lässt im OpenAI-/Fireworks-Payload das Limitfeld weg. Diese beiden `None`-Bedeutungen nicht verwechseln. [lib.rs:46, 503–506; chat_text.rs:43–55; chat_provider.rs:778–785]

## 2. Anbieter- und Modellauflösung

### Anbieterwahl

Bei `LlmProviderConfig::from_env` gilt diese Priorität:

1. `DL_LLM_PROVIDER_<USE_CASE>`
2. `DL_LLM_PROVIDER_DEFAULT`
3. `default_provider_for(use_case)`

Für die hier relevanten Fälle lauten die Suffixe `BOT_PATE`, `FAQ` und `BRAIN_ANTWORT`; ihr Anbieter-Standard ist Fireworks. Andere unterstützte Anbieter sind OpenAI, MiniMax und Mistral sowie ein nur durch Tests injizierbarer Mock. Die Fabrik prüft außerdem die Anbieterzulässigkeit; MiniMax ist für die standardmäßig als `UserContent` klassifizierten Fälle grundsätzlich gesperrt, abgesehen von einem expliziten Entwicklungs-Override. [chat_provider.rs:242–260, 297–329, 377–398, 434–479, 594–629]

### Fireworks-Modell im Fabrikweg

Für eine einzelne Anfrage gilt, von höchster zu niedrigster Priorität:

1. Explizites `ChatParams.model`, bei Verwendung des Adapters aus `GenerateRequest.model`.
2. `DL_LLM_MODEL_<USE_CASE>`, beispielsweise `DL_LLM_MODEL_BOT_PATE`, `DL_LLM_MODEL_FAQ` oder `DL_LLM_MODEL_BRAIN_ANTWORT`.
3. `FIREWORK_MODEL`.
4. `FIREWORKS_MODEL`.
5. `DEFAULT_FIREWORKS_MODEL`: `accounts/fireworks/models/deepseek-v4-flash-0731`.

Die Umgebungswerte werden getrimmt; leere Werte werden übersprungen. Die konfigurierten Werte werden beim Bau des Providers in dessen `default_model` gespeichert. Ein vorhandener Provider liest sie nicht bei jeder Anfrage erneut. [chat_provider.rs:572–583, 641–645, 687–745, 765–768; chat_text.rs:43–55; lib.rs:42]

**Implementierungsdetail:** Die Provider-Konstruktoren fragen intern den Schlüssel `DL_LLM_MODEL_BOT_PATE` ab. Erst `model_key_lookup` in der Fabrik übersetzt diesen in den jeweiligen Anwendungsschlüssel. Das Bot-Pate-Modell ist dadurch kein globaler Rückfall für alle Fälle. Wer `from_fireworks_env` direkt ohne diese Übersetzung aufruft, erhält diese Trennung nicht. [chat_provider.rs:467–473, 555–583, 700–703]

### Fireworks-Modell im direkten Client

Hier gilt nur:

`GenerateRequest.model` → `FIREWORK_MODEL` → `FIREWORKS_MODEL` → `DEFAULT_FIREWORKS_MODEL`.

`FireworksClient::from_env` liest keinen `DL_LLM_MODEL_<USE_CASE>`-Schlüssel. `new` kann alternativ einen Modellnamen direkt als Konstruktorparameter erhalten. [lib.rs:434–465, 501–506]

### Keine dynamische Modell-Discovery

Die untersuchten Fireworks-Bauwege übernehmen die Modellzeichenfolge aus diesen Quellen. Sie fragen keinen `/models`-Endpunkt ab und übersetzen keinen Anzeigenamen wie „DeepSeek V4 Flash“ in eine Anbieter-ID. `effective_model` liefert das explizite oder beim Bau konfigurierte Modell schon vor dem Aufruf; das ist keine Remote-Auflösung. Bei Erfolg kann zusätzlich der vom Anbieter zurückgegebene Modellname in `ChatResponse.model` stehen. [chat_provider.rs:687–711, 750–799, 1388–1395; lib.rs:434–465, 501–543]

**Verfügbarkeit bleibt offen:** Der Kommentar zur Modellkonstante dokumentiert für den 26.08.2026 einen HTTP 404 beim undatierten Namen und HTTP 412 wegen eines gesperrten Kontos bei der datierten Variante. Er stellt ausdrücklich klar, dass der 412 die Verfügbarkeit von `-0731` nicht beweist. Das ist ein historischer Quellkommentar, keine aktuelle Kontodiagnose. [lib.rs:30–42]

## 3. Endpunkt, Zugang und Timeout

### Fireworks-Endpunkt

Beide Fireworks-Wege nutzen standardmäßig:

- Basis-URL: `https://api.fireworks.ai/inference/v1`
- Anfrage: `POST https://api.fireworks.ai/inference/v1/chat/completions`
- Protokoll: OpenAI-kompatibles JSON mit `model` und `messages`, keine Streaming-Auswertung in diesen Implementierungen.

Konfigurationspriorität der Basis-URL: `FIREWORK_BASE_URL` → `FIREWORKS_BASE_URL` → Standard. Abschließende Schrägstriche werden beim Bau entfernt; `/chat/completions` wird beim Aufruf angehängt. Die konfigurierte Basis sollte daher nicht bereits den vollständigen Chat-Pfad enthalten. [chat_provider.rs:29, 697–699, 738–741, 771–798; lib.rs:49, 442–444, 452–465, 513–543]

Für den Zugang wird zuerst `FIREWORK_API_KEY`, dann `FIREWORKS_API_KEY` gelesen. Fehlt beides, liefert der direkte Konstruktor `None`, die Provider-Variante einen Initialisierungsfehler. Requests verwenden Bearer-Authentifizierung. Hier werden ausschließlich Variablennamen dokumentiert, keine Zugangswerte. [lib.rs:435–441, 524–528; chat_provider.rs:691–696, 791–796]

### Tatsächliche HTTP-Zeitlimits

| Bauweg | Gesetztes Zeitlimit | Wie festgelegt? |
|---|---:|---|
| Provider-Fabrik, `LlmUseCase::BotPate` | 110 Sekunden je HTTP-Versuch | `BOT_PATE_REQUEST_TIMEOUT` über `retry_for_use_case` |
| Provider-Fabrik, alle anderen Fälle, auch `Faq` und `BrainAntwort` | 45 Sekunden je HTTP-Versuch | `DEFAULT_REQUEST_TIMEOUT` über `retry_for_use_case` |
| Direkter `FireworksClient` | 60 Sekunden | Literal im HTTP-Client-Konstruktor |
| Manuell gebauter Chat-Provider | übergebene `RetryConfig.request_timeout`; Standard 45 Sekunden | Konstruktorparameter, kein hier ausgewerteter Timeout-Umgebungsschlüssel |

Belege: [chat_provider.rs:11–26, 462–473, 562–569, 687–711, 714–745, 1066–1088; lib.rs:452–465].

`RetryConfig::http_client` setzt ausdrücklich `.timeout(self.request_timeout)`. Beide HTTP-Client-Bauwege verwenden bei einem Builder-Fehler `unwrap_or_default()`; die oben genannten Werte beschreiben den regulär erfolgreichen Clientbau. [chat_provider.rs:1083–1088; lib.rs:458–461]

**Abgrenzung zum Concierge:** Der Kommentar am Dateianfang spricht noch von einem 100-Sekunden-Fenster, während die ausführbare Provider-Konstante 110 Sekunden beträgt. Ein Test begründet dies damit, dass der HTTP-Versuch das im Test angenommene Concierge-Limit von 100 Sekunden überleben soll. Die tatsächliche äußere Concierge-Abbruchlogik wurde hier nicht geprüft. Daher nicht „Concierge wartet 110 Sekunden“ behaupten, sondern „BotPate-HTTP-Versuch ist auf 110 Sekunden konfiguriert“. [chat_provider.rs:12–24, 1756–1766]

### Retries und Fehler

Im Provider-Weg sind standardmäßig zwei Wiederholungen vorgesehen, also höchstens drei Versuche. Wiederholt werden nur HTTP 429 und 5xx, mit exponentiellem Backoff von zunächst 250, dann 500 Millisekunden. Ein beim Senden erkannter Timeout oder sonstiger Transportfehler bricht sofort ab; 401 und 403 werden zu `Auth`. Das Zeitlimit gilt für den einzelnen HTTP-Versuch, nicht als gemeinsames Gesamtbudget über alle Wiederholungen. [chat_provider.rs:25–26, 1066–1094, 1103–1189]

Nuance für die Fehlersuche: Die spezielle Timeout-Zuordnung liegt um `.send().await`. Fehler beim anschließenden Lesen als JSON werden pauschal als `Provider("invalid JSON response")` abgebildet. Nicht jeder Fehler beim Empfang des Antwortkörpers erscheint deshalb als typisierter `Timeout`. [chat_provider.rs:1110–1129, 1190–1193]

## 4. Denkmodus und Antwortverarbeitung

| Pfad | Behandlung von `reasoning_effort` |
|---|---|
| Direkter `FireworksClient` | `Some(wert)` wird unverändert als JSON-Feld gesendet; `None` lässt das Feld weg. Keine lokale Wertvalidierung. |
| `ChatTextGenerator` → `ChatProvider` | Ein gesetzter Wert erzeugt eine Warnung und wird verworfen. `ChatParams` besitzt kein entsprechendes Feld. |
| Direkter OpenAI-/Fireworks-`ChatProvider` | Sendet kein `reasoning_effort`. Die modellabhängige Parameterbehandlung unten ist davon getrennt. |

Belege: [lib.rs:54–63, 513–522; chat_text.rs:43–67; chat_provider.rs:94–100, 765–789].

Der Test des direkten Clients prüft beispielhaft, dass der String `"none"` übertragen und bei `None` kein Feld erzeugt wird. Das beweist das Anfrageformat, nicht die Wirkung beim konkreten Fireworks-Modell. Weder die zulässigen Anbieterwerte noch dessen Standard-Denkmodus sind durch diese lokale Implementierung belegt. [lib.rs:1395–1429]

`openai_uses_reasoning_parameters` erkennt ausschließlich Modellpräfixe `gpt-5`, `o1`, `o3` und `o4`. Bei diesen Modellen entfällt `temperature`, und das Ausgabelimit heißt `max_completion_tokens` statt `max_tokens`. Die Fireworks-ID für DeepSeek fällt nicht unter diese Prüfung und erhält regulär `temperature` und gegebenenfalls `max_tokens`. Dies ist Parameterkompatibilität, kein Denkmodus-Schalter. [chat_provider.rs:769–785, 810–816]

Der OpenAI-/Fireworks-Chatparser liest den Inhalt der ersten Antwortauswahl. Bei `finish_reason: "length"` verwirft er die Antwort mit `response truncated (max_tokens)`, damit abgeschnittener Inhalt nicht als fertige Antwort durchgereicht wird. Separate Reasoning-Felder werden dort nicht als Antwort übernommen. [chat_provider.rs:1371–1414]

Es gibt zwar die Hilfsfunktion `strip_think` zum Entfernen von `<think>…</think>`-Blöcken, aber die hier beschriebenen Fireworks- und Adapter-Aufrufe wenden sie nicht automatisch an. Daraus folgt keine allgemeine Garantie, dass jeder zurückgegebene Text frei von Denktext ist. [lib.rs:501–544, 1111–1132; chat_text.rs:60–100; chat_provider.rs:1371–1414]

## 5. Hinweise für Support-Antworten

1. **Zuerst den Bauweg bestimmen.** Direkter Client und Provider-Adapter unterscheiden sich bei Modellschlüsseln, JSON-Modus, Timeout, Retries und Denkmodus.
2. **Standard nicht mit Laufzeitwert verwechseln.** Fireworks und DeepSeek V4 Flash sind Quellcode-Standards. Anfrageparameter und Konfiguration können sie überschreiben. Das Initialisierungslog des Providers nennt Anbieter und Modell; `effective_model` berücksichtigt den Anfrage-Override. [chat_provider.rs:700–710, 750–768]
3. **„Keine KI-Antwort“ ist keine fachliche Antwort.** Der Adapter liefert bei Fehlern `None`. Das Startinventar prüft den lokalen Providerbau und kann fehlende Zugänge ausweisen, führt aber keinen erfolgreichen Modellaufruf als Verfügbarkeitsprüfung durch. [chat_text.rs:89–97; chat_provider.rs:488–521]
4. **404 und 412 auseinanderhalten.** Die lokale Fehlerdeutung verweist bei 404 auf Modell oder Endpunkt, bei 402/412 auf Kontosperre oder Limit und die Anbieterabrechnung. Eine Kontosperre beweist weder einen richtigen noch einen falschen Modellnamen. [chat_provider.rs:1230–1245; lib.rs:30–42]
5. **Offen bleiben:** aktive Deployment-Werte, konkrete Verdrahtung in dl-knowledge und Concierge, äußere Anwendungszeitlimits sowie die aktuelle Erreichbarkeit und Denkmodus-Semantik des Fireworks-Modells. Es wurden keine Live-Anfragen oder Laufzeittests durchgeführt.
