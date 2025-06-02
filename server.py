# cantonese_ai_mcp_server/server.py

import os
import requests
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

# Initialize the FastMCP server
mcp = FastMCP("CantoneseAIServer")

# --- Pydantic Models for Tool Input ---

class TextToSpeechInput(BaseModel):
    """
    Input model for the text_to_speech tool.
    Defines the expected arguments and their types.
    """
    text: str = Field(..., description="The text to be converted to speech.")
    voice: str = Field("default", description="The voice to use for the speech synthesis.")
    language: str = Field("cantonese", description="The language of the text. Can be 'cantonese' or 'english'.")
    output_filename: str = Field(..., description="The name of the file to save the audio to (e.g., 'output.mp3').")

class SpeechToTextInput(BaseModel):
    """
    Input model for the speech_to_text tool.
    """
    input_filename: str = Field(..., description="The path to the local audio file to be transcribed (e.g., 'audio.wav').")


# --- Tool Definitions ---

@mcp.tool()
def text_to_speech(input: TextToSpeechInput) -> dict:
    """
    Converts a string of text into an audio file using the cantonese.ai API.
    """
    api_key = os.getenv("CANTONESE_AI_API_KEY")
    if not api_key:
        return {
            "success": False,
            "error": "CANTONESE_AI_API_KEY environment variable not set."
        }

    base_url = "https://api.cantonese.ai/v1"
    endpoint = f"{base_url}/text-to-speech"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "text": input.text,
        "voice": input.voice,
        "language": input.language,
        "format": "mp3"
    }

    try:
        response = requests.post(endpoint, headers=headers, json=data)

        if response.status_code == 200:
            with open(input.output_filename, "wb") as f:
                f.write(response.content)
            return {
                "success": True,
                "message": f"Audio file saved as {input.output_filename}"
            }
        else:
            return {
                "success": False,
                "error": f"API Error: {response.status_code} - {response.text}"
            }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Request failed: {e}"
        }

@mcp.tool()
def speech_to_text(input: SpeechToTextInput) -> dict:
    """
    Transcribes an audio file into text using the cantonese.ai API.
    """
    api_key = os.getenv("CANTONESE_AI_API_KEY")
    if not api_key:
        return {
            "success": False,
            "error": "CANTONESE_AI_API_KEY environment variable not set."
        }

    if not os.path.exists(input.input_filename):
        return {
            "success": False,
            "error": f"File not found at path: {input.input_filename}"
        }

    base_url = "https://api.cantonese.ai/v1"
    endpoint = f"{base_url}/speech-to-text"
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        with open(input.input_filename, "rb") as f:
            files = {"audio": f}
            response = requests.post(endpoint, headers=headers, files=files)

        if response.status_code == 200:
            return {
                "success": True,
                "result": response.json()
            }
        else:
            return {
                "success": False,
                "error": f"API Error: {response.status_code} - {response.text}"
            }
    except FileNotFoundError:
        return {
            "success": False,
            "error": f"File not found at path: {input.input_filename}"
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Request failed: {e}"
        }
# Run the server
if __name__ == "__main__":
    # stdio transport is used for local testing
    mcp.run(transport='stdio')