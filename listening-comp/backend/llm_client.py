"""
Singleton module for managing the Groq LLM client.
This ensures we only create one client instance across the application.
"""

from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

class GroqClientSingleton:
    _instance = None
    _client = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GroqClientSingleton, cls).__new__(cls)
            # Initialize the Groq client
            cls._client = Groq(api_key=os.environ["GROQ_API_KEY"])
            cls._model = os.environ.get("LLM_MODEL_ID", "mixtral-8x7b-32768")
        return cls._instance

    @property
    def client(self):
        return self._client

    @property
    def model(self):
        return self._model

# Create a global instance for easy import
groq_client = GroqClientSingleton()
