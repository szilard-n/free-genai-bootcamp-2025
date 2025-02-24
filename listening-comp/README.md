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
The RAG (Retrieval-Augmented Generation) system provides semantic search over German learning content:

#### Vector Store Implementation
- Uses ChromaDB with persistent storage in `backend/data/vector_store`
- Embeds content using `paraphrase-multilingual-mpnet-base-v2` model
  - Optimized for multilingual understanding, especially German
  - Creates embeddings from dialogues, statements, and questions
- Stores content with type-based classification:
  - `dialogue_or_statement`: Actual conversations and announcements
  - `exam_question`: Questions about the content
  - `exam_statement`: True/false statements
  - `instruction`: Setup and contextual information

#### Content Organization
- Each document is stored with metadata:
  - `content_type`: Identifies the type of content
  - `type`: More specific categorization (content, question, statement)
  - `part`: Which exam part it belongs to
  - `question_number`: Reference to original question

#### Search and Retrieval
- Prioritizes finding relevant dialogues and statements
- Uses normalized distance-based scoring for better relevance:
  - Scores normalized relative to the result set
  - Higher scores indicate better matches
- Configurable parameters:
  - `max_results`: Maximum number of results to return
  - `similarity_threshold`: Minimum relevance score
- Returns full context including:
  - Content text
  - Metadata
  - Relevance scores

#### Vector Store Management
- Automatic updates when source data changes
- Clean recreation of collections to ensure consistency
- Maintains last update timestamp to prevent unnecessary updates

#### Example Usage
1. User submits a query (e.g., "ordering food in German")
2. System finds semantically similar dialogues
3. Returns relevant conversations prioritizing actual dialogue content
4. Scores indicate how well each result matches the query

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
- Automatic generation of question variations maintaining original context
- Multi-part exam structure supporting different question types and formats
- YouTube integration for transcript downloads
- Vector-based storage with ChromaDB for efficient similarity search
- Basic chat interface with Groq LLM

## How It Works

1. **Content Processing**
   - YouTube transcripts are downloaded and processed
   - Content is structured into dialogues, statements, and questions
   - Each piece of content is tagged with appropriate metadata (type, part, etc.)

2. **Vector Storage**
   - Content is embedded using a multilingual model optimized for German
   - Embeddings are stored in ChromaDB for efficient retrieval
   - Metadata enables filtering by content type and other attributes

3. **Semantic Search**
   - Users can search for specific topics or scenarios in German
   - System finds semantically similar content using vector similarity
   - Results are ranked by relevance using normalized distance scores
   - Prioritizes actual dialogues and statements over exam questions

4. **Interactive Features** (Coming Soon)
   - Question generation from dialogues
   - Interactive practice sessions
   - Real-time feedback on responses
   - Progress tracking and difficulty adjustment

## How to Run It
1. Create virtual env
```sh
python -m venv .venv
source .venv/bin/activate
```

2. Install requirements
```sh
pip install -r requirements.txt
```

3. Run the frontend
```sh
streamlit run frontend/main.py
```