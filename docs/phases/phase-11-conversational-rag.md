# Phase 11 – Conversational RAG & Chat Experience

## Objective

Extend the Basic RAG pipeline into a conversational research experience.

ResearchPilot can now maintain independent conversations around research
papers, understand follow-up questions using conversation context, and
provide a ChatGPT-style interface for interacting with uploaded documents.

---

## What Was Built

- `ChatService`
- `ChatSession` model
- Conversational RAG
- Conversation-aware query contextualization
- Follow-up question handling
- Document-scoped conversations
- Multiple independent chat sessions
- Chat history panel
- New Chat functionality
- Active conversation handling
- Document association with conversations
- Retrieved source display
- ChatGPT-style message interface

---

## Conversational RAG Architecture

```text
User Message
      ↓
Conversation History
      ↓
Query Contextualization
      ↓
Standalone Query
      ↓
Query Embedding
      ↓
Document-Specific Retrieval
      ↓
Relevant Chunks
      ↓
RAGService
      ↓
LLMService
      ↓
Ollama
      ↓
Grounded Answer
```

---

## Follow-Up Questions

The system can resolve references in follow-up questions using recent
conversation history.

Example:

```text
User:
What is social cohesion?

Assistant:
Social cohesion is...

User:
Give its definition.
```

The system contextualizes the second question into a standalone query:

```text
Give the definition of social cohesion.
```

This contextualized query is then used for semantic retrieval.

---

## Conversation Context

The most recent conversation messages are provided to the contextualization
step.

The system currently uses the latest six messages when constructing the
conversation context.

This provides enough recent context for normal research conversations
without continuously sending the entire conversation to the LLM.

---

## Chat Sessions

Each conversation is represented by a `ChatSession`.

```text
ChatSession
├── id
├── title
├── document_id
├── messages
├── created_at
└── updated_at
```

Each chat is associated with a specific research document.

```text
Chat A
 └── Document A

Chat B
 └── Document B

Chat C
 └── Document C
```

This prevents conversations from becoming mixed with unrelated papers.

---

## Chat Interface

The Chat with Paper page now contains two levels of navigation.

### Application Navigation

The existing ResearchPilot sidebar provides application-level navigation:

```text
Home
Research Discovery
Paper Analysis
Compare Papers
Chat with Paper
Learning Center
Presentation Generator
Retrieval Debugger
Agent Workflow
Settings
```

### Chat Navigation

Inside Chat with Paper, a separate in-page panel provides:

```text
Chats

+ New Chat

Recent conversations
```

This avoids creating a second Streamlit application sidebar.

---

## Chat Workspace

The Chat with Paper workspace is divided into:

```text
┌──────────────────┬─────────────────────────────┐
│                  │                             │
│   Chat History   │      Current Conversation   │
│                  │                             │
│   + New Chat     │      Research Paper         │
│                  │                             │
│   Social Cohesion│      User message           │
│   TCP Research   │      AI response             │
│                  │                             │
│                  │      Ask a question...      │
└──────────────────┴─────────────────────────────┘
```

---

## Document-Scoped Retrieval

Each conversation carries a `document_id`.

The document ID is passed through the chat and RAG layers so retrieval is
performed against the correct research paper.

```text
ChatSession
     ↓
document_id
     ↓
RAGService
     ↓
Document-specific Vector Store
```

This prevents one paper's chunks from being used to answer questions about
another paper.

---

## Source Transparency

Generated answers can display their retrieved sources.

Each source provides:

- Chunk ID
- Similarity score
- Document name
- Chunk content

This allows users to inspect the document context behind an answer.

---

## Current Limitations

- Chat persistence was initially session-based.
- Response streaming has not yet been implemented.
- Automatic scrolling has not yet been implemented.
- PDF upload is still handled through Paper Analysis.
- Chat titles are currently generated from the document filename.
- Advanced long-term memory has not yet been implemented.

---

## Future Improvements

- Persistent chat storage
- Persistent document records
- Upload directly from New Chat
- Streaming responses
- Automatic scrolling
- Rename chats
- Delete chats
- Search chat history
- Advanced conversational memory
- Multi-document conversations