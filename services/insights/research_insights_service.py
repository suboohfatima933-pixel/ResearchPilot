import json
from models.research_insights import ResearchInsights

from services.llm.llm_service import LLMService
from services.rag.embedding_service import EmbeddingService
from services.rag.vector_store_service import (
    VectorStoreService,
)


class ResearchInsightsService:
    """Generates AI-powered insights from research papers."""

    def __init__(self):
        self.llm_service = LLMService()
        self.embedding_service = EmbeddingService()
        self.vector_store_service = VectorStoreService()

    def generate(
        self,
        document_id: str,
        document_name: str,
    ) -> ResearchInsights:
        """Generate structured insights for a research paper."""

        if not document_id:
            raise ValueError(
                "Document ID is required."
            )

        if not document_name:
            raise ValueError(
                "Document name is required."
            )

        # Load the document vector store
        self.vector_store_service.load(
            document_id
        )

        # Retrieve representative evidence
        sources = self._retrieve_sources(
            document_id
        )

        if not sources:
            raise ValueError(
                "No evidence was found for this paper."
            )

        # Build research context
        context = self._build_context(
            sources
        )

        # Build insight prompt
        prompt = self._build_prompt(
            document_name,
            context,
        )

        # Generate AI response
        response = self.llm_service.generate(
            prompt
        )

        # Parse structured insights
        return self._parse_response(
            document_id,
            document_name,
            response,
        )

    def _retrieve_sources(
        self,
        document_id: str,
    ):
        """Retrieve evidence covering key research areas."""

        retrieval_queries = [
            "What problem does this research address?",
            "What are the main research objectives?",
            "What methodology was used?",
            "What are the key findings?",
            "What limitations does this research have?",
            "What future research gaps are identified?",
            "What practical impact does this research have?",
        ]

        sources = []
        retrieved_chunk_ids = set()

        for query in retrieval_queries:

            query_embedding = (
                self.embedding_service.embed_query(
                    query
                )
            )

            results = self.vector_store_service.search(
                query_embedding,
                document_id,
                top_k=3,
                min_score=0.0,
            )

            for result in results:

                if result.chunk_id in retrieved_chunk_ids:
                    continue

                retrieved_chunk_ids.add(
                    result.chunk_id
                )

                sources.append(result)

        return sources

    def _build_context(
        self,
        sources,
    ) -> str:
        """Build grounded context from retrieved evidence."""

        context_parts = []

        for source in sources:

            context_parts.append(
                f"""
Chunk ID: {source.chunk_id}

Content:
{source.content}
""".strip()
            )

        return "\n\n---\n\n".join(
            context_parts
        )

    def _build_prompt(
        self,
        document_name: str,
        context: str,
    ) -> str:
        """Build the prompt for structured research insights."""

        return f"""
You are an expert research analyst.

Analyze the research paper using only the
provided source context.

Research Paper:
{document_name}

Source Context:
{context}

Return the analysis as valid JSON only.

Use exactly this structure:

{{
    "executive_summary": "",
    "research_problem": "",
    "objectives": [],
    "methodology": "",
    "key_findings": [],
    "limitations": [],
    "research_gaps": [],
    "practical_impact": "",
    "key_takeaways": []
}}

Instructions:

- Do not include markdown or code fences.
- Do not invent information.
- Use only evidence from the provided context.
- If information is not available, use an empty
  string or empty list.
- Keep the executive summary concise but meaningful.
- Extract clear and specific findings.
- Identify limitations only when supported by
  the source context.
- Identify research gaps only when supported by
  the source context.

Return valid JSON only.
""".strip()

    def _parse_response(
        self,
        document_id: str,
        document_name: str,
        response: str,
    ) -> ResearchInsights:
        """Parse the LLM JSON response into research insights."""

        try:

            data = json.loads(
                response
            )

        except json.JSONDecodeError as error:

            raise ValueError(
                "Research insights could not be parsed."
            ) from error

        return ResearchInsights(
            document_id=document_id,
            document_name=document_name,
            executive_summary=data.get(
                "executive_summary",
                "",
            ),
            research_problem=data.get(
                "research_problem",
                "",
            ),
            objectives=data.get(
                "objectives",
                [],
            ),
            methodology=data.get(
                "methodology",
                "",
            ),
            key_findings=data.get(
                "key_findings",
                [],
            ),
            limitations=data.get(
                "limitations",
                [],
            ),
            research_gaps=data.get(
                "research_gaps",
                [],
            ),
            practical_impact=data.get(
                "practical_impact",
                "",
            ),
            key_takeaways=data.get(
                "key_takeaways",
                [],
            ),
        )
    
    