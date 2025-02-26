import os
from dotenv import load_dotenv
import groq
import base64

class LLMClient:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Only initialize once
        if not LLMClient._initialized:
            load_dotenv()
            
            self.api_key = os.getenv("GROQ_API_KEY")
            self.model_id = os.getenv("GROQ_MODEL_ID")
            
            if not all([self.api_key, self.model_id]):
                raise ValueError("Missing required environment variables")
            
            self.client = groq.Client(api_key=self.api_key)
            LLMClient._initialized = True

    def chat_completion(self, messages):
        """
        Send a chat completion request to the LLM API.
        
        Args:
            messages (list): List of message objects with role and content
            
        Returns:
            str: The model's response
        """
        try:
            completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model_id,
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error in chat completion: {e}")
            return None