import streamlit as st

# Define German levels with descriptions
GERMAN_LEVELS = {
    "A1": "Beginner - Can understand and use familiar everyday expressions",
    "A2": "Elementary - Can communicate in simple and routine tasks",
    "B1": "Intermediate - Can deal with most situations likely to arise while travelling",
    "B2": "Upper Intermediate - Can interact with a degree of fluency and spontaneity",
    "C1": "Advanced - Can express ideas fluently and spontaneously",
    "C2": "Professional - Can understand virtually everything heard or read"
}


def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    if 'german_level' not in st.session_state:
        st.session_state.german_level = None
    if 'session_active' not in st.session_state:
        st.session_state.session_active = False
    if 'start_clicked' not in st.session_state:
        st.session_state.start_clicked = False
    if 'reset_clicked' not in st.session_state:
        st.session_state.reset_clicked = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"


def handle_start():
    st.session_state.session_active = True
    st.session_state.start_clicked = True
    st.session_state.current_page = "Practice"


def handle_reset():
    st.session_state.german_level = None
    st.session_state.session_active = False
    st.session_state.reset_clicked = True


def show():
    initialize_session_state()

    st.title("Welcome to German Writing Practice")

    if st.session_state.session_active:
        st.info(f"You have an active session at level: {st.session_state.german_level}")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            st.button("Reset Session", type="primary", on_click=handle_reset)
        
        st.divider()
        st.write("Use the navigation menu on the left to switch between pages.")
        
        if st.session_state.current_page == "Practice":
            st.write("You are now in the practice page.")
        
    else:
        # Level selection section
        st.header("Select Your German Level")

        # Create two columns for better layout
        col1, col2 = st.columns([2, 1])

        with col1:
            # Level selection with descriptions using selectbox
            level_options = [""] + list(GERMAN_LEVELS.keys())
            selected_level = st.selectbox(
                "Choose your German proficiency level:",
                level_options,
                format_func=lambda x: f"{x} - {GERMAN_LEVELS[x].split(' - ')[0]}" if x else "Select a level...",
                key="level_selector"
            )
            
            if selected_level:
                st.info(GERMAN_LEVELS[selected_level].split(" - ")[1])
            
            # Store the selected level in session state
            st.session_state.german_level = selected_level

        with col2:
            st.markdown("### Start Session")
            # Only enable the start button if a level is selected
            if selected_level:
                st.button("Start Session", type="primary", on_click=handle_start)
