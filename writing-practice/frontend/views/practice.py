import streamlit as st
from backend.sentence_operator import SentenceOperator

def handle_go_home():
    st.session_state.current_page = "Home"

def show():
    # Check if german_level is set in session state
    if not st.session_state.get('session_active', False):
        st.warning("Please start a new session from the home page first!")
        st.button("Go to Home", on_click=handle_go_home)
        return

    # Create operator instance at the start
    operator = SentenceOperator()
    
    if "sentences" not in st.session_state:
        level = st.session_state.get("level", "A1")
        st.session_state.sentences = operator.generate_sentences(level)
        st.session_state.translations = [""] * 10  # Initialize empty translations
        st.session_state.results = None  # Store evaluation results

    st.title("German Translation Practice")
    
    # Create two columns for the layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("English Sentences")
        # Create text inputs for translations
        translations = []
        for i, sentence in enumerate(st.session_state.sentences):
            st.write(f"**{i+1}. {sentence}**")
            translation = st.text_input(
                f"Translation {i+1}",
                value=st.session_state.translations[i],
                key=f"translation_{i}",
                label_visibility="collapsed"
            )
            translations.append(translation)
        
        # Update session state with current translations
        st.session_state.translations = translations
        
        # Submit button
        if st.button("Check Translations"):
            # Validate all translations are filled
            empty_translations = [i+1 for i, t in enumerate(st.session_state.translations) if not t.strip()]
            if empty_translations:
                st.error(f"Please complete all translations. Missing translations: {', '.join(map(str, empty_translations))}")
                return
                
            with st.spinner("Evaluating your translations..."):
                results = operator.check_translations(
                    st.session_state.get("level", "A1"),
                    st.session_state.sentences,
                    st.session_state.translations
                )
                st.session_state.results = results
    
    with col2:
        st.header("Results")
        if st.session_state.results:
            results = st.session_state.results
            
            # Display overall score
            st.metric("Overall Score", f"{results['score']}%")
            
            # Display individual translation results
            for translation in results["translations"]:
                with st.expander(f"Translation {translation['number']}"):
                    if not translation["mistakes"]:
                        st.success("Perfect! No mistakes.")
                    else:
                        for mistake in translation["mistakes"]:
                            st.error(f"**{mistake['type'].title()} ({mistake['subtype']}):**")
                            st.write(f"- {mistake['description']}")
                            st.write(f"- Correction: *{mistake['correction']}*")
                            st.info(f"💡 Remember: {mistake['learning_point']}")
            
            # Display conclusion
            st.subheader("Overall Feedback")
            st.write(results["conclusion"]["overall_feedback"])
            
            st.subheader("Strengths")
            for strength in results["conclusion"]["strengths"]:
                st.write(f"✅ {strength}")
            
            st.subheader("Areas to Improve")
            for area in results["conclusion"]["areas_to_improve"]:
                st.write(f"📝 {area}")
            
            st.subheader("Study Recommendations")
            for rec in results["conclusion"]["study_recommendations"]:
                with st.expander(f"📚 {rec['topic']}"):
                    st.write(f"**Why focus on this?**\n{rec['explanation']}")
                    st.write("**Examples from your translations:**")
                    for example in rec["examples"]:
                        st.write(f"- {example}")
                    st.write(f"**Practice Suggestion:**\n{rec['practice_suggestion']}")
        else:
            st.info("Submit your translations to see the results here!")
            
    # Add a reset button at the bottom
    if st.button("Start New Practice"):
        del st.session_state.sentences
        del st.session_state.translations
        st.session_state.results = None
        st.rerun()
