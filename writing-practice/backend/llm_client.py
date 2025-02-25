import os
from dotenv import load_dotenv
import groq

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
            self.txt_model = os.getenv("GROQ_TXT_MODEL")
            self.img_model = os.getenv("GROQ_IMG_MODEL")
            
            if not all([self.api_key, self.txt_model, self.img_model]):
                raise ValueError("Missing required environment variables")
            
            self.client = groq.Client(api_key=self.api_key)
            LLMClient._initialized = True

    def chat_completion(self, messages):
        """
        Send a chat completion request to Groq
        
        Args:
            messages (list): List of message dictionaries with 'role' and 'content' keys
            
        Returns:
            str: The model's response text
        """
        try:
            completion = self.client.chat.completions.create(
                messages=messages,
                model=self.txt_model,
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error in chat completion: {str(e)}")
            return None

    def image_completion(self, messages):
        """
        Send an image completion request to Groq
        
        Args:
            messages (list): List of message dictionaries with 'role' and 'content' keys
                           Content should include image data in base64 format
            
        Returns:
            str: The model's response text
        """
        try:
            completion = self.client.chat.completions.create(
                messages=messages,
                model=self.img_model,
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error in image completion: {str(e)}")
            return None