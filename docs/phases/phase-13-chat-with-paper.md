# Phase 13 — Chat with Paper

## Goal

Build a persistent conversational interface that allows users to ask
multiple questions about uploaded research papers.

## Features

### Chat Management

- Create new chat sessions
- Select an existing research paper
- Upload a new research paper directly from the chat workflow
- Prevent duplicate chat creation
- Rename chat conversations
- Delete chat conversations
- Persist chat sessions in SQLite
- Display chat history ordered by recent activity

### Document Processing

New papers uploaded from the chat workflow go through the complete
document processing pipeline:

- PDF upload
- PDF parsing
- Text chunking
- Embedding generation
- FAISS vector store creation
- Vector store persistence
- Document metadata persistence

### Conversational RAG

- Ask questions about a selected research paper
- Retrieve relevant document chunks
- Generate grounded AI answers
- Maintain conversation history
- Contextualize follow-up questions
- Resolve references such as "it", "they", and "this"
- Use recent conversation context for better retrieval

### Source Transparency

- Display source chunks used for answers
- Show similarity scores
- Show document names
- Allow users to inspect retrieved content

## Architecture

```text
Chat Page
    ↓
ChatService
    ↓
Contextualize Follow-up Question
    ↓
RAGService
    ↓
Semantic Retrieval
    ↓
LLM Answer Generation
    ↓
Persist Messages