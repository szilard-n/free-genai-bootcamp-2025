# German Writing Practice Application

A comprehensive tool for German language learners to practice and improve their writing skills through interactive exercises and image-based text analysis.

## 🌟 Features

### 1. Personalized Learning Experience
- Select your German proficiency level (A1-C2) to receive appropriate practice exercises
- Track your progress with detailed feedback and scoring
- Get personalized study recommendations based on your performance

### 2. Translation Practice
- Practice translating English sentences to German at your selected CEFR level
- Receive detailed feedback on grammar, vocabulary, and sentence structure
- Learn from mistakes with specific corrections and learning points

### 3. Image Analysis
- Upload images containing German text (signs, menus, articles, etc.)
- Extract text using Optical Character Recognition (OCR)
- Get comprehensive linguistic analysis including:
  - Morphology (word formation, declensions, conjugations)
  - Syntax (sentence structure, word order)
  - Cases and tenses
  - Vocabulary level and notes
  - Cultural context

### 4. Learning Opportunities
- Identify patterns in your mistakes
- Receive targeted study recommendations
- Practice with example variations
- Understand cultural and contextual nuances

## 🛠️ Technologies

### Frontend
- **Streamlit**: Interactive web application framework
- **Python**: Core programming language
- **PIL/Pillow**: Image processing for the uploaded images

### Backend
- **Tesseract OCR**: Text extraction from images with German language support
- **Groq LLM API**: AI-powered language analysis and feedback
- **Python**: Server-side logic and API integration

### Infrastructure
- **Docker**: Containerization for easy deployment and consistent environments
- **Docker Compose**: Multi-container orchestration

## 🏗️ Architecture

The application follows a modular architecture with clear separation between frontend and backend components:

### Frontend (Streamlit)
- **main.py**: Entry point and navigation controller
- **views/home.py**: User session management and level selection
- **views/practice.py**: Translation practice interface
- **views/image.py**: Image upload and analysis display

### Backend (Python)
- **image_analyzer.py**: Image processing and text analysis
- **sentence_operator.py**: Sentence generation and translation evaluation
- **llm_client.py**: Interface with the Groq LLM API

## 📊 Data Flow

1. **User Session**:
   - User selects German proficiency level (A1-C2)
   - Session state is maintained throughout the application

2. **Translation Practice**:
   - System generates level-appropriate English sentences
   - User translates sentences to German
   - Backend evaluates translations and provides detailed feedback
   - Results are displayed with scores, corrections, and study recommendations

3. **Image Analysis**:
   - User uploads an image containing German text
   - Tesseract OCR extracts text from the image
   - LLM analyzes the text for linguistic features
   - Results are displayed in an organized, educational format

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose
- Groq API key

### Environment Setup
1. Clone the repository
2. Create a `.env` file with the following variables:
   ```
   GROQ_API_KEY=your_api_key_here
   GROQ_MODEL_ID=your_preferred_model_id
   ```

### Running the Application
```bash
# Build and start the application
docker-compose up

# Access the application
# Open your browser and navigate to http://localhost:8501
```

## 🔍 Project Structure

```
writing-practice/
├── .env                    # Environment variables
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
├── backend/
│   ├── __init__.py
│   ├── image_analyzer.py   # Image analysis logic
│   ├── llm_client.py       # LLM API client
│   └── sentence_operator.py # Translation practice logic
└── frontend/
    ├── __init__.py
    ├── main.py             # Application entry point
    └── views/
        ├── home.py         # Home page view
        ├── image.py        # Image analysis view
        └── practice.py     # Translation practice view
```

## 🧠 AI Integration

The application leverages AI in two key ways:

1. **Language Generation and Evaluation**:
   - Generates level-appropriate practice sentences
   - Evaluates user translations with detailed feedback
   - Provides personalized study recommendations

2. **Image Text Analysis**:
   - Extracts text from images using OCR
   - Analyzes linguistic features of the extracted text
   - Provides educational context and learning opportunities