import streamlit as st
from typing import Dict
import json
from collections import Counter
import re

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.rag import GermanLearningRAG
from backend.structured_data import TranscriptStructurer
from backend.get_transcript import YouTubeTranscriptDownloader
from backend.chat import GroqChat

# Page config
st.set_page_config(
    page_title="German Learning Assistant",
    page_icon="🇩🇪",
    layout="wide"
)

# Initialize session state
if 'transcript' not in st.session_state:
    st.session_state.transcript = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'chat' not in st.session_state:
    st.session_state.chat = None
if 'rag' not in st.session_state:
    st.session_state.rag = None


def render_header():
    """Render the header section"""
    st.title("🇩🇪 German Learning Assistant")
    st.markdown("""
    Transform YouTube transcripts into interactive German learning experiences.
    
    This tool demonstrates:
    - Base LLM Capabilities
    - RAG (Retrieval Augmented Generation)
    - Groq Integration
    - Agent-based Learning Systems
    """)


def render_sidebar():
    """Render the sidebar with component selection"""
    with st.sidebar:
        st.header("Development Stages")

        # Main component selection
        selected_stage = st.radio(
            "Select Stage:",
            [
                "1. Chat with Nova",
                "2. Raw Transcript",
                "3. Structured Data",
                "4. RAG Implementation",
                "5. Interactive Learning"
            ]
        )

        # Stage descriptions
        stage_info = {
            "1. Chat with Nova": """
            **Current Focus:**
            - Basic German learning
            - Understanding LLM capabilities
            - Identifying limitations
            """,

            "2. Raw Transcript": """
            **Current Focus:**
            - YouTube transcript download
            - Raw text visualization
            - Initial data examination
            """,

            "3. Structured Data": """
            **Current Focus:**
            - Text cleaning
            - Dialogue extraction
            - Data structuring
            """,

            "4. RAG Implementation": """
            **Current Focus:**
            - Groq embeddings
            - Vector storage
            - Context retrieval
            """,

            "5. Interactive Learning": """
            **Current Focus:**
            - Scenario generation
            - Audio synthesis
            - Interactive practice
            """
        }

        st.markdown("---")
        st.markdown(stage_info[selected_stage])

        return selected_stage


def render_chat_stage():
    """Render the chat interface"""
    st.header("Chat with Nova")

    # Initialize GroqChat instance if not in session state
    if st.session_state.chat is None:
        st.session_state.chat = GroqChat()

    # Introduction text
    st.markdown("""
    Start by exploring Nova's base German language capabilities. Try asking questions about German grammar, 
    vocabulary, or cultural aspects.
    """)

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🧑‍💻" if message["role"] == "user" else "🤖"):
            st.markdown(message["content"])

    # Chat input area
    if prompt := st.chat_input("Ask about German language..."):
        # Process the user input
        process_message(prompt)

    # Example questions in sidebar
    with st.sidebar:
        st.markdown("### Try These Examples")
        example_questions = [
            "How do I say 'Where is the train station?' in German?",
            "Explain the difference between 'der', 'die', and 'das'",
            "What's the polite form of 'essen'?",
            "How do numbers and counting work in German?",
            "What's the difference between 'du' and 'Sie'?",
            "How do I ask for directions politely?"
        ]

        for q in example_questions:
            if st.button(q, use_container_width=True, type="secondary"):
                # Process the example question
                process_message(q)
                st.rerun()

    # Add a clear chat button
    if st.session_state.messages:
        if st.button("Clear Chat", type="primary"):
            st.session_state.messages = []
            st.rerun()


def process_message(message: str):
    """Process a message and generate a response"""
    # Add user message to state and display
    st.session_state.messages.append({"role": "user", "content": message})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(message)

    # Generate and display assistant's response
    with st.chat_message("assistant", avatar="🤖"):
        response = st.session_state.chat.generate_response(message)
        if response:
            st.markdown(response)
            st.session_state.messages.append(
                {"role": "assistant", "content": response})


def count_characters(text):
    """Count German and total characters in text"""
    if not text:
        return 0, 0

    def is_german(char):
        return any([
            char in 'äöüßÄÖÜ',  # German special characters
            char.isalpha(),     # Regular alphabet
            char.isnumeric()    # Numbers
        ])

    german_chars = sum(1 for char in text if is_german(char))
    return german_chars, len(text)


def render_transcript_stage():
    """Render the raw transcript stage"""
    st.header("Raw Transcript Processing")

    # URL input
    url = st.text_input(
        "YouTube URL",
        placeholder="Enter a German lesson YouTube URL"
    )

    # Download button and processing
    if url:
        if st.button("Download Transcript"):
            try:
                downloader = YouTubeTranscriptDownloader()
                transcript = downloader.get_transcript(url)
                if transcript:
                    # Store the raw transcript text in session state
                    transcript_text = "\n".join(
                        [entry['text'] for entry in transcript])
                    st.session_state.transcript = transcript_text
                    st.success("Transcript downloaded successfully!")
                else:
                    st.error("No transcript found for this video.")
            except Exception as e:
                st.error(f"Error downloading transcript: {str(e)}")

    # Display transcript and analysis if available
    if st.session_state.transcript:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Raw Transcript")

            # Display transcript with line numbers
            lines = st.session_state.transcript.split('\n')
            for i, line in enumerate(lines, 1):
                st.text(f"{i:3d} | {line}")

        with col2:
            st.subheader("Text Analysis")

            # Character count
            german_chars, total_chars = count_characters(
                st.session_state.transcript)

            # Display metrics
            metrics_col1, metrics_col2 = st.columns(2)
            metrics_col1.metric("Total Characters", total_chars)
            metrics_col2.metric("German Characters", german_chars)

            # Word frequency analysis
            st.markdown("#### Word Frequency")
            words = re.findall(r'\b\w+\b', st.session_state.transcript.lower())
            word_freq = Counter(words).most_common(10)

            # Create frequency table
            freq_data = {
                "Word": [word for word, _ in word_freq],
                "Frequency": [freq for _, freq in word_freq]
            }
            st.dataframe(freq_data, use_container_width=True)

            # Save transcript button
            if st.button("Save Transcript", type="primary"):
                try:
                    os.makedirs("backend/data/transcripts", exist_ok=True)
                    video_id = url.split("v=")[-1]
                    file_path = f"backend/data/transcripts/{video_id}.txt"

                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(st.session_state.transcript)

                    st.success(f"Transcript saved to {file_path}")
                except Exception as e:
                    st.error(f"Error saving transcript: {str(e)}")


def render_structured_stage():
    """Render the structured data stage"""
    st.header("Structured Data Processing")

    # Initialize session state for structured data
    if 'structured_data' not in st.session_state:
        st.session_state.structured_data = None
    if 'transcript_structurer' not in st.session_state:
        st.session_state.transcript_structurer = TranscriptStructurer()

    # Check if transcript is available
    if 'transcript' not in st.session_state or not st.session_state.transcript:
        st.warning("Please load a transcript in the Raw Transcript stage first.")
        return

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Transcript Analysis")

        # Process Transcript Button
        if st.button("Process Transcript"):
            with st.spinner("Processing transcript..."):
                try:
                    # Process the transcript using the structurer
                    structured_data = st.session_state.transcript_structurer.structure_transcript(
                        st.session_state.transcript
                    )
                    st.session_state.structured_data = structured_data
                    st.success("Transcript processed successfully!")
                except Exception as e:
                    st.error(f"Error processing transcript: {str(e)}")

        # Display original transcript with formatting
        st.markdown("### Original Transcript")
        transcript_text = st.session_state.transcript

        # Split transcript into parts for collapsible sections
        parts = transcript_text.split("\n\n")
        for i, part in enumerate(parts):
            with st.expander(f"Part {i+1}", expanded=(i == 0)):
                # Highlight dialogues (lines starting with - or •)
                formatted_lines = []
                for line in part.split("\n"):
                    if line.strip().startswith(("-", "•")):
                        formatted_lines.append(f"**{line}**")
                    else:
                        formatted_lines.append(line)
                st.markdown("\n".join(formatted_lines))

    with col2:
        st.subheader("Structured Data")

        if st.session_state.structured_data:
            # Create tabs for different views
            tab1, tab2 = st.columns(2)

            with tab1:
                # Display exam parts
                for part in st.session_state.structured_data.parts:
                    with st.expander(f"Part {part.part}", expanded=True):
                        st.markdown("**Introduction:**")
                        st.write(part.introduction)
                        st.markdown("**Questions:**")
                        st.write(f"Number of questions: {len(part.questions)}")

            with tab2:
                # Display questions with filtering
                if st.session_state.structured_data.parts:  # Check if we have any parts
                    part_filter = st.selectbox(
                        "Filter by Part:",
                        options=[
                            f"Part {p.part}" for p in st.session_state.structured_data.parts]
                    )

                    if part_filter:  # Only proceed if a part is selected
                        selected_part = int(part_filter.split()[-1])
                        questions = next(
                            p.questions for p in st.session_state.structured_data.parts
                            if p.part == selected_part
                        )

                        for q in questions:
                            with st.expander(f"Question {q.question_number}", expanded=False):
                                st.markdown("**Text:**")
                                st.write(q.text)

                                if q.exam_question:
                                    st.markdown("**Exam Question:**")
                                    st.write(q.exam_question)

                                if q.exam_statement:
                                    st.markdown("**Exam Statement:**")
                                    st.write(q.exam_statement)

                                if q.answers:
                                    st.markdown("**Answers:**")
                                    for a in q.answers:
                                        icon = "✓" if a.correct else " "
                                        st.write(
                                            f"{icon} {a.option}. {a.text}")

                                if q.is_true is not None:
                                    st.markdown("**True/False:**")
                                    st.write("True" if q.is_true else "False")
                else:
                    st.info("No exam parts available yet")
        else:
            st.info("Click 'Process Transcript' to see structured data")


def render_rag_stage():
    """Render the RAG implementation stage"""
    st.header("RAG System")

    # Check if structured data exists
    if 'structured_data' not in st.session_state or not st.session_state.structured_data:
        st.warning("Please process a transcript in the Structured Data stage first.")
        return

    if st.session_state.rag is None:
        with st.spinner("Initializing RAG system..."):
            st.session_state.rag = GermanLearningRAG()
            st.success("RAG system initialized successfully!")

            # Update vector store button
    if st.button("Update Vector Store"):
        with st.spinner("Updating vector store..."):
            try:
                updated = st.session_state.rag.update_vector_store()
                if updated:
                    st.success("Vector store updated successfully!")
                else:
                    st.info("Vector store is already up to date.")
            except Exception as e:
                st.error(f"Error updating vector store: {str(e)}")     

    # Query input
    query = st.text_input(
        "Search Query",
        placeholder="Ask about German vocabulary, phrases, or search for specific topics in the dialogues..."
    )

    # Only proceed if we have a query
    if query:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Retrieved Context")
            try:
                # Get similar contexts
                results = st.session_state.rag.query(query)

                if not results:
                    st.info(
                        "No relevant contexts found for your query. Try rephrasing your question or using different keywords.")
                else:
                    # Display results
                    for idx, result in enumerate(results, 1):
                        metadata = result['metadata']
                        content_type = metadata.get('content_type', '')

                        # Create a descriptive title based on content type
                        title = f"Context {idx}: "
                        if content_type == 'dialogue_or_statement':
                            title += "Dialogue"
                        elif content_type == 'exam_question':
                            title += "Question"
                        elif content_type == 'exam_statement':
                            title += "Statement"
                        elif content_type == 'instruction':
                            title += "Instructions"

                        with st.expander(title):
                            # Format content based on type
                            if content_type == 'dialogue_or_statement':
                                # Split dialogue into lines and format
                                lines = result['content'].split(' - ')
                                formatted_lines = [
                                    '- ' + line for line in lines]
                                st.markdown('\n\n'.join(formatted_lines))
                            else:
                                st.markdown(result['content'])

                            # Show part number and question number if available
                            location = f"Part {metadata['part']}"
                            if 'question_number' in metadata:
                                location += f", Question {metadata['question_number']}"
                            st.caption(location)
            except Exception as e:
                st.error(f"Error querying vector store: {str(e)}")

        with col2:
            st.subheader("Generated Response")
            if 'results' in locals() and results:
                # Generate response button
                if st.button("Generate Response", key="generate_response"):
                    with st.spinner("Generating response..."):
                        try:
                            # Prepare context for Groq
                            context = "\n\n".join(
                                [r['content'] for r in results])
                            prompt = f"""Based on the following German learning content:

{context}

Answer this question: {query}

Focus on explaining the German language concepts, vocabulary, and grammar relevant to the question. If the context contains example dialogues, use them to illustrate your points."""

                            # Initialize chat if needed
                            if st.session_state.chat is None:
                                st.session_state.chat = GroqChat()

                            # Generate and display response
                            response = st.session_state.chat.generate_response(
                                prompt)
                            if response:
                                st.markdown(response)
                            else:
                                st.error(
                                    "Failed to generate response. Please try again.")
                        except Exception as e:
                            st.error(f"Error generating response: {str(e)}")


def render_interactive_stage():
    """Render the interactive learning stage"""
    st.header("Interactive Learning")

    # Check for required data
    if 'rag' not in st.session_state or not st.session_state.rag:
        st.warning("Please initialize the RAG system in the RAG Implementation stage first.")
        return

    # Initialize session state for interactive learning
    if 'current_scenario' not in st.session_state:
        st.session_state.current_scenario = None
    if 'current_audio' not in st.session_state:
        st.session_state.current_audio = None
    if 'user_answer' not in st.session_state:
        st.session_state.user_answer = None
    if 'feedback' not in st.session_state:
        st.session_state.feedback = None
    if 'practice_scores' not in st.session_state:
        st.session_state.practice_scores = {'correct': 0, 'total': 0}

    # Topic selection
    topics = {
        "Ordering Food": "Dialogues about ordering in restaurants",
        "Travel": "Conversations about flights, trains, or directions",
        "Daily Life": "Everyday scenarios like shopping or museum visits"
    }
    selected_topic = st.selectbox("Select Practice Topic", list(topics.keys()))

    # Generate scenario button
    if st.button("Generate New Scenario"):
        st.session_state.current_scenario = None
        st.session_state.current_audio = None
        st.session_state.user_answer = None
        st.session_state.feedback = None
        # TODO: Integrate backend to generate scenario
        # Use GroqChat to create a scenario based on selected_topic and structured_data
        # Example: st.session_state.current_scenario = st.session_state.chat.generate_scenario(selected_topic, st.session_state.structured_data)
        st.session_state.current_scenario = {
            "context": f"You’re practicing {selected_topic.lower()}.",
            "dialogue": "Placeholder dialogue",
            "question": "What would you say next?",
            "options": ["Option A", "Option B", "Option C"]  # Placeholder
        }
        st.rerun()

    # Display scenario and exercise
    if st.session_state.current_scenario:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Scenario")
            st.write(
                f"**Context:** {st.session_state.current_scenario['context']}")
            st.write(
                f"**Dialogue:**\n\n{st.session_state.current_scenario['dialogue']}")

            # Audio section
            if st.session_state.current_audio:
                st.audio(st.session_state.current_audio)
            else:
                if st.button("Generate Audio"):
                    with st.spinner("Generating audio..."):
                        # TODO: Integrate backend audio synthesis
                        # Use an AudioGenerator class to create audio from scenario dialogue
                        # Example: st.session_state.current_audio = AudioGenerator().generate(st.session_state.current_scenario['dialogue'])
                        st.session_state.current_audio = "placeholder_audio.mp3"  # Placeholder
                        st.rerun()

        with col2:
            st.subheader("Practice Exercise")
            st.write(
                f"**Question:** {st.session_state.current_scenario['question']}")

            # Display options and handle answer submission
            if not st.session_state.feedback:
                answer = st.radio("Choose your answer:",
                                  st.session_state.current_scenario['options'])
                if st.button("Submit Answer"):
                    st.session_state.user_answer = answer
                    # TODO: Integrate backend feedback generation
                    # Use GroqChat to evaluate the answer against the scenario
                    # Example: st.session_state.feedback = st.session_state.chat.evaluate_answer(st.session_state.current_scenario, answer)
                    st.session_state.feedback = {
                        "correct": True, "explanation": "Placeholder feedback"}
                    st.session_state.practice_scores['total'] += 1
                    if st.session_state.feedback['correct']:
                        st.session_state.practice_scores['correct'] += 1
                    st.rerun()
            else:
                # Display feedback
                if st.session_state.feedback['correct']:
                    st.success(
                        f"Correct! {st.session_state.feedback['explanation']}")
                else:
                    st.error(
                        f"Incorrect. {st.session_state.feedback['explanation']}")
                if st.button("Try Another"):
                    st.session_state.current_scenario = None
                    st.session_state.current_audio = None
                    st.session_state.user_answer = None
                    st.session_state.feedback = None
                    st.rerun()

    # Progress tracking
    if st.session_state.practice_scores['total'] > 0:
        st.sidebar.subheader("Progress")
        accuracy = st.session_state.practice_scores['correct'] / \
            st.session_state.practice_scores['total']
        st.sidebar.write(
            f"Correct: {st.session_state.practice_scores['correct']}/{st.session_state.practice_scores['total']}")
        st.sidebar.write(f"Accuracy: {accuracy:.0%}")


def main():
    """Main application logic"""
    # Render header
    render_header()

    # Get selected stage from sidebar
    selected_stage = render_sidebar()

    # Render appropriate stage
    if selected_stage == "1. Chat with Nova":
        render_chat_stage()
    elif selected_stage == "2. Raw Transcript":
        render_transcript_stage()
    elif selected_stage == "3. Structured Data":
        render_structured_stage()
    elif selected_stage == "4. RAG Implementation":
        render_rag_stage()
    else:
        render_interactive_stage()


if __name__ == "__main__":
    main()
