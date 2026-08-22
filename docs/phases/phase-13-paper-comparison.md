# Phase 13 — Paper Comparison

## Goal

Build an AI-powered paper comparison feature that allows users
to compare two research papers using evidence retrieved from
each document.

---

## Features Implemented

### Paper Selection

Users can:

- Select Paper A
- Select Paper B
- Compare two different research papers

The system prevents users from selecting the same paper twice.

---

### Comparison Focus

Users can compare papers based on:

- Overall Comparison
- Research Objectives
- Methodology
- Key Findings
- Strengths and Limitations
- Conclusions
- Custom Question

---

### Evidence Retrieval

The system:

1. Converts the comparison question into an embedding.
2. Loads the FAISS vector store for Paper A.
3. Retrieves relevant chunks from Paper A.
4. Loads the FAISS vector store for Paper B.
5. Retrieves relevant chunks from Paper B.
6. Builds a combined evidence context.
7. Sends the grounded context to the LLM.

This ensures comparisons are based on retrieved evidence
rather than unsupported assumptions.

---

### Document-Scoped Vector Stores

Each research paper has its own vector store:

```text
data/vector_stores/
└── document_id/
    ├── faiss.index
    └── metadata.json