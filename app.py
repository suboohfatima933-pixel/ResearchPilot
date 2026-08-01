
import streamlit as st

from app.components.sidebar import render_sidebar

from app.pages import (
    home,
    discovery,
    analysis,
    compare,
    chat,
    learning,
    presentation,
    debugger,
    workflow,
    settings,
)

st.set_page_config(
    page_title="ResearchPilot",
    page_icon="📚",
    layout="wide",
)

if "selected_paper" not in st.session_state:
    st.session_state.selected_paper = None

if "search_query" not in st.session_state:
    st.session_state.search_query = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

page = render_sidebar()

PAGE_MAP = {
    "home": home.render,
    "discovery": discovery.render,
    "analysis": analysis.render,
    "compare": compare.render,
    "chat": chat.render,
    "learning": learning.render,
    "presentation": presentation.render,
    "debugger": debugger.render,
    "workflow": workflow.render,
    "settings": settings.render,
}

PAGE_MAP[page]()