from models.paper_comparison import PaperComparison

from services.llm.llm_service import LLMService
from services.rag.embedding_service import EmbeddingService
from services.rag.vector_store_service import VectorStoreService


class PaperComparisonService:
    """Compares two research papers using retrieved evidence."""

    def __init__(self):
        self.llm_service = LLMService()
        self.embedding_service = EmbeddingService()
        self.vector_store_service = VectorStoreService()

    def compare(
        self,
        question: str,
        paper_a_id: str,
        paper_a_name: str,
        paper_b_id: str,
        paper_b_name: str,
    ) -> PaperComparison:
        """Compare two papers using relevant retrieved content."""

        if not question.strip():
            raise ValueError("Comparison question cannot be empty.")

        # Validate paper selection
        if paper_a_id == paper_b_id:
            raise ValueError(
                "Please select two different research papers."
            )

        # Create query embedding
        query_embedding = self.embedding_service.embed_query(
            question
        )

        # Retrieve sources from paper A
        paper_a_sources = self._retrieve_sources(
            query_embedding,
            paper_a_id,
        )

        # Retrieve sources from paper B
        paper_b_sources = self._retrieve_sources(
            query_embedding,
            paper_b_id,
        )

        # Validate retrieved evidence
        if not paper_a_sources and not paper_b_sources:
            raise ValueError(
                "No relevant evidence was found in either paper."
            )        

        # Build context
        context = self._build_context(
            paper_a_name,
            paper_a_sources,
            paper_b_name,
            paper_b_sources,
        )

        # Generate comparison
        prompt = self._build_prompt(
            question,
            paper_a_name,
            paper_b_name,
            context,
        )

        answer = self.llm_service.generate(
            prompt
        )

        return PaperComparison(
            paper_a_name=paper_a_name,
            paper_b_name=paper_b_name,
            comparison_type=question,
            answer=answer,
            paper_a_sources=paper_a_sources,
            paper_b_sources=paper_b_sources,
        )

    def _retrieve_sources(
        self,
        query_embedding,
        document_id: str,
    ):
        """Retrieve relevant sources for one paper."""

        # Load the document vector store
        self.vector_store_service.load(
            document_id
        )

        return self.vector_store_service.search(
            query_embedding,
            document_id,
            top_k=5,
            min_score=0.30,
        )

    def _build_context(
        self,
        paper_a_name: str,
        paper_a_sources,
        paper_b_name: str,
        paper_b_sources,
    ) -> str:
        """Build grounded context from both papers."""

        paper_a_context = "\n\n".join(
            source.content
            for source in paper_a_sources
        )

        paper_b_context = "\n\n".join(
            source.content
            for source in paper_b_sources
        )

        return f"""
PAPER A: {paper_a_name}

{paper_a_context}

---

PAPER B: {paper_b_name}

{paper_b_context}
""".strip()

    def _build_prompt(
        self,
        question: str,
        paper_a_name: str,
        paper_b_name: str,
        context: str,
    ) -> str:
        """Build a grounded paper comparison prompt."""

        return f"""
You are an expert research assistant.

Compare the following two research papers based only on
the provided source context.

Paper A: {paper_a_name}
Paper B: {paper_b_name}

Comparison Question:
{question}

Source Context:
{context}

Instructions:

- Compare the papers directly and clearly.
- Identify important similarities and differences.
- Do not invent information not present in the source context.
- If the available context is insufficient, clearly say so.
- Use clear markdown headings and bullet points where helpful.

Comparison:
""".strip()