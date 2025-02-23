# Implementation Details

## System Components

### 1. Data Structure (`structured_data.py`)
- Defines hierarchical data classes for exam content:
  - `Exam`: Contains all exam parts
  - `ExamPart`: Groups questions by part (1, 2, or 3)
  - `Question`: Individual question with context and answers
  - `Answer`: Multiple choice options (for Parts 1 and 3)

#### Transcript to Question Processing
- YouTube transcripts only contain the audio content (conversations/monologues)
- Questions and answers are not in the transcript as they're read by students during the exam
- Uses Groq LLM to:
  1. Extract relevant conversations and monologues from transcripts
  2. Generate appropriate exam questions based on the content
  3. Create plausible answer options (A, B, C) or true/false statements
  4. Ensure questions match the format for each part:
     - Part 1: Questions about two-person conversations
     - Part 2: True/false statements about announcements
     - Part 3: Questions about monologues

#### Data Validation
- Strict JSON schema enforcement
- Part-specific validation:
  - Part 1: Proper conversation formatting with speaker markers
  - Part 2: Valid true/false statements
  - Part 3: Monologue text without conversation markers
- Question numbering and metadata tracking
- Proper German A1 level language validation

### 2. Transcript Handling (`get_transcript.py`)
- Downloads YouTube video transcripts using `youtube_transcript_api`
- Features:
  - Extracts video ID from YouTube URLs
  - Downloads transcripts with language preference (German, English)
  - Saves raw transcripts to `data/transcripts/` with video ID
- Handles basic error handling for transcript downloads

### 3. LLM Client (`llm_client.py`)
- Implements a singleton pattern for managing the Groq LLM client
- Centralizes LLM configuration and access across the application:
  - API key management
  - Default model selection
  - Client instantiation
- Used by all components that need LLM capabilities:
  - Transcript structuring
  - Question generation
  - Chat interface
  - RAG system
- Ensures consistent settings and efficient resource usage

### 4. RAG System (`rag.py`)
The RAG (Retrieval-Augmented Generation) system combines vector search with LLM-based question generation:

#### Vector Store Implementation
- Uses ChromaDB for efficient similarity search
- Embeds questions using `paraphrase-multilingual-mpnet-base-v2` model
  - Chosen specifically for better German language understanding
  - Creates embeddings from both question text and context
- Stores all questions in a single collection for broader semantic matches
- Each question includes metadata:
  - Part number (1, 2, or 3)
  - Question number
  - Video ID
  - Whether it's an original or derivative question

#### Question Generation
- Uses Groq LLM to generate variations while maintaining A1 difficulty
- Part-specific formatting:
  - Part 1: Two-person conversations with multiple choice (A, B, C)
  - Part 2: Monologue statements with true/false answers
  - Part 3: Monologue questions with multiple choice (A, B, C)
- Strict validation ensures:
  - Correct JSON structure
  - Required fields per part type
  - Proper conversation markers for Part 1
  - Valid answer options for Parts 1 and 3

#### Search and Retrieval
- Semantic search across all parts for broader coverage
- Configurable similarity thresholds to ensure relevance
- Can filter results:
  - By part number if needed
  - Include/exclude derivative questions
  - Limit number of results
- Returns full context including:
  - Original conversation/monologue
  - Question text
  - Answer options
  - Similarity scores

#### Example Flow
1. User submits a query (e.g., "Wie viel kostet...")
2. System embeds query using the multilingual model
3. ChromaDB finds similar questions across all parts
4. System can generate variations based on retrieved questions
5. Each variation maintains the correct format for its part

### 5. Chat Interface (`chat.py`)
- Simple chat interface using Groq LLM
- Features:
  - Basic message-response functionality
  - Uses Groq for generating responses
  - Error handling for API calls
  - Compatible with Streamlit UI

## Data Organization

```
backend/
├── data/
│   ├── questions/    # JSON files with exam questions (one per video)
│   └── transcripts/  # Raw transcripts from YouTube (one per video)
├── rag.py           # RAG implementation with ChromaDB and Groq
├── chat.py          # Basic chat interface with Groq
├── get_transcript.py # YouTube transcript downloader
├── llm_client.py    # Singleton LLM client for Groq
└── structured_data.py # Data classes and transcript structuring
```

## Key Features
- Semantic search using multilingual embeddings for accurate question retrieval
- Automatic generation of A1-level question variations maintaining original context
- Multi-part exam structure supporting different question types and formats
- YouTube integration for transcript downloads
- Vector-based storage with ChromaDB for efficient similarity search
- Basic chat interface with Groq LLM

## How It Works
1. YouTube transcripts are downloaded and stored
2. Transcripts are processed into structured exam questions
3. Questions are embedded and stored in ChromaDB
4. RAG system generates variations and handles retrieval
5. Chat interface provides basic interaction with Groq LLM
6. Each component maintains A1 difficulty level and German language focus

## How to Run the Frontend

```sh
streamlit run frontend/main.py
```

The frontend is referecing the backend so no need to run backend separately.

## How to Run the Backend

1. Create virtual env
```sh
python -m venv .venv
source .venv/bin/activate
```

2. Install requirements
```sh
pip install -r requirements.txt
```

3. Run the backend
```sh
python backend/main.py
```