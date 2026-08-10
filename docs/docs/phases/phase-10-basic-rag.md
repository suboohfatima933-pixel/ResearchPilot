# Phase 10 – Basic RAG

## Objective

Implement a basic Retrieval-Augmented Generation (RAG) pipeline that uses
retrieved document chunks as context for an LLM-generated answer.

The goal is to ensure that answers are grounded in the uploaded research
paper rather than relying on the model's general knowledge.

---

## What Was Built

- Ollama LLM integration
- Centralized LLM model configuration
- LLMService
- RAGService
- Query embedding
- Semantic retrieval
- Context construction
- Grounded prompt generation
- LLM-generated answers
- Retrieved source display
- Relevance threshold protection

---

## Files Added

- services/llm/llm_service.py
- services/rag/rag_service.py

---

## Files Modified

- config/settings.py
- app/pages/analysis.py
- services/rag/embedding_service.py
- services/rag/vector_store_service.py
- models/search_result.py

---

## Configuration

The LLM model is configured through environment variables.

Example:

```env
OLLAMA_MODEL=gpt-oss:120b-cloud
```

The model name is not hardcoded inside the application.

This allows the LLM to be changed without modifying the service implementation.

---

## LLM Architecture

ResearchPilot uses Ollama as the LLM provider.

```text
RAGService
    ↓
LLMService
    ↓
Ollama
    ↓
gpt-oss:120b-cloud
```

The LLM provider is isolated behind `LLMService` so the rest of the
application does not depend directly on Ollama.

---

## RAG Pipeline

```text
User Question
      ↓
Query Embedding
      ↓
FAISS Semantic Search
      ↓
Similarity Threshold
      ↓
Relevant Chunks
      ↓
Context Construction
      ↓
Grounded Prompt
      ↓
LLM
      ↓
Answer + Sources
```

---

## Grounding Strategy

The LLM is instructed to answer using only the retrieved document context.

If relevant information cannot be found in the retrieved chunks, the
system returns:

> I couldn't find relevant information in the uploaded document.

This prevents the LLM from answering unrelated questions using outside
knowledge.

---

## Relevance Filtering

A minimum similarity score of `0.60` is currently used.

```text
Similarity >= 0.60
        ↓
    Retrieved

Similarity < 0.60
        ↓
     Rejected
```

The threshold was selected after testing retrieval against both relevant
and unrelated questions.

---

## Example

### Relevant Question

```text
What is TCP?
```

The system:

1. Generates a query embedding.
2. Searches the FAISS index.
3. Retrieves relevant transport-layer chunks.
4. Sends those chunks to the LLM.
5. Generates a grounded answer.
6. Displays the retrieved chunks as sources.

### Unrelated Question

```text
What is LangGraph?
```

When the uploaded document is about the transport layer and the retrieved
chunks do not meet the similarity threshold, the LLM is not called.

The system instead reports that relevant information could not be found in
the document.

---

## Engineering Concepts

- Retrieval-Augmented Generation
- Semantic Search
- Query Embeddings
- Vector Similarity
- Context Construction
- Prompt Engineering
- Grounded Generation
- LLM Abstraction
- Hallucination Prevention
- Environment-Based Configuration

---

## Design Decisions

### 1. Separate LLM Service

LLM communication is isolated inside `LLMService`.

This prevents UI and RAG components from depending directly on Ollama.

### 2. Separate RAG Service

`RAGService` orchestrates:

- Query embedding
- Retrieval
- Context construction
- LLM generation

### 3. Retrieval Before Generation

The LLM is only called after relevant document chunks have been retrieved.

### 4. Similarity Threshold

Weak retrieval results are rejected before they reach the LLM.

### 5. Source Transparency

Retrieved chunks are displayed alongside the generated answer to make
the response traceable.

---

## Testing

The following scenarios were tested:

- Relevant questions return document-based answers.
- Unrelated questions are rejected when no relevant chunks meet the
  similarity threshold.
- Retrieved chunks are displayed as sources.
- Ollama LLM integration works successfully.
- RAG generation works successfully through the Paper Analysis page.

---

## Current Limitations

- Single-document workflow
- Fixed similarity threshold
- Basic prompt construction
- No conversation memory
- No reranking
- No hybrid search
- No citation formatting
- No multi-turn chat

---

## Future Improvements

- Chat with Paper
- Conversation history
- Source citations
- Cross-encoder reranking
- Hybrid retrieval
- Query rewriting
- Multi-document retrieval
- LangGraph orchestration
- Agent-based research workflows