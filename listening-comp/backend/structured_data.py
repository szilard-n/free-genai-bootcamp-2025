from dataclasses import dataclass
from typing import List, Optional
from llm_client import groq_client
import os
from dotenv import load_dotenv
import json

load_dotenv()


@dataclass
class Answer:
    """Represents a possible answer for multiple choice questions"""
    option: str
    text: str
    correct: bool

    def to_dict(self):
        return {
            "option": self.option,
            "text": self.text,
            "correct": self.correct
        }


@dataclass
class Question:
    """Represents a single question in the exam part"""
    question_number: int
    text: str
    exam_question: Optional[str] = None  # For parts 1 and 3
    exam_statement: Optional[str] = None  # For part 2
    answers: Optional[List[Answer]] = None  # For parts 1 and 3
    is_true: Optional[bool] = None  # For part 2

    def to_dict(self):
        result = {
            "question_number": self.question_number,
            "text": self.text
        }

        if self.exam_question is not None:
            result["exam_question"] = self.exam_question
        if self.exam_statement is not None:
            result["exam_statement"] = self.exam_statement
        if self.answers is not None:
            result["answers"] = [a.to_dict() for a in self.answers]
        if self.is_true is not None:
            result["is_true"] = self.is_true

        return result


@dataclass
class ExamPart:
    """Represents a part of the exam with its introduction and questions"""
    part: int
    introduction: str
    questions: List[Question]

    def to_dict(self):
        return {
            "part": self.part,
            "introduction": self.introduction,
            "questions": [q.to_dict() for q in self.questions]
        }


@dataclass
class Exam:
    """Represents the entire exam with all its parts"""
    parts: List[ExamPart]

    def to_dict(self):
        return {
            "parts": [p.to_dict() for p in self.parts]
        }


class TranscriptStructurer:
    """Handles structuring of A1 German listening comprehension exam data"""

    def __init__(self):
        """Initialize the transcript structurer"""
        pass

    def load_prompt(self, transcript: str) -> str:
        return f"""
        You are a German language expert. Given this German A1 listening comprehension transcript,
        extract all parts and their questions, and generate appropriate exam questions based on the content.

        Important: You can skip the examples given by the narrator and focus only on the exam questions. Examples are usually the first questions at each part starting with Beispiel.
        Important: Return ONLY valid JSON with this exact structure, nothing else:
        [
            {{
                "part": 1,
                "introduction": "Teil 1: Was ist richtig? Kreuzen Sie an A, B oder C. Sie hören jeden Text zweimal.",
                "questions": [
                    {{
                        "question_number": 1,
                        "text": "- Properly formatted conversation between two people with proper punctuation.",
                        "exam_question": "A relevant question about the conversation",
                        "answers": [
                            {{
                                "option": "A",
                                "text": "First possible answer",
                                "correct": true
                            }},
                            {{
                                "option": "B",
                                "text": "Second possible answer",
                                "correct": false
                            }},
                            {{
                                "option": "C",
                                "text": "Third possible answer",
                                "correct": false
                            }}
                        ]
                    }}
                ]
            }},
            {{
                "part": 2,
                "introduction": "Teil 2: Kreuzen Sie an richtig oder falsch. Sie hören jeden Text einmal.",
                "questions": [
                    {{
                        "question_number": 1,
                        "text": "Properly formatted monologue/announcement text",
                        "exam_statement": "A relevant statement about the announcement that can be true or false",
                        "is_true": true
                    }}
                ]
            }},
            {{
                "part": 3,
                "introduction": "Teil 3: Was ist richtig? Kreuzen Sie an A, B oder C. Sie hören jeden Text zweimal.",
                "questions": [
                    {{
                        "question_number": 1,
                        "text": "Properly formatted monologue text from one speaker",
                        "exam_question": "A relevant question about the monologue",
                        "answers": [
                            {{
                                "option": "A",
                                "text": "First possible answer",
                                "correct": true
                            }},
                            {{
                                "option": "B",
                                "text": "Second possible answer",
                                "correct": false
                            }},
                            {{
                                "option": "C",
                                "text": "Third possible answer",
                                "correct": false
                            }}
                        ]
                    }}
                ]
            }}
        ]

        Guidelines for Text Formatting:
        - Format all text with proper punctuation and make it readable
        - Remove "[Musik]" notations, applause indicators, and other non-conversational elements
        - Remove question number prefixes (e.g., "Nummer eins", "Nummer 2", etc.)
        - For conversations (Part 1), use dashes (-) to indicate different speakers
        - For monologues (Parts 2 and 3), format as a single coherent text with proper punctuation

        Guidelines for Question Generation:
        Part 1 (Conversations):
        - Create a question that tests understanding of key information from the conversation
        - Generate three plausible answers where only one is correct
        - Answers should be reasonable within the context of the conversation
        - The correct answer must be clearly derivable from the conversation

        Part 2 (True/False):
        - Create a clear statement about the announcement/monologue
        - The statement should be either clearly true or false based on the content
        - Focus on factual information from the text
        - Avoid ambiguous statements

        Part 3 (Monologues):
        - Create a question that tests understanding of the speaker's message
        - Generate three plausible answers where only one is correct
        - Answers should relate to the main point or key details of the monologue
        - The correct answer must be clearly derivable from the text

        For example:
        Instead of:
        "Nummer eins Entschuldigung was kostet dieser Pullover jetzt da steht 30% billiger einen Moment bitte 19,95 Euro ja Euro natürlich okay den nehme ich"

        Format as:
        {{
            "text": "- Entschuldigung, was kostet dieser Pullover jetzt? Da steht 30% billiger. - Einen Moment bitte. 19,95. - Euro? - Ja, Euro. Natürlich. - Okay, den nehme ich.",
            "exam_question": "Wie viel kostet der Pullover?",
            "answers": [
                {{"option": "A", "text": "19,95 Euro", "correct": true}},
                {{"option": "B", "text": "29,95 Euro", "correct": false}},
                {{"option": "C", "text": "39,95 Euro", "correct": false}}
            ]
        }}

        Transcript:
        {transcript}
        """

    def structure_transcript(self, transcript: str) -> Exam:
        """Structure a transcript into an Exam object with parts and questions."""
        try:
            completion = groq_client.client.chat.completions.create(
                model=groq_client.model,
                messages=[
                    {"role": "system", "content": "You are a German language expert that extracts structured data from transcripts. Always return valid JSON."},
                    {"role": "user", "content": self.load_prompt(transcript)}
                ],
                temperature=0.1,
                max_tokens=2000
            )

            response_text = completion.choices[0].message.content
            if "```json" in response_text:
                response_text = response_text.split(
                    "```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split(
                    "```")[1].split("```")[0].strip()

            response = json.loads(response_text)
            exam_parts = []

            for part_data in response:
                questions = []
                for q in part_data["questions"]:
                    # Create answers list if present (Parts 1 and 3)
                    answers = None
                    if "answers" in q:
                        answers = [
                            Answer(
                                option=a["option"],
                                text=a["text"],
                                correct=a["correct"]
                            ) for a in q["answers"]
                        ]

                    question = Question(
                        question_number=q["question_number"],
                        text=q["text"],
                        # Use get() to handle optional fields
                        exam_question=q.get("exam_question"),
                        exam_statement=q.get("exam_statement"),
                        answers=answers,
                        is_true=q.get("is_true")
                    )
                    questions.append(question)

                exam_part = ExamPart(
                    part=part_data["part"],
                    introduction=part_data["introduction"],
                    questions=questions
                )
                exam_parts.append(exam_part)

            return Exam(parts=exam_parts)

        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {str(e)}")
            print("Response was:", response_text)
            return Exam(parts=[])
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return Exam(parts=[])

    def save_exam_data(self, exam: Exam, path: str = "./data/questions/exam_data.json"):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(exam.to_dict(), f, indent=4, ensure_ascii=False)

    def load_transcript(self, path: str) -> str:
        return open(path, "r", encoding="utf-8").read()


if __name__ == "__main__":
    transcript_structurer = TranscriptStructurer()
    transcript = transcript_structurer.load_transcript("./data/transcripts/mLUTv35RigE.txt")
    exam = transcript_structurer.structure_transcript(transcript)
    transcript_structurer.save_exam_data(exam)
