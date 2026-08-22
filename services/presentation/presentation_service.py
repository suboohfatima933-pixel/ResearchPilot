import json

from models.presentation_content import (
    PresentationContent,
)

from services.llm.llm_service import LLMService
from services.rag.embedding_service import (
    EmbeddingService,
)
from services.rag.vector_store_service import (
    VectorStoreService,
)


class PresentationService:
    """Generates grounded presentations from research papers."""

    def __init__(self):
        self.llm_service = LLMService()
        self.embedding_service = EmbeddingService()
        self.vector_store_service = VectorStoreService()

    def generate(
        self,
        document_id: str,
        document_name: str,
        presentation_type: str,
        slide_count: int,
    ) -> PresentationContent:
        """Generate a presentation from a research paper."""

        if not document_id:
            raise ValueError(
                "Document ID is required."
            )

        if not document_name:
            raise ValueError(
                "Document name is required."
            )

        valid_presentation_types = [
            "Research Summary",
            "Academic Presentation",
            "Executive Summary",
            "Educational Presentation",
        ]

        if (
            presentation_type
            not in valid_presentation_types
        ):
            raise ValueError(
                "Invalid presentation type."
            )

        if slide_count < 3 or slide_count > 15:
            raise ValueError(
                "Slide count must be between "
                "3 and 15."
            )

        # Retrieve representative evidence
        sources = self._retrieve_sources(
            document_id=document_id,
        )

        if not sources:
            raise ValueError(
                "No relevant evidence was found "
                "in this research paper."
            )

        # Build grounded context
        context = self._build_context(
            sources=sources,
        )

        # Build presentation prompt
        prompt = self._build_prompt(
            document_name=document_name,
            presentation_type=presentation_type,
            slide_count=slide_count,
            context=context,
        )

        response = self.llm_service.generate(
            prompt,
            response_format=(
                PresentationContent.model_json_schema()
            ),
        )

        # Parse and validate response
        return self._parse_response(
            response=response,
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
            "What problem does this research address?",
            "What methodology or approach was used?",
            "What are the most important findings?",
            "What conclusions and implications does this research present?",
            "What limitations or future research directions are discussed?",
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
                    top_k=3,
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
        document_name: str,
        presentation_type: str,
        slide_count: int,
        context: str,
    ) -> str:
        """Build the presentation generation prompt."""

        return f"""
You are an expert research communicator and
presentation strategist.

Create a {presentation_type} based only on the
provided research paper evidence.

Research Paper:
{document_name}

Required Number of Slides:
{slide_count}

Source Evidence:
{context}

Presentation Type Instructions:

Research Summary:
- Give a balanced overview of the research.
- Cover the problem, methodology, findings,
  conclusions, and significance.

Academic Presentation:
- Use a formal academic structure.
- Clearly present research objectives, methodology,
  findings, limitations, and conclusions.

Executive Summary:
- Focus on the most important findings and implications.
- Keep the content concise and decision-focused.
- Prioritize impact over technical detail.

Educational Presentation:
- Explain the research clearly for learning purposes.
- Introduce complex concepts gradually.
- Focus on understanding and clarity.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "title": "string",
    "slides": [
        {{
            "title": "string",
            "content": [
                "string",
                "string",
                "string"
            ],
            "speaker_notes": "string"
        }}
    ]
}}

Requirements:

- Generate exactly {slide_count} slides.
- Every slide must have a clear and specific title.
- Each slide should contain 3 to 5 concise bullet points.
- Avoid repeating the same information across slides.
- Create a logical narrative from beginning to end.
- Speaker notes should provide additional context
  without simply repeating the bullet points.
- Use only information supported by the source evidence.
- Do not invent facts, statistics, or conclusions.
- If evidence for a topic is missing, do not fabricate it.
- Return valid JSON only.
""".strip()

    def _parse_response(
        self,
        response: str,
    ) -> PresentationContent:
        """Parse and validate the AI response."""

        if not response or not response.strip():
            raise ValueError(
                "The AI returned an empty presentation response."
            )

        cleaned_response = response.strip()

        if cleaned_response.startswith(
            "```json"
        ):
            cleaned_response = cleaned_response[
                len("```json"):
            ]

        elif cleaned_response.startswith(
            "```"
        ):
            cleaned_response = cleaned_response[
                len("```"):
            ]

        if cleaned_response.endswith(
            "```"
        ):
            cleaned_response = cleaned_response[
                :-len("```")
            ]

        cleaned_response = cleaned_response.strip()

        try:

            data = json.loads(
                cleaned_response
            )

        except json.JSONDecodeError as error:

            raise ValueError(
                "The AI returned invalid JSON for the "
                "presentation."
            ) from error

        try:

            return PresentationContent.model_validate(
                data
            )

        except ValueError as error:

            raise ValueError(
                "The AI response did not match the "
                "required presentation structure."
            ) from error