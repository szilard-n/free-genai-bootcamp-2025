from backend.llm_client import LLMClient
import json

class SentenceOperator:
    def __init__(self):
        self.llm_client = LLMClient()

    def generate_sentences(self, level: str) -> list[str]:
        """
        Generate 10 English sentences that are appropriate for translation into German at the given CEFR level.
        
        Args:
            level (str): CEFR level (A1, A2, B1, B2, C1, C2)
            
        Returns:
            list[str]: List of 10 English sentences
        """
        system_prompt = """You are an experienced German language teacher and CEFR expert.
        Your role is to generate English sentences that are suitable for translation into German at specific CEFR levels.
        
        Follow these level-specific guidelines:
        - A1: Basic personal information, simple present tense, basic questions, numbers, colors, simple objects
        - A2: Daily routines, simple past tense, basic preferences, weather, shopping, directions
        - B1: Experiences, opinions, future plans, all basic tenses, simple subordinate clauses
        - B2: Abstract topics, passive voice, hypothetical situations, complex opinions
        - C1: Professional topics, idiomatic expressions, complex arguments, all tenses
        - C2: Sophisticated concepts, nuanced meanings, complex structures, academic/professional content
        
        Each level should only use grammar structures and vocabulary that would be known at that level in German."""

        user_prompt = f"""Generate exactly 10 English sentences that students should translate into German at {level} level.
        
        Critical requirements:
        1. STRICTLY stay within {level} level complexity when considering German translation
        2. Each sentence on a new line
        3. Include:
           - At least one question
           - One command/request
           - Three statements
        4. Use only structures that can be translated using {level} level German grammar
        5. Focus on practical, everyday situations
        6. Ensure sentences can be naturally translated to German
        
        Output format:
        - ONLY the 10 sentences
        - One sentence per line
        - No additional text or explanations"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = self.llm_client.chat_completion(messages)
        if not response:
            return []

        # Split response into sentences and clean them
        sentences = [s.strip() for s in response.strip().split('\n') if s.strip()]
        return sentences[:10]  # Ensure we return at most 10 sentences

    def check_translations(self, level: str, english_sentences: list[str], german_translations: list[str]) -> dict:
        """
        Check the correctness of German translations and provide detailed feedback.
        
        Args:
            level (str): CEFR level (A1, A2, B1, B2, C1, C2)
            english_sentences (list[str]): Original English sentences
            german_translations (list[str]): Student's German translations
            
        Returns:
            dict: Evaluation results with score, mistakes, and recommendations
        """
        if len(english_sentences) != len(german_translations):
            raise ValueError("Number of English sentences and German translations must match")

        # Prepare the sentences for evaluation
        translation_pairs = []
        for i, (eng, ger) in enumerate(zip(english_sentences, german_translations), 1):
            translation_pairs.append(f"{i}. English: {eng}\n   German: {ger}")

        system_prompt = """You are a strict but fair German language teacher evaluating a student's translation test.
        
        Evaluation Criteria:
        1. Grammar (40% of score):
           - Verb conjugation and placement
           - Article usage and case (Nominative, Accusative, Dative, Genitive)
           - Adjective endings
           - Word order rules
           - Tense usage appropriate for level
        
        2. Vocabulary (30% of score):
           - Word choice accuracy
           - Level-appropriate vocabulary
           - Idiomatic expressions (if applicable to level)
           - Preposition usage
           - Articles with nouns (der/die/das)
        
        3. Sentence Structure (30% of score):
           - Natural German word order
           - Proper subordinate clause structure
           - Comma usage
           - Question formation
           - Command formation
        
        Level-Specific Focus:
        - A1: Basic word order, present tense, articles, simple questions
        - A2: Past tense, modal verbs, connecting words, separable verbs
        - B1: All basic tenses, subordinate clauses, relative pronouns
        - B2: Passive voice, subjunctive, complex clauses
        - C1: Advanced structures, nuanced expressions, all tenses
        - C2: Sophisticated style, complex academic language
        
        CRITICAL: Your response must be ONLY valid JSON, with NO additional text before or after.
        
        JSON Structure:
        {
            "score": <0-100>,
            "translations": [
                {
                    "number": 1,
                    "mistakes": [] or [
                        {
                            "type": "grammar/vocabulary/structure",
                            "subtype": "verb-conjugation/article/word-order/etc",
                            "description": "detailed explanation",
                            "correction": "correct form",
                            "learning_point": "rule or tip to remember"
                        }
                    ]
                }
            ],
            "conclusion": {
                "overall_feedback": "detailed assessment of performance",
                "strengths": ["specific strong points with examples"],
                "areas_to_improve": ["specific weak points with examples"],
                "study_recommendations": [
                    {
                        "topic": "grammar point/vocabulary area",
                        "explanation": "why this needs attention",
                        "examples": ["examples from the test"],
                        "practice_suggestion": "specific exercise or study method"
                    }
                ]
            }
        }"""

        user_prompt = f"""Evaluate these {level} level translations according to CEFR standards:

{chr(10).join(translation_pairs)}

Important:
1. Evaluate strictly according to {level} level CEFR standards
2. Be specific about each type of mistake
3. Provide clear corrections and learning points
4. Consider partial credit for answers that are understandable but not perfect
5. In the conclusion, focus on patterns of mistakes rather than individual errors
6. Provide actionable study recommendations with specific examples from the test
7. Consider both accuracy and naturalness of expression

Provide the evaluation in the specified JSON format."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = self.llm_client.chat_completion(messages)
        if not response:
            print("No response from LLM")
            return {}

        try:
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()

            return json.loads(response)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Failed to parse response: {response}")
            return {
                "score": 0,
                "translations": [],
                "conclusion": {
                    "overall_feedback": "Error processing evaluation",
                    "strengths": [],
                    "areas_to_improve": [],
                    "study_recommendations": []
                }
            }