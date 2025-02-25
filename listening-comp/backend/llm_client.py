"""
Singleton module for managing LLM clients (Groq and ElevenLabs).
This ensures we only create one client instance across the application.
"""

from dataclasses import dataclass
from pathlib import Path
from groq import Groq
import os
from dotenv import load_dotenv
from elevenlabs import ElevenLabs, play
from typing import Optional, Dict, List, Union, Iterator
import hashlib
import threading

load_dotenv()


class LLMClient:
    """Manages all LLM interactions including chat and text-to-speech"""

    _instance = None
    _groq_client = None
    _groq_model = None
    _elevenlabs = None
    _female_voice_id = None
    _male_voice_id = None
    _tts_model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMClient, cls).__new__(cls)
            # Initialize Groq
            cls._groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])
            cls._groq_model = os.environ.get("LLM_MODEL_ID", "mixtral-8x7b-32768")

            # Initialize ElevenLabs
            cls._elevenlabs = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
            cls._female_voice_id = os.environ.get("ELEVENLABS_FEMALE_VOICE_ID")
            cls._male_voice_id = os.environ.get("ELEVENLABS_MALE_VOICE_ID")
            cls._tts_model = os.environ.get("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")

            # Create audio directory if it doesn't exist
            Path("backend/data/audio").mkdir(parents=True, exist_ok=True)
        return cls._instance

    def _get_audio_path(self, text: str) -> str:
        """Generate a unique filename for the audio based on the text content."""
        text_hash = hashlib.md5(text.encode()).hexdigest()
        return f"backend/data/audio/{text_hash}.mp3"

    def generate_and_play_audio(self, text: str) -> Optional[bytes]:
        """Generate audio from text and play it in a non-blocking way.

        Args:
            text: The text to convert to speech

        Returns:
            The generated audio bytes for download, or None if generation failed
        """
        try:
            # Generate new audio
            audio_iterator = self._elevenlabs.text_to_speech.convert(
                text=text,
                voice_id=self._female_voice_id,
                model_id=self._tts_model,
                output_format="mp3_44100_128",
            )

            # Collect all chunks into bytes
            audio_bytes = b''.join(list(audio_iterator))
            
            # Play audio in a separate thread to not block UI
            threading.Thread(target=lambda: play(audio_bytes), daemon=True).start()
            
            return audio_bytes

        except Exception as e:
            print(f"Error generating audio: {str(e)}")
            return None

    def download_audio(self, audio: bytes, text: str) -> Optional[str]:
        """Save audio bytes to a file for download.

        Args:
            audio: The audio bytes to save
            text: The text used to generate the audio (for filename)

        Returns:
            Path to the saved audio file, or None if saving failed
        """
        try:
            audio_path = self._get_audio_path(text)
            with open(audio_path, 'wb') as f:
                f.write(audio)
            return audio_path
        except Exception as e:
            print(f"Error saving audio: {str(e)}")
            return None

    def generate_response(
        self,
        message: Union[str, List[Dict[str, str]]],
        temperature: float = 0.1
    ) -> Optional[str]:
        """Generate a response using Groq LLM.

        Args:
            message: Either a string prompt or a list of chat messages
            temperature: Controls randomness in the response (0.0 to 1.0)

        Returns:
            The generated response text, or None if generation failed
        """
        try:
            # Convert string message to chat format if needed
            messages = (
                [{"role": "user", "content": message}]
                if isinstance(message, str)
                else message
            )

            chat_completion = self._groq_client.chat.completions.create(
                model=self._groq_model,
                messages=messages,
                temperature=temperature,
            )

            response_text = chat_completion.choices[0].message.content
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            return response_text
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return None

# Create a global instance for easy import
llm_client = LLMClient()
