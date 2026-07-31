import streamlit as st

PAGES = {
    "🏠 Home": "home",
    "🔍 Research Discovery": "discovery",
    "📄 Paper Analysis": "analysis",
    "⚖️ Compare Papers": "compare",
    "💬 Chat with Paper": "chat",
    "🎓 Learning Center": "learning",
    "📊 Presentation Generator": "presentation",
    "🧠 Retrieval Debugger": "debugger",
    "🔄 Agent Workflow": "workflow",
    "⚙️ Settings": "settings",
}


def render_sidebar() -> str:
    with st.sidebar:
        st.title("📚 ResearchPilot")
        st.caption("Multi-Agent AI Research Copilot")

        st.divider()

        selected = st.radio(
            "Navigation",
            list(PAGES.keys()),
            label_visibility="collapsed",
        )

        st.divider()

        st.markdown("### System Status")
        st.success("UI Ready")
        st.info("AI Engine: Coming Soon")

    return PAGES[selected]