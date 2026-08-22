import streamlit as st

from services.database.document_repository import (
    DocumentRepository,
)
from services.learning.learning_service import (
    LearningService,
)


def render():
    """Render the Learning Center page."""

    st.title("🎓 Learning Center")

    st.caption(
        "Turn research papers into interactive "
        "learning material."
    )

    # Initialize services
    document_repository = DocumentRepository()
    learning_service = LearningService()

    # Load documents
    documents = document_repository.get_all()

    if not documents:

        st.info(
            "📄 No research papers are available yet. "
            "Upload and process a paper first."
        )

        return

    document_options = {
        document.document_id: document.original_filename
        for document in documents
    }

    # Learning settings
    paper_col, level_col = st.columns(2)

    with paper_col:

        selected_document_id = st.selectbox(
            "Select a research paper",
            options=list(document_options.keys()),
            format_func=lambda document_id:
                document_options[document_id],
        )

    with level_col:

        difficulty_level = st.selectbox(
            "Learning level",
            options=[
                "Beginner",
                "Intermediate",
                "Advanced",
            ],
        )

    st.divider()

    # Generate learning content
    if st.button(
        "✨ Generate Learning Material",
        type="primary",
        use_container_width=True,
    ):

        try:

            with st.spinner(
                "Creating your learning material..."
            ):

                learning_content = (
                    learning_service.generate(
                        document_id=selected_document_id,
                        difficulty_level=difficulty_level,
                    )
                )

        except (
            ValueError,
            FileNotFoundError,
        ) as error:

            st.error(str(error))

            return

        st.session_state.learning_content = (
            learning_content
        )

        st.session_state.learning_document_id = (
            selected_document_id
        )

        st.session_state.learning_difficulty = (
            difficulty_level
        )

        # Reset quiz state
        st.session_state.learning_quiz_answers = {}
        st.session_state.learning_quiz_submitted = False

        st.rerun()

    # Load generated learning content
    learning_content = st.session_state.get(
        "learning_content"
    )

    learning_document_id = st.session_state.get(
        "learning_document_id"
    )

    learning_difficulty = st.session_state.get(
        "learning_difficulty"
    )

    # Prevent showing content from another paper
    if (
        learning_content is None
        or learning_document_id
        != selected_document_id
        or learning_difficulty
        != difficulty_level
    ):
        return

    st.divider()

    # Simplified explanation
    st.subheader("📖 Understand the Paper")

    st.write(
        learning_content.simplified_explanation
    )

    st.divider()

    # Key concepts
    st.subheader("🧠 Key Concepts")

    for concept in learning_content.key_concepts:

        with st.expander(
            concept.concept
        ):

            st.write(
                concept.explanation
            )

    st.divider()

    # Flashcards
    st.subheader("🗂️ Flashcards")

    st.caption(
        "Try answering the question before "
        "revealing the answer."
    )

    for index, flashcard in enumerate(
        learning_content.flashcards,
        start=1,
    ):

        with st.expander(
            f"Flashcard {index}"
        ):

            st.markdown(
                f"**Question:** "
                f"{flashcard.question}"
            )

            show_answer = st.button(
                "Show Answer",
                key=(
                    f"flashcard_"
                    f"{selected_document_id}_"
                    f"{difficulty_level}_"
                    f"{index}"
                ),
            )

            if show_answer:

                st.success(
                    flashcard.answer
                )

    st.divider()

    # Knowledge quiz
    st.subheader("📝 Knowledge Quiz")

    st.caption(
        "Test your understanding of the paper."
    )

    quiz_answers = {}

    for index, quiz_question in enumerate(
        learning_content.quiz_questions,
        start=1,
    ):

        st.markdown(
            f"**Question {index}:** "
            f"{quiz_question.question}"
        )

        selected_answer = st.radio(
            "Choose an answer",
            options=quiz_question.options,
            key=(
                f"quiz_"
                f"{selected_document_id}_"
                f"{difficulty_level}_"
                f"{index}"
            ),
            index=None,
            label_visibility="collapsed",
        )

        quiz_answers[index] = selected_answer

        st.write("")

    # Submit quiz
    if not st.session_state.get(
        "learning_quiz_submitted",
        False,
    ):

        if st.button(
            "Submit Quiz",
            type="primary",
            use_container_width=True,
        ):

            unanswered = [
                index
                for index, answer in quiz_answers.items()
                if answer is None
            ]

            if unanswered:

                st.warning(
                    "Please answer all questions "
                    "before submitting."
                )

            else:

                st.session_state.learning_quiz_answers = (
                    quiz_answers
                )

                st.session_state.learning_quiz_submitted = True

                st.rerun()

    # Display quiz results
    if st.session_state.get(
        "learning_quiz_submitted",
        False,
    ):

        saved_answers = (
            st.session_state.learning_quiz_answers
        )

        correct_answers = 0

        for index, quiz_question in enumerate(
            learning_content.quiz_questions,
            start=1,
        ):

            user_answer = saved_answers.get(
                index
            )

            if (
                user_answer
                == quiz_question.correct_answer
            ):

                correct_answers += 1

        total_questions = len(
            learning_content.quiz_questions
        )

        score_percent = (
            correct_answers
            / total_questions
            * 100
            if total_questions
            else 0
        )

        st.divider()

        st.subheader("📊 Quiz Results")

        result_col_1, result_col_2 = st.columns(2)

        with result_col_1:

            st.metric(
                "Score",
                f"{correct_answers}/{total_questions}",
            )

        with result_col_2:

            st.metric(
                "Percentage",
                f"{score_percent:.0f}%",
            )

        st.progress(
            score_percent / 100
        )

        st.divider()

        st.subheader("📚 Answer Review")

        for index, quiz_question in enumerate(
            learning_content.quiz_questions,
            start=1,
        ):

            user_answer = saved_answers.get(
                index
            )

            is_correct = (
                user_answer
                == quiz_question.correct_answer
            )

            if is_correct:

                st.success(
                    f"Question {index}: Correct"
                )

            else:

                st.error(
                    f"Question {index}: Incorrect"
                )

                st.caption(
                    f"Correct answer: "
                    f"{quiz_question.correct_answer}"
                )

            st.write(
                quiz_question.explanation
            )

        # Retake quiz
        if st.button(
            "🔄 Retake Quiz",
            use_container_width=True,
        ):

            st.session_state.learning_quiz_answers = {}
            st.session_state.learning_quiz_submitted = False

            st.rerun()