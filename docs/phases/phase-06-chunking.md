# Phase 06 – Document Chunking

## Objective

Split parsed research papers into meaningful chunks to prepare them for embedding and semantic retrieval.

---

## What Was Built

- Chunk domain model
- Chunk service
- RecursiveCharacterTextSplitter integration
- Chunk Inspector
- Chunk Statistics
- Chunk Preview
- Average chunk size calculation

---

## Files Added

- models/chunk.py
- services/rag/chunk_service.py

---

## Files Modified

- app/pages/analysis.py

---

## Engineering Concepts

- Recursive Character Text Splitting
- Chunk Overlap
- Chunk Size Selection
- RAG Pipeline
- Separation of Concerns

---

## Architecture

PDF

↓

Parser Service

↓

Document

↓

Chunk Service

↓

Chunks

↓

Ready for Embeddings

---

## Design Decisions

- RecursiveCharacterTextSplitter
- Chunk Size: 1000
- Chunk Overlap: 200
- Domain-driven Chunk model
- Dedicated ChunkService

---

## Lessons Learned

- Chunking quality directly impacts retrieval quality.
- Visual chunk inspection helps debug the RAG pipeline.
- Statistics provide insight into chunk distribution.

---

## Future Improvements

- Semantic Chunking
- Parent-Child Chunking
- Layout-Aware Chunking
- Page-aware Chunks
- Citation-aware Chunks