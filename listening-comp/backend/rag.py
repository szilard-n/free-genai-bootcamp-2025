import chromadb
import json
import os
from typing import List, Dict
from chromadb.utils import embedding_functions


class GermanLearningRAG:
    def __init__(self, persist_directory: str = "backend/data/vector_store"):
        """Initialize the RAG system with ChromaDB using multilingual embeddings"""
        self.persist_directory = persist_directory
        self.collection_name = "german_learning"
        self.structured_data_path = "backend/data/questions/structured_data.json"

        # Check if structured data exists
        if not os.path.exists(self.structured_data_path):
            raise FileNotFoundError(f"Structured data file not found at {self.structured_data_path}")

        # Create persist directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)

        # Initialize embedding function with multilingual model
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
        )

        # Initialize ChromaDB client with persistence
        self.client = chromadb.PersistentClient(path=persist_directory)

        # Load structured data
        data = self._load_structured_data()
        documents, metadatas, ids = self._prepare_documents(data)

        # Check if collection exists first
        collection_exists = False
        try:
            self.collection = self.client.get_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function
            )
            collection_exists = True
        except Exception:
            pass

        # Create new collection or update existing one
        if collection_exists:
            # Check if we need to update existing collection
            if len(self.collection.get()['ids']) != len(ids):
                self.collection.delete()
                self.collection = self.client.create_collection(
                    name=self.collection_name,
                    embedding_function=self.embedding_function
                )
                self.collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
        else:
            # Collection doesn't exist, create it and add data
            self.collection = self.client.create_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function
            )
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )

    def _load_structured_data(self) -> Dict:
        """Load the structured data from JSON file"""
        with open(self.structured_data_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _get_last_modified_time(self) -> float:
        """Get the last modified time of the structured data file"""
        return os.path.getmtime(self.structured_data_path)

    def _prepare_documents(self, data: Dict) -> tuple[List[str], List[Dict], List[str]]:
        """Prepare documents for vector storage from structured data"""
        documents = []
        metadatas = []
        ids = []

        for part in data['parts']:
            part_num = part['part']
            intro = part['introduction']

            # Add part introduction
            documents.append(intro)
            metadatas.append({
                'type': 'introduction',
                'part': part_num,
                'content_type': 'instruction'
            })
            ids.append(f"part_{part_num}_intro")

            # Add questions and their context
            for q in part['questions']:
                q_num = q['question_number']

                # Add the dialogue/text content
                documents.append(q['text'])
                metadatas.append({
                    'type': 'content',
                    'part': part_num,
                    'question_number': q_num,
                    'content_type': 'dialogue_or_statement'
                })
                ids.append(f"part_{part_num}_q{q_num}_content")

                # Handle different question types based on part number
                if part_num in [1, 3]:  # Parts 1 and 3: Multiple choice questions
                    # Add the exam question
                    documents.append(q['exam_question'])
                    metadatas.append({
                        'type': 'question',
                        'part': part_num,
                        'question_number': q_num,
                        'content_type': 'exam_question'
                    })
                    ids.append(f"part_{part_num}_q{q_num}_question")

                else:  # Part 2: True/False statements
                    # Add the exam statement
                    documents.append(q['exam_statement'])
                    metadatas.append({
                        'type': 'statement',
                        'part': part_num,
                        'question_number': q_num,
                        'content_type': 'exam_statement'
                    })
                    ids.append(f"part_{part_num}_q{q_num}_statement")

        return documents, metadatas, ids

    def update_vector_store(self) -> bool:
        """Update the vector store if the structured data has changed"""
        try:
            # Check if we need to update
            last_modified = self._get_last_modified_time()
            collection_count = self.collection.count()

            # If collection is empty or data file is newer, update
            if collection_count == 0 or not hasattr(self, '_last_update') or last_modified > self._last_update:
                print(f"Updating vector store. Collection count: {collection_count}, Last modified: {last_modified}")
                data = self._load_structured_data()
                documents, metadatas, ids = self._prepare_documents(data)

                # Delete existing collection and create new one
                if collection_count > 0:
                    self.client.delete_collection(name=self.collection_name)
                    self.collection = self.client.create_collection(
                        name=self.collection_name,
                        embedding_function=self.embedding_function
                    )

                # Add new data
                print(f"Adding {len(documents)} documents to vector store")
                self.collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )

                self._last_update = last_modified
                return True

            return False
        except Exception as e:
            print(f"Error updating vector store: {str(e)}")
            raise

    def query(self, query_text: str, max_results: int = 3, similarity_threshold: float = 0.1) -> List[Dict]:
        try:
            where = {"content_type": "dialogue_or_statement"}
            results = self.collection.query(
                query_texts=[query_text],
                n_results=10,
                where=where,
                include=['documents', 'metadatas', 'distances']
            )
            
            formatted_results = []
            if results['documents'] and results['documents'][0]:
                # Use raw distances for scoring - smaller distance = better match
                distances = results['distances'][0]
                max_dist = max(distances)
                
                for doc, meta, dist in zip(results['documents'][0], results['metadatas'][0], distances):
                    # Simple normalized score - closer to 1 = better match
                    score = 1 - (dist / max_dist)
                    formatted_results.append({
                        'content': doc,
                        'metadata': meta,
                        'score': score,
                        'raw_distance': dist
                    })
                    print(f"Distance: {dist:.3f}, Score: {score:.3f}, Content: {doc[:50]}...")
            
            # Sort by score (higher is better)
            formatted_results.sort(key=lambda x: x['score'], reverse=True)
            print(f"\nReturning {len(formatted_results[:max_results])} results")
            return formatted_results[:max_results]
            
        except Exception as e:
            print(f"Error querying vector store: {str(e)}")
            raise
