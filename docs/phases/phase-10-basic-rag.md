# Phase 10 – Basic RAG

## Objective

Implement the first complete Retrieval-Augmented Generation (RAG)
pipeline for ResearchPilot.

The objective is to combine semantic retrieval with an LLM so that the
system can generate answers grounded in the uploaded research paper.

---

## What Was Built

- Ollama LLM integration
- Centralized LLM configuration
- `LLMService`
- `RAGService`
- Query embedding
- Semantic retrieval
- Context construction
- Grounded prompt generation
- LLM-generated answers
- Retrieved source display
- Similarity threshold protection

---

## LLM Configuration

ResearchPilot uses Ollama for LLM generation.

The model is configured through the environment rather than being
hardcoded throughout the application.

Example:

```env
OLLAMA_MODEL=gpt-oss:120b-cloud
```

The model configuration is loaded centrally through:

```text
config/settings.py
```

This allows the model to be changed without modifying the LLM service.

---

## LLM Architecture

```text
RAGService
     ↓
LLMService
     ↓
Ollama
     ↓
gpt-oss:120b-cloud
```

`LLMService` is responsible for communication with the configured
Ollama model.

The rest of the application does not directly depend on Ollama.

---

## RAG Pipeline

```text
User Question
      ↓
Query Embedding
      ↓
FAISS Semantic Search
      ↓
Relevant Chunks
      ↓
Context Construction
      ↓
Grounded Prompt
      ↓
LLM
      ↓
Generated Answer
      ↓
Sources
```

---

## Retrieval and Generation

The RAG pipeline separates retrieval from generation.

First, the user's question is converted into an embedding.

The embedding is used to retrieve relevant document chunks from FAISS.

Only retrieved chunks that meet the configured similarity threshold are
passed to the LLM.

The LLM then generates an answer using the retrieved context.

---

## Grounding Strategy

The LLM is explicitly instructed to answer using only the provided
document context.

The prompt instructs the model to:

- Use only the supplied document context.
- Avoid outside knowledge.
- Avoid inventing information.
- State when the answer cannot be found in the document.

This reduces the likelihood of unsupported answers.

---

## Relevance Threshold

The retrieval pipeline uses a minimum similarity score of `0.60`.

```text
Similarity >= 0.60
        ↓
Relevant
        ↓
Passed to LLM


Similarity < 0.60
        ↓
Rejected
        ↓
LLM is not called
```

This provides an important guardrail against generating answers from
unrelated document content.

---

## Example

### Relevant Question

```text
What is TCP?
```

The system:

1. Creates a query embedding.
2. Searches the vector store.
3. Retrieves relevant chunks.
4. Builds the document context.
5. Sends the context to the LLM.
6. Generates a grounded answer.
7. Displays the retrieved chunks as sources.

---

### Irrelevant Question

```text
What is LangGraph?
```

If the uploaded document is about the transport layer and no retrieved
chunks meet the similarity threshold, the system does not call the LLM.

Instead, it returns:

```text
I couldn't find relevant information in the uploaded document.
```

This prevents the model from answering an unrelated question using its
general knowledge.

---

## RAGService

`RAGService` orchestrates the complete retrieval and generation process.

Its responsibilities include:

- Generating the query embedding.
- Loading the vector store.
- Retrieving relevant chunks.
- Applying the similarity threshold.
- Building the context.
- Constructing the grounded prompt.
- Calling `LLMService`.
- Returning the answer and sources.

---

## LLMService

`LLMService` provides an abstraction around Ollama.

The RAG layer does not need to know how Ollama is configured or called.

The interaction is simplified to:

```python
answer = llm_service.generate(prompt)
```

This makes the LLM provider easier to replace or extend later.

---

## Source Display

The generated answer is accompanied by the document chunks used as
retrieval sources.

Each source displays:

- Chunk ID
- Similarity score
- Document name
- Chunk content

This provides transparency into which parts of the paper influenced the
answer.

---

## Testing

The following scenarios were tested successfully:

### Relevant Retrieval

```text
What is TCP?
```

Result:

- Relevant chunks retrieved.
- LLM generated an answer.
- Sources displayed.

### Irrelevant Retrieval

```text
What is LangGraph?
```

Result:

- No sufficiently relevant chunks.
- LLM was not called.
- System returned the document-not-found response.

### LLM Integration

The Ollama model was tested independently before being connected to the
RAG pipeline.

The configured model:

```text
gpt-oss:120b-cloud
```

successfully generated responses.

---

## Engineering Concepts

- Retrieval-Augmented Generation
- Semantic Retrieval
- Query Embeddings
- Vector Search
- Context Construction
- Prompt Engineering
- Grounded Generation
- LLM Abstraction
- Hallucination Prevention
- Environment-Based Configuration

---

## Design Decisions

### Separate LLM Service

Ollama communication is isolated inside `LLMService`.

### Separate RAG Service

`RAGService` orchestrates retrieval and generation without placing AI
logic directly inside the Streamlit UI.

### Retrieval Before Generation

The LLM is only called when relevant document context has been retrieved.

### Similarity Threshold

Weak retrieval results are rejected before reaching the LLM.

### Environment-Based Model Configuration

The LLM model is configured through `.env` rather than being hardcoded
inside application services.

### Source Transparency

Retrieved chunks are displayed with the generated answer.

---

## Current Limitations

- Single-question RAG workflow
- No conversation memory
- No streaming responses
- No reranking
- No hybrid retrieval
- No multi-document retrieval
- No persistent chat history
- Basic prompt construction

---

## Future Improvements

- Conversational RAG
- Chat with Paper
- Conversation history
- Query contextualization
- Streaming responses
- Source citations
- Cross-encoder reranking
- Hybrid retrieval
- Multi-document research
- LangGraph orchestration
- Agent-based research workflows