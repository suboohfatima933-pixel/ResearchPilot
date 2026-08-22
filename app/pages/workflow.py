import streamlit as st


def render():
    """Render the Agent Workflow page."""

    st.title("🔄 Agent Workflow")

    st.caption(
        "Explore how ResearchPilot processes research "
        "papers and generates grounded AI outputs."
    )

    st.divider()

    st.subheader("🧠 Core Research Pipeline")

    workflow_steps = [
        {
            "icon": "📄",
            "title": "Document Processing",
            "description": (
                "ResearchPilot validates uploaded PDF files "
                "and extracts the research paper text."
            ),
        },
        {
            "icon": "🧩",
            "title": "Document Chunking",
            "description": (
                "Extracted research content is divided into "
                "smaller, meaningful chunks for retrieval."
            ),
        },
        {
            "icon": "🧠",
            "title": "Embedding Generation",
            "description": (
                "Each chunk is converted into a semantic "
                "vector representation using the embedding model."
            ),
        },
        {
            "icon": "🗂️",
            "title": "Vector Storage",
            "description": (
                "Document embeddings are stored in a dedicated "
                "FAISS vector store for each research paper."
            ),
        },
        {
            "icon": "🔍",
            "title": "Evidence Retrieval",
            "description": (
                "Relevant research evidence is retrieved based "
                "on the user's question or requested workflow."
            ),
        },
        {
            "icon": "🤖",
            "title": "AI Analysis",
            "description": (
                "The AI analyzes only the retrieved evidence "
                "to generate grounded responses and insights."
            ),
        },
        {
            "icon": "✨",
            "title": "Research Output",
            "description": (
                "ResearchPilot delivers structured insights, "
                "comparisons, learning content, answers, or "
                "presentations."
            ),
        },
    ]

    for index, step in enumerate(
        workflow_steps,
        start=1,
    ):

        with st.container(
            border=True,
        ):

            step_col, content_col = st.columns(
                [1, 8]
            )

            with step_col:

                st.markdown(
                    f"### {step['icon']}"
                )

                st.caption(
                    f"Step {index}"
                )

            with content_col:

                st.markdown(
                    f"#### {step['title']}"
                )

                st.write(
                    step["description"]
                )

        if index < len(workflow_steps):

            st.markdown(
                "<div style='text-align: center; "
                "font-size: 24px;'>↓</div>",
                unsafe_allow_html=True,
            )

    st.divider()

    st.subheader("⚙️ Feature Workflows")

    workflows = [
        {
            "title": "📊 Research Insights",
            "steps": [
                "Retrieve relevant evidence",
                "Build grounded research context",
                "Analyze important patterns",
                "Generate structured insights",
            ],
        },
        {
            "title": "⚖️ Compare Papers",
            "steps": [
                "Retrieve evidence from Paper A",
                "Retrieve evidence from Paper B",
                "Build combined source context",
                "Generate grounded comparison",
            ],
        },
        {
            "title": "💬 Chat with Paper",
            "steps": [
                "Receive the user's question",
                "Generate a semantic query embedding",
                "Retrieve relevant research chunks",
                "Generate a grounded answer",
            ],
        },
        {
            "title": "🎓 Learning Center",
            "steps": [
                "Retrieve relevant research evidence",
                "Build learning-focused context",
                "Generate educational explanations",
                "Create research-based learning content",
            ],
        },
        {
            "title": "📊 Presentation Generator",
            "steps": [
                "Retrieve representative research evidence",
                "Build grounded presentation context",
                "Generate structured presentation slides",
                "Validate the AI response with Pydantic",
                "Export the presentation as PowerPoint",
            ],
        },
    ]

    for workflow in workflows:

        with st.expander(
            workflow["title"]
        ):

            for step_number, step in enumerate(
                workflow["steps"],
                start=1,
            ):

                st.markdown(
                    f"**{step_number}.** {step}"
                )

    st.divider()

    st.subheader("🛡️ Grounded AI Principle")

    st.info(
        "ResearchPilot follows a retrieval-grounded workflow. "
        "The AI receives relevant evidence retrieved from the "
        "selected research paper instead of generating answers "
        "without source context."
    )