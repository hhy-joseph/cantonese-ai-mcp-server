# Cantonese.ai MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An **MCP (Model Context Protocol) server** that provides tools for **text-to-speech** and **speech-to-text** conversion using the [cantonese.ai](https://cantonese.ai) API. This server is designed to be run with `mcp dev`.

---

## ✨ Features

* **Text-to-Speech Tool**: Convert Cantonese or English text into high-quality audio.
* **Speech-to-Text Tool**: Transcribe an audio file into text.
* **Modern Tooling**: Set up with `uv` for fast package management.
* **Easy Integration**: Connects with any MCP-compatible client (e.g., an LLM agent).
* **Secure**: Your `cantonese.ai` API key is handled securely as an environment variable.

---

## 🚀 Getting Started

### Prerequisites

* **Python 3.8+**
* `uv`: We recommend using `uv` for Python package management. 

### Installation

1.  **Clone the repository:**
    ```bash
    git clone 
    cd cantonese-ai-mcp-server
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    uv venv
    source .venv/bin/activate
    ```
3.  **Install the dependencies:**
    This project uses `uv` to sync dependencies from `pyproject.toml`.
    ```bash
    uv sync
    ```
4.  **Set up your API Key:**
    You'll need an API key from `cantonese.ai`. Export your API key as an environment variable. You can add this to your `.bashrc` or `.zshrc` file for persistence.
    ```bash
    export CANTONESE_AI_API_KEY="your-api-key-here"
    ```

### Running the Server

Start the MCP development server using the following command. It will watch for changes in `server.py` and automatically reload.

```bash
uv run mcp dev server.py
```

You should see an output indicating that the server has started and is available, typically at `http://127.0.0.1:6274`.

OR

### Running the Server and use in Claude Desktop

```bash
uv run server.py
```

Please view [For Server Developers](https://modelcontextprotocol.io/quickstart/server) on how to set up connection with Cladue Desktop.


### 🛠️ Using the Tools
Once the server is running, it will expose two tools.

#### Tool: `text_to_speech`
Converts a string of text into an audio file.

#### Arguments:

-`text` (string, required): The text to be converted to speech.
-`voice` (string, optional, default: "default"): The voice to use for the speech synthesis.
-`language` (string, optional, default: "cantonese"): The language of the text. Can be "cantonese" or "english".
-`output_filename` (string, required): The name of the file to save the audio to (e.g., `output.mp3`).

#### Example Invocation:

```json
{
  "tool": "text_to_speech",
  "arguments": {
    "text": "你好世界",
    "output_filename": "hello_world.mp3"
  }
}
```

#### Successful Response:

```json
{
  "success": true,
  "message": "Audio file saved as hello_world.mp3"
}
```

#### Tool: `speech_to_text`

Transcribes an audio file into text.

Arguments:

`input_filename` (string, required): The path to the local audio file to be transcribed (e.g., `audio.wav`).

#### Example Invocation:

```json
{
  "tool": "speech_to_text",
  "arguments": {
    "input_filename": "audio.wav"
  }
}
```

#### Successful Response:

The tool will return a JSON object with the transcription details from the API.

```json
{
  "success": true,
  "result": {
    "text": "你好世界",
    "confidence": 0.95,
    "language": "cantonese",
    "duration": 2.3,
    "timestamp": "2025-06-02T11:22:00Z"
  }
}
```

### 📜 License

This project is licensed under the MIT License - see the `LICENSE` file for details.