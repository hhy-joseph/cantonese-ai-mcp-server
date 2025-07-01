import httpx
from mcp.server.fastmcp import FastMCP
import os
from pathlib import Path
import tempfile
from typing import Optional

# --- Configuration for the Cantonese-AI APIs ---
# IMPORTANT: Replace with your actual API key.
# You can set this as an environment variable named CANTONESE_AI_API_KEY
API_KEY = os.environ.get("CANTONESE_AI_API_KEY", "YOUR_API_KEY")

# Updated URLs based on the provided documentation
TTS_API_URL = "https://api.cantonese.ai/v1/tts"
SST_API_URL = "https://paid-api.cantonese.ai" # CORRECTED URL

# Create a single MCP server instance for all our Cantonese AI tools
mcp = FastMCP("cantonese-ai-tools")

@mcp.tool()
def text_to_speech(
    text: str,
    voice_id: Optional[str] = None,
    speed: Optional[float] = 1,
    pitch: Optional[int] = 0,
    output_extension: str = "mp3"
) -> str:
    """
    Converts Cantonese text to speech using the cantonese.ai API
    with full customization and saves the audio to a temporary file.

    Args:
        text: The Cantonese text to be spoken. Maximum 5000 characters.
        voice_id: Unique identifier for the voice to use.
        speed: Speech speed multiplier. Range: 0.5-3.0. Defaults to 1.0.
        pitch: Pitch adjustment in semitones. Range: -12 to +12. Defaults to 0.
        output_extension: The audio output format. Defaults to "mp3". Options: "mp3", "wav", "ogg", "flac".

    Returns:
        The file path to the saved audio file.
    """
    if API_KEY == "YOUR_API_KEY":
        return "Error: API key not set. Please set the CANTONESE_AI_API_KEY environment variable or edit the script."

    try:
        # Build the request payload according to the documentation
        payload = {
            "api_key": API_KEY,
            "text": text,
            "output_extension": output_extension,
            "should_convert_from_simplified_to_traditional":True
        }
        # Add optional parameters to the payload only if they are provided
        if voice_id is not None:
            payload["voice_id"] = voice_id
        if speed is not None:
            payload["speed"] = speed
        if pitch is not None:
            payload["pitch"] = pitch
        
        with httpx.Client(timeout=60.0) as client:
            print(f"Sending request to TTS API with payload: {payload}")
            response = client.post(TTS_API_URL, json=payload)
            response.raise_for_status()

            # Save the audio to a temporary file with the correct extension
            temp_dir = tempfile.gettempdir()
            file_name = f"cantonese_tts_output.{output_extension}"
            audio_file_path = Path(temp_dir) / file_name
            with open(audio_file_path, "wb") as f:
                f.write(response.content)

            return f"Audio successfully saved to: {audio_file_path}"

    except httpx.RequestError as e:
        return f"An error occurred while requesting from Cantonese.ai TTS API: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


@mcp.tool()
def speech_to_text(
    audio_file_path: str,
    with_timestamp: bool = False,
    with_diarization: bool = False
) -> str:
    """
    Transcribes Cantonese audio to text using the standard cantonese.ai SST API.

    Args:
        audio_file_path: The full path to the audio file (e.g., mp3, wav, m4a).
        with_timestamp: Set to true to include word-level timestamps.
        with_diarization: Set to true to enable speaker diarization.

    Returns:
        The transcribed text from the API's JSON response.
    """
    if API_KEY == "YOUR_API_KEY":
        return "Error: API key not set. Please set the CANTONESE_AI_API_KEY environment variable or edit the script."

    audio_path = Path(audio_file_path)
    if not audio_path.is_file():
        return f"Error: The audio file was not found at {audio_file_path}"

    try:
        # Prepare the multipart/form-data payload according to the new documentation
        form_data = {
            "api_key": (None, API_KEY),
            "with_timestamp": (None, str(with_timestamp).lower()),
            "with_diarization": (None, str(with_diarization).lower()),
        }

        with open(audio_path, "rb") as audio_file:
            # The audio file must be sent under the field name "data"
            files = {"data": (audio_path.name, audio_file)}
            
            with httpx.Client(timeout=120.0) as client:
                print(f"Sending request to SST API at {SST_API_URL}")
                # No separate headers needed, everything is in the multipart form
                response = client.post(SST_API_URL, data=form_data, files=files)
                response.raise_for_status()

        # The API returns a JSON object, we return it as a string for Claude to display.
        return response.text

    except httpx.RequestError as e:
        return f"An error occurred while requesting from the SST API: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


if __name__ == "__main__":
    print("Starting Cantonese AI Tools MCP Server...")
    print("Available tools: text_to_speech, speech_to_text")
    mcp.run(transport ="stdio")