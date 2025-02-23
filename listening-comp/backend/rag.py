import chromadb
import json
from pathlib import Path
from typing import List, Tuple, Dict, Any
import os
from dotenv import load_dotenv
from llm_client import groq_client

load_dotenv()

# Set tokenizer environment variable to avoid warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"

class QuestionVectorStore:
    def __init__(self, db_path: str = "./chroma_db"):
        """Initialize the vector store with ChromaDB.

        Args:
            db_path (str): Path to the ChromaDB database directory
        """
        self.client = chromadb.PersistentClient(path=db_path)
        
        # Use multilingual model better suited for German
        self.collection = self.client.get_or_create_collection(
            name="language-learning-questions",
            metadata={"description": "German language learning questions and answers"},
            embedding_function=chromadb.utils.embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="paraphrase-multilingual-mpnet-base-v2"  # Better for German language
            )
        )

    def _load_questions_from_json(self, file_path: Path) -> List[Tuple[str, Dict[str, Any]]]:
        """Load and process questions from a JSON file.

        Args:
            file_path (Path): Path to the JSON file containing questions

        Returns:
            List[Tuple[str, Dict]]: List of (document, metadata) tuples
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, dict) or 'parts' not in data:
                print(f"Warning: File {file_path} does not have the expected structure")
                return []
            
            questions = []
            for part in data['parts']:
                if not isinstance(part, dict) or 'questions' not in part:
                    print(f"Warning: Part in {file_path} does not have the expected structure")
                    continue
                
                for q in part['questions']:
                    try:
                        # Get question text
                        text = q.get('text', '')
                        if not text:
                            print(f"Warning: Question in {file_path} is missing text")
                            continue
                        
                        # Handle different question types based on part
                        if part['part'] == 2:
                            # Part 2: True/False questions use exam_statement
                            exam_question = q.get('exam_statement', '')
                            if not exam_question:
                                print(f"Warning: Part 2 question in {file_path} is missing exam_statement")
                                continue
                            correct_answer = "Richtig" if q.get('is_true', False) else "Falsch"
                        else:
                            # Parts 1 & 3: Multiple choice questions use exam_question
                            exam_question = q.get('exam_question', '')
                            if not exam_question:
                                print(f"Warning: Part {part['part']} question in {file_path} is missing exam_question")
                                continue
                            
                            # Get correct answer from multiple choice
                            answers = q.get('answers', [])
                            correct_answer = next((a['text'] for a in answers if a.get('correct', False)), None)
                            if not correct_answer:
                                print(f"Warning: Question in {file_path} is missing correct answer")
                                continue
                        
                        document = f"Context: {text}\nQuestion: {exam_question}"
                        metadata = {
                            'part': part['part'],
                            'question_number': q.get('question_number', 0),
                            'video_id': file_path.stem,
                            'correct_answer': correct_answer,
                            'is_derivative': False
                        }
                        questions.append((document, metadata))
                    except Exception as e:
                        print(f"Error processing question in {file_path}: {str(e)}")
                        continue
            
            return questions
        except Exception as e:
            print(f"Error loading file {file_path}: {str(e)}")
            return []

    def generate_derivative_questions(self, original_question: str, context: str, part: int, n_variations: int = 3) -> List[Dict[str, Any]]:
        """Generate derivative questions using Groq LLM."""
        part_instructions = {
            1: """This is for Part 1 (Teil 1) of the A1 German listening exam. 
               Each question must be based on a conversation between TWO people.
               Each question must have exactly THREE multiple choice answers (A, B, C) with only ONE correct answer.
               The conversation should be properly formatted with dashes (-) for each speaker's turn.""",
            
            2: """This is for Part 2 (Teil 2) of the A1 German listening exam.
               Each question must be based on a MONOLOGUE (one person speaking, commercial, announcement, etc.).
               Each question must be a STATEMENT that can be marked as either TRUE or FALSE.
               Do not include multiple choice answers, only provide the correct true/false value.""",
            
            3: """This is for Part 3 (Teil 3) of the A1 German listening exam.
               Each question must be based on a MONOLOGUE (one person speaking, like a voice message or announcement).
               Each question must have exactly THREE multiple choice answers (A, B, C) with only ONE correct answer.
               The text should be a single person's speech without conversation markers."""
        }

        part_instruction = part_instructions.get(part, "Invalid exam part")
        
        system_prompt = """You are a German A1 exam question generator. Your task is to create variations of existing exam questions.
        IMPORTANT: 
        1. Format your response as a single-line JSON string
        2. Each variation must be a separate object in the variations array
        3. Each variation must have exactly one text and one question field
        4. Keep all text in German and maintain A1 level difficulty
        5. Follow the example format exactly"""

        example_response = {
            1: """{"variations":[{"text":"- Guten Tag, was kostet diese Jacke? - Moment... 29,95 Euro. - Ist das mit Rabatt? - Ja, 30% günstiger.","question":"Wie viel kostet die Jacke?","answers":[{"option":"A","text":"29,95 Euro","correct":true},{"option":"B","text":"39,95 Euro","correct":false},{"option":"C","text":"19,95 Euro","correct":false}]}]}""",
            2: """{"variations":[{"text":"Achtung, eine wichtige Durchsage: Das Restaurant im ersten Stock ist heute wegen technischer Probleme geschlossen.","question":"Das Restaurant ist heute geöffnet.","is_true":false}]}""",
            3: """{"variations":[{"text":"Guten Tag, hier ist eine Nachricht für Frau Weber. Ihr Termin morgen um 14 Uhr wurde leider abgesagt.","question":"Wann ist der Termin?","answers":[{"option":"A","text":"Um 14 Uhr","correct":true},{"option":"B","text":"Um 15 Uhr","correct":false},{"option":"C","text":"Um 16 Uhr","correct":false}]}]}"""
        }

        user_prompt = f"""Generate {n_variations} variations of this German A1 listening question:

        Original Context: {context}
        Original Question: {original_question}

        {part_instruction}

        IMPORTANT: 
        1. Format your response as a single-line JSON string
        2. Each variation must be in the variations array
        3. Use this exact format (all in one line):

        {example_response[part]}"""

        try:
            completion = groq_client.client.chat.completions.create(
                model=groq_client.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=1000
            )

            response_text = completion.choices[0].message.content.strip()
            
            try:
                # Remove any whitespace and newlines from the response
                response_text = ' '.join(response_text.split())
                
                # Basic validation of JSON structure
                if not response_text.startswith('{"variations":[') or not response_text.endswith(']}'):
                    raise json.JSONDecodeError("Invalid JSON structure", response_text, 0)
                
                data = json.loads(response_text)
                variations = data["variations"]
                
                # Validate each variation
                for var in variations:
                    required_fields = {"text", "question"}
                    if part in [1, 3]:
                        required_fields.add("answers")
                    elif part == 2:
                        required_fields.add("is_true")
                        
                    if not all(field in var for field in required_fields):
                        print(f"Skipping invalid variation: {var}")
                        continue
                    
                    # Format text nicely
                    var["text"] = ' '.join(var["text"].split())
                    if part == 1:  # Add newlines for conversations
                        var["text"] = var["text"].replace(" - ", "\n- ")
                
                return variations
            except json.JSONDecodeError as e:
                print(f"Error generating variations: {str(e)}")
                print(f"Response was: {response_text}")
                return []
                
        except Exception as e:
            print(f"Error generating variations: {str(e)}")
            print(f"Response was: {completion.choices[0].message.content if 'completion' in locals() else 'No response'}")
            return []

    def add_derivative_questions(self, batch_size: int = 100) -> None:
        """Generate and add derivative questions for all existing questions in the collection.
        
        Args:
            batch_size (int): Number of questions to process in each batch
        """
        # Get all existing questions
        existing_questions = self.collection.get()
        
        all_derivatives = []
        all_derivative_metadatas = []
        all_derivative_ids = []
        
        for idx, (document, metadata) in enumerate(zip(existing_questions['documents'], existing_questions['metadatas'])):
            # Skip if it's already a derivative
            if metadata.get('is_derivative', False):
                continue
                
            # Extract context and question from document
            context = document.split('\nQuestion: ')[0].replace('Context: ', '')
            question = document.split('\nQuestion: ')[1]
            
            # Generate variations based on the part
            variations = self.generate_derivative_questions(
                question, 
                context, 
                metadata['part']
            )
            
            for var_idx, variation in enumerate(variations):
                derivative_id = f"{metadata['video_id']}_derivative_{idx}_{var_idx}"
                
                # Handle different formats based on the part
                if metadata['part'] == 2:
                    # Part 2: True/False statements
                    derivative_doc = f"Context: {variation['text']}\nQuestion: {variation['question']}"
                    correct_answer = "Richtig" if variation['is_true'] else "Falsch"
                else:
                    # Part 1 and 3: Multiple choice
                    derivative_doc = f"Context: {variation['text']}\nQuestion: {variation['question']}"
                    correct_answer = next(a['text'] for a in variation['answers'] if a['correct'])
                
                derivative_metadata = metadata.copy()
                derivative_metadata.update({
                    'is_derivative': True,
                    'original_question_id': f"{metadata['video_id']}_{metadata['part']}_{metadata['question_number']}",
                    'correct_answer': correct_answer
                })
                
                all_derivatives.append(derivative_doc)
                all_derivative_metadatas.append(derivative_metadata)
                all_derivative_ids.append(derivative_id)
        
        # Add derivatives to collection in batches
        for i in range(0, len(all_derivatives), batch_size):
            end_idx = min(i + batch_size, len(all_derivatives))
            self.collection.add(
                documents=all_derivatives[i:end_idx],
                metadatas=all_derivative_metadatas[i:end_idx],
                ids=all_derivative_ids[i:end_idx]
            )

    def load_questions_directory(self, questions_dir: str | Path, batch_size: int = 100) -> None:
        """Load all questions from a directory into the vector store.

        Args:
            questions_dir (str | Path): Path to directory containing question JSON files
            batch_size (int): Number of questions to process in each batch
        """
        questions_path = Path(questions_dir)
        all_documents = []
        all_metadatas = []
        all_ids = []

        for json_file in questions_path.glob("*.json"):
            questions = self._load_questions_from_json(json_file)
            for idx, (document, metadata) in enumerate(questions):
                doc_id = f"{metadata['video_id']}_{metadata['part']}_{metadata['question_number']}"
                all_documents.append(document)
                all_metadatas.append(metadata)
                all_ids.append(doc_id)

        # Add documents to the collection in batches
        for i in range(0, len(all_documents), batch_size):
            end_idx = min(i + batch_size, len(all_documents))
            self.collection.add(
                documents=all_documents[i:end_idx],
                metadatas=all_metadatas[i:end_idx],
                ids=all_ids[i:end_idx]
            )

    def search_similar_questions(self, query_text: str, n_results: int = 5, include_derivatives: bool = True) -> Dict[str, Any]:
        """Search for similar questions in the vector store.

        Args:
            query_text (str): The query text to search for
            n_results (int): Number of results to return
            include_derivatives (bool): Whether to include derivative questions in search

        Returns:
            Dict[str, Any]: Search results containing documents, metadata, and distances
        """
        where_filter = None if include_derivatives else {"is_derivative": False}
        
        # Get more results than needed to allow for filtering
        n_search = min(n_results * 2, 20)
        
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_search,
            where=where_filter
        )
        
        # Filter out results with very low similarity
        if results['distances'][0]:
            min_dist = min(results['distances'][0])
            max_dist = max(results['distances'][0])
            dist_range = max_dist - min_dist if max_dist != min_dist else 1
            
            # Convert distances to scores (0-1)
            scores = [(1 - (d - min_dist) / dist_range) for d in results['distances'][0]]
            
            # Keep only results with reasonable similarity
            filtered_indices = [i for i, score in enumerate(scores) if score > 0.1][:n_results]
            
            if filtered_indices:
                results['documents'] = [[results['documents'][0][i] for i in filtered_indices]]
                results['metadatas'] = [[results['metadatas'][0][i] for i in filtered_indices]]
                results['distances'] = [[1 - scores[i] for i in filtered_indices]]
            else:
                # If no good results, return empty
                results['documents'] = [[]]
                results['metadatas'] = [[]]
                results['distances'] = [[]]
        
        return results

    def get_collection_stats(self) -> Dict[str, int]:
        """Get statistics about the vector store collection.

        Returns:
            Dict[str, int]: Dictionary containing collection statistics
        """
        all_questions = self.collection.get()
        original_count = sum(1 for m in all_questions['metadatas'] if not m.get('is_derivative', False))
        derivative_count = sum(1 for m in all_questions['metadatas'] if m.get('is_derivative', False))
        
        return {
            "total_questions": len(all_questions['metadatas']),
            "original_questions": original_count,
            "derivative_questions": derivative_count
        }


def format_search_results(results: Dict[str, Any]) -> str:
    """Format search results for display.

    Args:
        results (Dict[str, Any]): Search results from vector store

    Returns:
        str: Formatted string of results
    """
    output = []
    for idx, (document, metadata, distance) in enumerate(zip(
        results['documents'][0],
        results['metadatas'][0],
        results['distances'][0]
    )):
        result = f"\nResult {idx + 1}:"
        result += f"\nDocument: {document}"
        result += f"\nVideo ID: {metadata['video_id']}"
        result += f"\nPart: {metadata['part']}"
        result += f"\nQuestion Number: {metadata['question_number']}"
        result += f"\nCorrect Answer: {metadata['correct_answer']}"
        result += f"\nIs Derivative: {metadata['is_derivative']}"
        if metadata.get('original_question_id'):
            result += f"\nOriginal Question ID: {metadata['original_question_id']}"
        result += f"\nSimilarity Score: {1 - distance:.4f}"
        output.append(result)
    return "\n".join(output)


if __name__ == "__main__":
    import time
    from pathlib import Path

    # Initialize vector store
    print("\n1. Initializing QuestionVectorStore...")
    vector_store = QuestionVectorStore()
    
    # Load original questions
    questions_dir = Path("./data/questions")
    print(f"\n2. Loading original questions from {questions_dir}...")
    vector_store.load_questions_directory(questions_dir)
    
    # Get initial stats
    initial_stats = vector_store.get_collection_stats()
    print("\n3. Initial collection statistics:")
    print(f"   Total questions: {initial_stats['total_questions']}")
    print(f"   Original questions: {initial_stats['original_questions']}")
    print(f"   Derivative questions: {initial_stats['derivative_questions']}")
    
    # Generate derivatives
    print("\n4. Generating derivative questions...")
    start_time = time.time()
    vector_store.add_derivative_questions()
    end_time = time.time()
    print(f"   Time taken: {end_time - start_time:.2f} seconds")
    
    # Get updated stats
    final_stats = vector_store.get_collection_stats()
    print("\n5. Final collection statistics:")
    print(f"   Total questions: {final_stats['total_questions']}")
    print(f"   Original questions: {final_stats['original_questions']}")
    print(f"   Derivative questions: {final_stats['derivative_questions']}")
    
    # Example searches
    print("\n6. Performing example searches...")
    
    # Search 1: Include both original and derivative questions
    print("\nSearch 1: 'Wie viel kostet' (including derivatives)")
    results = vector_store.search_similar_questions(
        "Wie viel kostet",
        n_results=3,
        include_derivatives=True
    )
    print(format_search_results(results))
    
    # Search 2: Only original questions
    print("\nSearch 2: 'Wo ist das Restaurant' (originals only)")
    results = vector_store.search_similar_questions(
        "Wo ist das Restaurant",
        n_results=2,
        include_derivatives=False
    )
    print(format_search_results(results))
    
    # Search 3: True/False questions (Part 2)
    print("\nSearch 3: 'Öffnungszeiten' (including derivatives)")
    results = vector_store.search_similar_questions(
        "Öffnungszeiten",
        n_results=2,
        include_derivatives=True
    )
    print(format_search_results(results))
    
    print("\nThe vector store is now populated with both original and derivative questions.")