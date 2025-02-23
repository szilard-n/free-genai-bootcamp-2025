import os
from typing import Optional
import streamlit as st
from llm_client import groq_client

class GroqChat:
    """Simple chat interface using Groq LLM"""

    def __init__(self):
        """Initialize the chat interface"""
        pass

    def generate_response(self, message: str) -> Optional[str]:
        """Generate a response to a user message.

        Args:
            message (str): The user's message

        Returns:
            Optional[str]: The generated response, or None if an error occurred
        """
        try:
            chat_completion = groq_client.client.chat.completions.create(
                model=groq_client.model,
                messages=[{"role": "user", "content": message}],
                temperature=0.1,
                max_tokens=1000
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return None


if __name__ == "__main__":
    chat = GroqChat()
    while True:
        user_input = input("You: ")
        if user_input.lower() == '/exit':
            break
        response = chat.generate_response(user_input)
        print("Bot:", response)
