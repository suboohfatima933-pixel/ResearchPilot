import json

from models.learning_content import LearningContent

from services.llm.llm_service import LLMService
from services.rag.embedding_service import EmbeddingService
from services.rag.vector_store_service import VectorStoreService


class LearningService:
    """Generates learning material from research papers."""

    def __init__(self):
        self.llm_service = LLMService()
        self.embedding_service = EmbeddingService()
        self.vector_store_service = VectorStoreService()

    def generate(
        self,
        document_id: str,
        difficulty_level: str,
    ) -> LearningContent:
        """Generate structured learning content."""

        if not document_id:
            raise ValueError(
                "Document ID is required."
            )

        if difficulty_level not in [
            "Beginner",
            "Intermediate",
            "Advanced",
        ]:
            raise ValueError(
                "Invalid difficulty level."
            )

        # Retrieve evidence from the paper
        sources = self._retrieve_sources(
            document_id=document_id,
        )

        if not sources:
            raise ValueError(
                "No relevant evidence was found "
                "in this research paper."
            )

        # Build learning context
        context = self._build_context(
            sources
        )

        # Build generation prompt
        prompt = self._build_prompt(
            context=context,
            difficulty_level=difficulty_level,
        )

        # Generate learning content
        response = self.llm_service.generate(
            prompt
        )

        # Parse and validate response
        return self._parse_response(
            response
        )

    def _retrieve_sources(
        self,
        document_id: str,
    ):
        """Retrieve representative evidence from the paper."""

        self.vector_store_service.load(
            document_id
        )

        retrieval_queries = [
            "What is the main topic and purpose of this research?",
            "What are the most important concepts in this research?",
            "What methodology or approach was used?",
            "What are the key findings and conclusions?",
            "What are the important technical details and insights?",
        ]

        sources_by_chunk = {}

        for query in retrieval_queries:

            query_embedding = (
                self.embedding_service.embed_query(
                    query
                )
            )

            results = (
                self.vector_store_service.search(
                    query_embedding,
                    document_id,
                    top_k=4,
                    min_score=0.35,
                )
            )

            for result in results:

                sources_by_chunk[
                    result.chunk_id
                ] = result

        return list(
            sources_by_chunk.values()
        )

    def _build_context(
        self,
        sources,
    ) -> str:
        """Build grounded context from retrieved evidence."""

        return "\n\n".join(
            source.content
            for source in sources
        )

    def _build_prompt(
        self,
        context: str,
        difficulty_level: str,
    ) -> str:
        """Build the learning content prompt."""

        return f"""
You are an expert research educator.

Create learning material from the provided research
paper evidence.

Learning Level:
{difficulty_level}

Source Evidence:
{context}

Your goal is to help a learner understand and remember
the research paper.

Difficulty Instructions:

Beginner:
- Use simple and clear language.
- Explain technical terms when necessary.
- Focus on fundamental understanding.

Intermediate:
- Use normal academic language.
- Explain important methodology and findings.
- Include moderate conceptual depth.

Advanced:
- Preserve important academic terminology.
- Focus on deeper concepts and critical understanding.
- Include technically challenging questions.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "simplified_explanation": "string",
    "key_concepts": [
        {{
            "concept": "string",
            "explanation": "string"
        }}
    ],
    "flashcards": [
        {{
            "question": "string",
            "answer": "string"
        }}
    ],
    "quiz_questions": [
        {{
            "question": "string",
            "options": [
                "string",
                "string",
                "string",
                "string"
            ],
            "correct_answer": "string",
            "explanation": "string"
        }}
    ]
}}

Requirements:

- Generate 5 to 8 key concepts.
- Generate 5 to 8 flashcards.
- Generate 5 quiz questions.
- Each quiz question must have exactly 4 options.
- The correct_answer must exactly match one option.
- Use only information supported by the source evidence.
- Do not invent facts.
- Return valid JSON only.
""".strip()

    def _parse_response(
        self,
        response: str,
    ) -> LearningContent:
        """Parse and validate the AI response."""

        cleaned_response = (
            response
            .strip()
            .replace(
                "```json",
                "",
            )
            .replace(
                "```",
                "",
            )
            .strip()
        )

        try:

            data = json.loads(
                cleaned_response
            )

            return LearningContent.model_validate(
                data
            )

        except (
            json.JSONDecodeError,
            ValueError,
        ) as error:

            raise ValueError(
                "The AI returned an invalid "
                "learning content response."
            ) from error