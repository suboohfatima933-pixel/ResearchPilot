# Phase 14 — Retrieval Debugger

## Objective

Build a dedicated debugging interface to inspect and validate
ResearchPilot's semantic retrieval behavior.

The Retrieval Debugger allows users to test how queries are embedded,
searched against a selected research paper, filtered by similarity,
and returned as ranked document chunks.

---

## Features Implemented

### 1. Research Paper Selection

Users can select any persisted research paper from the database.

The selected document is used to load and inspect its corresponding
FAISS vector store.

---

### 2. Query Testing

Users can enter custom queries to test semantic retrieval.

Example queries include:

- What methodology was used in this research?
- What are the main findings of this research?
- What problem does this research attempt to solve?

---

### 3. Adjustable Top K

The debugger allows users to control how many of the highest-ranked
retrieval results should be returned.

Supported range:

- Minimum: 1 result
- Maximum: 10 results
- Default: 5 results

---

### 4. Adjustable Similarity Threshold

Users can control the minimum similarity score required for a chunk
to be included in the results.

This makes it possible to inspect how threshold filtering affects
semantic retrieval quality.

---

### 5. Retrieval Overview

The debugger displays important retrieval metrics:

- Query embedding dimensions
- Total vectors in the selected document
- Number of results found
- Selected minimum similarity threshold

---

### 6. Ranked Chunk Inspection

Retrieved chunks are displayed in ranked order.

Each result includes:

- Retrieval position
- Similarity percentage
- Chunk ID
- Character range
- Visual similarity indicator
- Retrieved chunk content

---

### 7. Empty Result Handling

If no chunks meet the selected similarity threshold, the debugger
shows a clear message instead of displaying irrelevant results.

---

### 8. Retrieval Validation

The Retrieval Debugger was tested using both relevant and irrelevant
queries.

Relevant queries successfully returned meaningful research content.

An irrelevant query about a chocolate cake returned weak matches when
the similarity threshold was set to `0.00`.

After increasing the threshold to `0.45`, the irrelevant query was
correctly filtered out while relevant methodology and findings queries
continued to return meaningful chunks.

This validated the retrieval threshold behavior for the current
embedding model and test document.

---

## Architecture

```text
Retrieval Debugger Page
        ↓
RetrievalDebuggerService
        ↓
EmbeddingService
        ↓
VectorStoreService
        ↓
Document-Specific FAISS Index
        ↓
Ranked SearchResult Objects
        ↓
Retrieval Debugger UI