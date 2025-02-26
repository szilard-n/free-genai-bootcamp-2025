from backend.llm_client import LLMClient
import json
import pytesseract
from PIL import Image
import io
import re

class ImageAnalyzer:
    def __init__(self):
        self.llm_client = LLMClient()

    def extract_text_from_image(self, image_bytes):
        """
        Extract text from image using Tesseract OCR.
        
        Args:
            image_bytes (bytes): The image file in bytes
            
        Returns:
            str: Extracted text from the image
        """
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Extract text using Tesseract with German language
            text = pytesseract.image_to_string(image, lang='deu')
            return text.strip()
        except Exception as e:
            print(f"Error in OCR text extraction: {e}")
            return None

    def analyze_image(self, image_bytes):
        """
        Extract text from image using OCR and analyze it using LLM.
        
        Args:
            image_bytes (bytes): The image file in bytes
            
        Returns:
            dict: Analysis results containing extracted text and explanations
        """
        try:
            # First extract text using OCR
            extracted_text = self.extract_text_from_image(image_bytes)
            if not extracted_text:
                return {
                    "error": "Failed to extract text from image",
                    "extracted_text": [],
                    "context": {
                        "overall_description": "Error in OCR processing",
                        "text_type": "",
                        "situation": "",
                        "target_audience": ""
                    },
                    "analysis": [],
                    "learning_opportunities": []
                }
            
            messages = [
                {
                    "role": "system",
                    "content": """You are a highly knowledgeable German language teacher analyzing German text. Your task is to provide comprehensive, educational analysis of the provided German text.

For the provided German text, provide the following detailed analysis:

1. Text Assessment:
   - Analyze the type of text (article, sign, menu, etc.)
   - Identify the register (formal, informal, colloquial, etc.)

2. Linguistic Analysis for each text element:
   - Morphology:
     * Word formation (compounds, prefixes, suffixes)
     * Declension patterns
     * Conjugation patterns
   - Syntax:
     * Sentence structure analysis
     * Word order rules applied
     * Clause types and relationships
   - Cases:
     * Identify used cases (Nominativ, Akkusativ, Dativ, Genitiv)
     * Explain why each case is used
   - Tenses:
     * Identify verb tenses
     * Explain tense usage in context

3. Vocabulary and Usage:
   - CEFR level categorization (A1-C2) with explanation
   - Common collocations and phrases
   - Synonyms and alternatives
   - Register-specific vocabulary
   - Regional variations if present

4. Cultural and Pragmatic Context:
   - Cultural references and implications
   - Situational context
   - Common usage scenarios
   - Regional or dialectal features

5. Learning Focus:
   - Key grammar patterns to study
   - Common pitfalls and mistakes
   - Practice suggestions
   - Related vocabulary fields
   - Example variations for different contexts

Format your response as a structured JSON:
{
    "extracted_text": [
        {
            "text": "actual text",
            "type": "sign/menu/article/etc",
            "register": "formal/informal/colloquial"
        }
    ],
    "context": {
        "overall_description": "general context",
        "text_type": "type of document/sign",
        "situation": "usage context",
        "target_audience": "intended readers"
    },
    "analysis": [
        {
            "text": "analyzed text segment",
            "translation": "precise English translation",
            "morphology": {
                "word_formation": ["compound explanations", "prefix/suffix analysis"],
                "declensions": ["relevant patterns"],
                "conjugations": ["verb forms explained"]
            },
            "syntax": {
                "sentence_structure": "detailed explanation",
                "word_order": "rule explanation",
                "clause_analysis": "clause relationships"
            },
            "cases": [
                {
                    "case": "Nominativ/Akkusativ/etc",
                    "usage": "why this case is used",
                    "examples": ["related examples"]
                }
            ],
            "tenses": [
                {
                    "tense": "present/past/etc",
                    "usage": "why this tense is used",
                    "examples": ["related examples"]
                }
            ],
            "vocabulary_level": "CEFR level",
            "vocabulary_notes": {
                "collocations": ["common word pairs"],
                "synonyms": ["alternative words"],
                "register_specific": ["formal/informal variants"]
            },
            "cultural_notes": {
                "references": ["cultural elements explained"],
                "regional_aspects": ["dialect/regional information"],
                "usage_context": ["when/where/how used"]
            }
        }
    ],
    "learning_opportunities": [
        {
            "topic": "grammar/vocabulary/cultural aspect",
            "explanation": "detailed teaching point",
            "common_mistakes": ["typical errors to avoid"],
            "practice_suggestions": [
                {
                    "type": "exercise type",
                    "description": "how to practice",
                    "examples": ["practice examples"]
                }
            ],
            "related_topics": ["connected grammar/vocabulary points"],
            "examples": [
                {
                    "original": "example text",
                    "variations": ["different contexts/situations"],
                    "usage_notes": "when to use each variation"
                }
            ]
        }
    ]
}

Remember to:
1. Provide clear, pedagogical explanations
2. Include practical examples and variations
3. Link grammar concepts to real-world usage
4. Suggest concrete learning activities
5. Highlight cultural and contextual nuances
6. Return the analysis as a structured JSON, nothing else"""
                },
                {
                    "role": "user",
                    "content": f"Analyze this German text extracted from an image. Provide comprehensive linguistic analysis, cultural context, and learning opportunities:\n\n{extracted_text}"
                }
            ]

            response = self.llm_client.chat_completion(messages)
            if not response:
                return {}

            try:
                # Enhanced JSON response cleanup
                if "```json" in response:
                    response = response.split("```json")[1].split("```")[0].strip()
                elif "```" in response:
                    response = response.split("```")[1].split("```")[0].strip()
                
                # Attempt to parse the JSON
                try:
                    return json.loads(response)
                except json.JSONDecodeError as e:
                    print(f"Initial JSON parse failed: {e}")
                    
                    # Try a more aggressive approach - use a JSON repair library if available
                    # or implement a simple fix for the most common issues
                    
                    # Check for unescaped quotes in strings
                    # Find strings and ensure quotes are properly escaped
                    def fix_string(match):
                        s = match.group(0)
                        # Escape unescaped quotes
                        s = re.sub(r'(?<!\\)"', r'\"', s[1:-1])
                        return f'"{s}"'
                    
                    # Fix strings with potential unescaped quotes
                    response = re.sub(r'"[^"]*"', fix_string, response)
                    
                    try:
                        return json.loads(response)
                    except json.JSONDecodeError as e:
                        print(f"JSON decode error after fixes: {e}")
                        print(f"Failed to parse response: {response}")
                        return {
                            "extracted_text": [],
                            "context": {
                                "overall_description": "Error processing analysis",
                                "text_type": "",
                                "situation": "",
                                "target_audience": ""
                            },
                            "analysis": [],
                            "learning_opportunities": []
                        }
            except Exception as e:
                print(f"Error in image analysis: {e}")
                return None
        except Exception as e:
            print(f"Error in image analysis: {e}")
            return None
