import sys
import os

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

import streamlit as st
from views import home, practice, image

st.set_page_config(
    page_title="German Writing Practice",
    page_icon="🇩🇪",
    layout="wide",
)


def initialize_session_state():
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"


def handle_nav_change():
    st.session_state.current_page = st.session_state.nav


def sidebar():
    with st.sidebar:
        st.title("Navigation")
        # Use the session state to determine the default index
        pages = ["Home", "Practice", "Image"]
        current_index = pages.index(st.session_state.current_page)
        
        st.radio(
            "Go to",
            pages,
            index=current_index,
            key="nav",
            on_change=handle_nav_change
        )


def main():
    initialize_session_state()
    
    # Show sidebar
    sidebar()
    
    # Route to the appropriate page
    if st.session_state.current_page == "Home":
        home.show()
    elif st.session_state.current_page == "Practice":
        practice.show()
    elif st.session_state.current_page == "Image":
        image.show()


if __name__ == "__main__":
    main()
