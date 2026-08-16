# Phase 12 – Persistent Chat & Database

## Objective

Replace temporary Streamlit chat state with persistent application
storage using SQLite.

ResearchPilot can now restore conversations after the Streamlit
application is restarted.

---

## What Was Built

- SQLite database
- `DatabaseService`
- `ChatRepository`
- Persistent chat sessions
- Persistent chat messages
- Chat retrieval
- Chat creation
- Chat title updates
- Chat deletion support
- Message persistence
- Chat timestamp updates
- Database-backed chat history

---

## Database Architecture

```text
Chat UI
   ↓
ChatService
   ↓
ChatRepository
   ↓
DatabaseService
   ↓
SQLite
```

The UI does not directly interact with SQLite.

Database access is isolated behind repository and database service layers.

---

## Database Location

The local database is stored at:

```text
database/
└── research_pilot.db
```

The database is created automatically when the database service is
initialized.

---

## Database Schema

### Chats

The `chats` table stores conversation-level information.

```text
chats
├── id
├── title
├── document_id
├── created_at
└── updated_at
```

### Chat Messages

The `chat_messages` table stores individual messages.

```text
chat_messages
├── id
├── chat_id
├── role
├── content
└── created_at
```

The relationship is:

```text
chats.id
    │
    ▼
chat_messages.chat_id
```

One chat can contain many messages.

---

## Persistent Chat Flow

### Creating a Chat

```text
New Chat
   ↓
ChatService.create_chat()
   ↓
ChatRepository.create_chat()
   ↓
SQLite
```

### Loading Chats

```text
Chat Page
   ↓
ChatService.get_all_chats()
   ↓
ChatRepository.get_all_chats()
   ↓
SQLite
   ↓
Chat History
```

### Loading a Conversation

```text
Selected Chat
      ↓
chat_id
      ↓
ChatRepository.get_chat()
      ↓
Messages
      ↓
Conversation UI
```

### Saving Messages

```text
User Message
      ↓
ChatService
      ↓
RAG
      ↓
Assistant Response
      ↓
ChatRepository.add_message()
      ↓
SQLite
```

Both the user message and assistant response are persisted.

---

## Chat Restoration

Previously, chat sessions existed only in Streamlit session state.

```text
Streamlit restart
       ↓
Chats lost
```

After Phase 12:

```text
Streamlit restart
       ↓
SQLite
       ↓
ChatRepository
       ↓
Chat history restored
```

This was successfully tested by restarting the Streamlit application and
confirming that previously created conversations remained available.

---

## Separation of Responsibilities

### ChatService

Responsible for application-level chat orchestration.

```text
ChatService
├── Create chat
├── Load chat
├── Load all chats
├── Send message
├── Update title
└── Delete chat
```

### ChatRepository

Responsible for persistent chat storage.

```text
ChatRepository
├── create_chat()
├── get_chat()
├── get_all_chats()
├── add_message()
├── get_messages()
├── update_title()
└── delete_chat()
```

### DatabaseService

Responsible for:

- SQLite connection management
- Database initialization
- Table creation
- Foreign-key configuration

---

## Why SQLite?

SQLite was selected for the current ResearchPilot architecture because it:

- Requires no separate database server.
- Works well for local development.
- Is included with Python.
- Provides relational data storage.
- Supports relationships between chats and messages.
- Can later be migrated to PostgreSQL if the application becomes
  multi-user or production-scale.

---

## Database vs Application Data

The SQLite database stores structured application information.

```text
database/
└── research_pilot.db
```

Uploaded PDFs and vector indexes remain separate:

```text
data/
├── uploads/
└── vector_stores/
```

The database does not store the FAISS vectors or raw PDF files.

---

## Current Architecture

```text
                       ResearchPilot
                            │
             ┌──────────────┴──────────────┐
             │                             │
        Chat Interface                 Paper Analysis
             │                             │
             ▼                             ▼
        ChatService                  PDF Processing
             │                             │
      ┌──────┴──────┐                      ▼
      │             │                 Embeddings
      ▼             ▼                      │
ChatRepository   RAGService                ▼
      │             │                 FAISS Vector Store
      ▼             ▼
   SQLite          LLM
                   │
                   ▼
                 Ollama
```

---

## Current Limitations

- Document metadata is not yet persisted in SQLite.
- Uploaded documents are still discovered from the filesystem.
- Chat titles currently use the document filename.
- No user/account system.
- No database migrations yet.
- No PostgreSQL support.
- No chat search.
- No chat rename/delete UI yet.

---

## Next Phase

The next step is to introduce persistent document records and connect them
to the existing chat and vector-store architecture.

Planned work:

- `documents` database table
- `DocumentRepository`
- Persistent document metadata
- Document upload registration
- Document-to-chat relationships
- Document management
- Upload directly from New Chat