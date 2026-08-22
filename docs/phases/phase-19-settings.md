# Phase 19: Settings

## Overview

Phase 19 introduces the Settings page, providing a centralized overview of the current ResearchPilot configuration and application storage.

The page focuses on displaying real application information rather than introducing unused or non-functional settings.

---

## Features Implemented

### ⚙️ AI Configuration

The Settings page displays the current AI configuration used by ResearchPilot:

- LLM provider
- Active LLM model
- Embedding model
- Embedding dimensions

This information is connected to the application's actual configuration and services.

---

## 📄 Document Processing Configuration

The page provides visibility into the current document processing setup:

- Supported document format
- Maximum upload size
- FAISS vector store
- Cosine similarity retrieval
- Document-scoped vector stores
- PowerPoint presentation export

---

## 💾 Storage Overview

The Settings page displays real-time application storage information.

The following counts are available:

- Uploaded research papers
- Document vector stores
- Generated PowerPoint presentations

These values are calculated from the application's actual storage and data directories.

---

## 🧠 AI Configuration

ResearchPilot currently uses:

- Ollama as the LLM provider
- The configured Ollama model for AI generation
- `BAAI/bge-small-en-v1.5` for semantic embeddings
- 384-dimensional embedding vectors

The active LLM model is loaded from the application configuration.

---

## 🗂️ Storage Architecture

ResearchPilot uses separate storage areas for different application resources:

```text
data/
├── uploads/
│   └── {document_id}/
│
├── vector_stores/
│   └── {document_id}/
│
└── presentations/
    └── generated_presentation.pptx