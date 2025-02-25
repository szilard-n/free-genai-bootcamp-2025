from typing import Dict, List, Optional, Tuple
import json
import random

from backend.rag import GermanLearningRAG
from backend.llm_client import llm_client


class InteractiveQuestionGenerator:
    """Handles generation of interactive German learning questions"""

    def __init__(self, rag: GermanLearningRAG):
        """Initialize the question generator.

        Args:
            rag (GermanLearningRAG): Instance of GermanLearningRAG for topic questions
        """
        self.rag = rag

    def _create_generation_prompt(self, topic: str, topic_questions: List[Dict]) -> str:
        """Create the detailed prompt for question generation.

        Args:
            topic (str): The topic to generate questions for
            topic_questions (List[Dict]): Example questions for the topic from RAG

        Returns:
            str: The formatted prompt
        """
        return f"""
        You are a highly qualified German language expert and A1 exam creator, specializing in creating engaging and educational listening comprehension exercises. Your task is to generate three distinct questions based on the topic '{topic}', following the official A1 exam format and guidelines.

        Reference Content:
        Here are some example questions from our database for this topic to understand the style and difficulty level:
        {json.dumps(topic_questions, indent=2)}

        Task Requirements:
        1. Create exactly three questions - one for each exam part
        2. Maintain consistent A1 difficulty level
        3. Focus exclusively on the '{topic}' theme
        4. Use natural, everyday German appropriate for A1 learners
        5. Ensure all dialogues and texts are properly punctuated and formatted
        6. Generate plausible and unambiguous answer options

        Specific Guidelines for Each Part:

        Part 1 - Dialogue:
        - Create a natural conversation between two people
        - Use simple, everyday language appropriate for A1 level
        - Include clear context and speaker indicators
        - Generate a question that tests key information comprehension
        - Provide three plausible answers where only one is correct
        - The correct answer must be clearly derivable from the dialogue

        Part 2 - Statement:
        - Write a clear announcement or informational text
        - Focus on factual, verifiable information
        - Create an unambiguous true/false statement
        - Avoid complex language structures
        - Ensure the truth value is clearly determinable from the text

        Part 3 - Monologue:
        - Create a single-speaker narrative
        - Use clear, structured presentation
        - Include relevant details for A1 level comprehension
        - Generate a focused question about key information
        - Provide three distinct answer options
        - Make the correct answer clearly identifiable

        Important: Return ONLY valid JSON with this exact structure, nothing else:
        {{
            "parts": [
                {{
                    "part": 1,
                    "introduction": "Teil 1: Was ist richtig? Kreuzen Sie an A, B oder C.",
                    "questions": [
                        {{
                            "question_number": 1,
                            "text": "- Properly formatted conversation between two people",
                            "topic": "{topic}",
                            "exam_question": "A relevant question about the conversation",
                            "answers": [
                                {{"option": "A", "text": "First possible answer", "correct": true}},
                                {{"option": "B", "text": "Second possible answer", "correct": false}},
                                {{"option": "C", "text": "Third possible answer", "correct": false}}
                            ]
                        }}
                    ]
                }},
                {{
                    "part": 2,
                    "introduction": "Teil 2: Kreuzen Sie an richtig oder falsch.",
                    "questions": [
                        {{
                            "question_number": 1,
                            "text": "Properly formatted monologue/announcement text",
                            "topic": "{topic}",
                            "exam_statement": "A relevant statement that can be true or false",
                            "is_true": true
                        }}
                    ]
                }},
                {{
                    "part": 3,
                    "introduction": "Teil 3: Was ist richtig? Kreuzen Sie an A, B oder C.",
                    "questions": [
                        {{
                            "question_number": 1,
                            "text": "Properly formatted monologue text from one speaker",
                            "topic": "{topic}",
                            "exam_question": "A relevant question about the monologue",
                            "answers": [
                                {{"option": "A", "text": "First possible answer", "correct": true}},
                                {{"option": "B", "text": "Second possible answer", "correct": false}},
                                {{"option": "C", "text": "Third possible answer", "correct": false}}
                            ]
                        }}
                    ]
                }}
            ]
        }}

        Guidelines for Text Formatting:
        - Use proper German punctuation and capitalization
        - For dialogues (Part 1), use dashes (-) to indicate different speakers
        - For monologues (Parts 2 and 3), format as coherent paragraphs
        - Remove any meta-information or annotations
        - Keep sentences short and clear for A1 level
        - Use appropriate spacing and line breaks for readability

        Remember: All content must be:
        1. Appropriate for A1 level learners
        2. Focused on the '{topic}' topic
        3. Natural and authentic-sounding German
        4. Clear and unambiguous
        5. Properly structured and formatted
        """

    def generate_scenario(self, topic: str) -> tuple[Optional[List[Dict]], Optional[str]]:
        """Generate an interactive learning scenario for a given topic.

        Args:
            topic (str): The topic to generate questions for

        Returns:
            tuple[Optional[List[Dict]], Optional[str]]: A tuple containing:
                - List of three scenario dictionaries or None if generation failed
                - An error message string or None if generation succeeded
        """
        try:
            # Get example questions for the topic
            topic_questions = self.rag.get_questions_by_topic(topic)

            if not topic_questions:
                return None, "No example questions found for this topic. Please try a different topic."

            # Generate questions using LLMClient
            prompt = self._create_generation_prompt(topic, topic_questions)
            response = llm_client.generate_response(prompt)

            if not response:
                return None, "Failed to generate questions. Please try again."
                    
            # Parse the generated exam
            try:
                print(f"Response from LLMClient: {response}")
                generated_exam = json.loads(response)
            except json.JSONDecodeError:
                return None, "Generated response was not in the correct format. Please try again."

            # Validate the generated exam structure
            if not isinstance(generated_exam, dict) or 'parts' not in generated_exam:
                return None, "Generated response was missing required structure. Please try again."

            try:
                scenarios = []
                
                # Process each part's question
                for part in generated_exam['parts']:
                    question = part['questions'][0]
                    
                    # Format the scenario based on the question type
                    if part['part'] in [1, 3]:  # Multiple choice questions
                        scenarios.append({
                            "context": f"You're practicing {topic.lower()}.",
                            "part": f"Teil {part['part']}",
                            "dialogue": question['text'],
                            "question": question['exam_question'],
                            "options": [answer['text'] for answer in question['answers']],
                            "correct_answer": next(i for i, a in enumerate(question['answers']) if a['correct']),
                            "answered": False,
                            "user_answer": None
                        })
                    else:  # True/False questions
                        scenarios.append({
                            "context": f"You're practicing {topic.lower()}.",
                            "part": f"Teil {part['part']}",
                            "dialogue": question['text'],
                            "question": question['exam_statement'],
                            "options": ["True", "False"],
                            "correct_answer": 0 if question['is_true'] else 1,
                            "answered": False,
                            "user_answer": None
                        })
                
                if len(scenarios) != 3:
                    return None, "Generated questions were incomplete. Expected 3 questions."
                    
                return scenarios, None
                
            except (IndexError, KeyError) as e:
                return None, f"Generated questions were incomplete. Error: {str(e)}"

        except Exception as e:
            error_msg = f"An unexpected error occurred: {str(e)}"
            print(f"Error generating scenario: {error_msg}")
            return None, error_msg
