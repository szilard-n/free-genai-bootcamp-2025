import streamlit as st
from backend.image_analyzer import ImageAnalyzer

def handle_go_home():
    st.session_state.current_page = "Home"

def show():
    # Check if session is active
    if not st.session_state.get('session_active', False):
        st.warning("Please select your German level first!")
        st.button("Go to Home", on_click=handle_go_home)
        return

    st.title("Image Analysis")
    
    # Create two columns
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("Upload Image")
        uploaded_file = st.file_uploader("Choose an image containing German text", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file is not None:
            # Display the uploaded image
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
            
            # Analyze button
            if st.button("Analyze"):
                with st.spinner("Analyzing image..."):
                    # Get image bytes
                    image_bytes = uploaded_file.getvalue()
                    
                    # Analyze image
                    image_analyzer = ImageAnalyzer()
                    analysis = image_analyzer.analyze_image(image_bytes)
                    
                    if analysis:
                        st.session_state.image_analysis = analysis
                    else:
                        st.error("Failed to analyze image")
    
    with col2:
        st.header("Analysis Results")
        if st.session_state.get('image_analysis'):
            analysis = st.session_state.image_analysis
            
            # Display extracted text
            with st.expander("📝 Extracted Text", expanded=True):
                for text_item in analysis["extracted_text"]:
                    st.write(f"**Text:** {text_item['text']}")
                    st.write(f"*Type:* {text_item['type']}")
                    st.write(f"*Register:* {text_item['register']}")
                    st.write("---")
            
            # Display context
            with st.expander("📍 Context", expanded=True):
                st.write(f"**Overall Description:** {analysis['context']['overall_description']}")
                st.write(f"**Type:** {analysis['context']['text_type']}")
                st.write(f"**Situation:** {analysis['context']['situation']}")
                st.write(f"**Target Audience:** {analysis['context']['target_audience']}")
            
            # Display detailed analysis
            st.subheader("📚 Detailed Analysis")
            for item in analysis["analysis"]:
                with st.expander(f"Analysis: {item['text'][:30]}..."):
                    # Text and Translation
                    st.write(f"**Original Text:** {item['text']}")
                    st.write(f"**Translation:** {item['translation']}")
                    
                    # Morphology
                    st.write("**Morphology:**")
                    st.markdown("##### Word Formation")
                    for formation in item["morphology"]["word_formation"]:
                        st.write(f"- {formation}")
                    st.markdown("##### Declensions")
                    for decl in item["morphology"]["declensions"]:
                        st.write(f"- {decl}")
                    st.markdown("##### Conjugations")
                    for conj in item["morphology"]["conjugations"]:
                        st.write(f"- {conj}")
                    
                    # Syntax
                    st.write("**Syntax:**")
                    st.write(f"*Sentence Structure:* {item['syntax']['sentence_structure']}")
                    st.write(f"*Word Order:* {item['syntax']['word_order']}")
                    st.write(f"*Clause Analysis:* {item['syntax']['clause_analysis']}")
                    
                    # Cases
                    st.write("**Cases:**")
                    for case in item["cases"]:
                        st.markdown(f"##### {case['case']}")
                        st.write(f"*Usage:* {case['usage']}")
                        st.write("*Examples:*")
                        for example in case["examples"]:
                            st.write(f"- {example}")
                    
                    # Tenses
                    st.write("**Tenses:**")
                    for tense in item["tenses"]:
                        st.markdown(f"##### {tense['tense']}")
                        st.write(f"*Usage:* {tense['usage']}")
                        st.write("*Examples:*")
                        for example in tense["examples"]:
                            st.write(f"- {example}")
                    
                    # Vocabulary
                    st.write(f"**Vocabulary Level:** {item['vocabulary_level']}")
                    st.markdown("##### Vocabulary Notes")
                    st.write("*Collocations:*")
                    for collocation in item["vocabulary_notes"]["collocations"]:
                        st.write(f"- {collocation}")
                    st.write("*Synonyms:*")
                    for synonym in item["vocabulary_notes"]["synonyms"]:
                        st.write(f"- {synonym}")
                    st.write("*Register-Specific:*")
                    for reg in item["vocabulary_notes"]["register_specific"]:
                        st.write(f"- {reg}")
                    
                    # Cultural Notes
                    st.markdown("##### Cultural Context")
                    st.write("*Cultural References:*")
                    for ref in item["cultural_notes"]["references"]:
                        st.write(f"- {ref}")
                    st.write("*Regional Aspects:*")
                    for aspect in item["cultural_notes"]["regional_aspects"]:
                        st.write(f"- {aspect}")
                    st.write("*Usage Context:*")
                    for context in item["cultural_notes"]["usage_context"]:
                        st.write(f"- {context}")
            
            # Display learning opportunities
            st.subheader("📖 Learning Opportunities")
            for opportunity in analysis["learning_opportunities"]:
                with st.expander(f"Topic: {opportunity['topic']}"):
                    st.write(f"**Explanation:** {opportunity['explanation']}")
                    
                    st.write("**Common Mistakes to Avoid:**")
                    for mistake in opportunity["common_mistakes"]:
                        st.write(f"- {mistake}")
                    
                    st.write("**Practice Suggestions:**")
                    for practice in opportunity["practice_suggestions"]:
                        st.write(f"*{practice['type']}*")
                        st.write(practice["description"])
                        st.write("Examples:")
                        for example in practice["examples"]:
                            st.write(f"- {example}")
                    
                    st.write("**Related Topics:**")
                    for topic in opportunity["related_topics"]:
                        st.write(f"- {topic}")
                    
                    st.write("**Examples and Variations:**")
                    for example in opportunity["examples"]:
                        st.write(f"Original: {example['original']}")
                        st.write("Variations:")
                        for variation in example["variations"]:
                            st.write(f"- {variation}")
                        st.write(f"*Usage Notes:* {example['usage_notes']}")
        else:
            st.info("Upload an image and click 'Analyze' to see the results here.")
