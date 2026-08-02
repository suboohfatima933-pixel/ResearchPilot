# Phase 05 – PDF Parsing

## Objective

Extract structured information from uploaded research papers using PyMuPDF.

---

## What Was Built

- PDF parser service
- Document domain model
- Text extraction
- Metadata extraction
- Page counting
- Text preview
- Character counting

---

## Files Added

- models/document.py
- services/pdf/parser_service.py

---

## Files Modified

- app/pages/analysis.py

---

## Engineering Concepts

- Document Processing Pipeline
- Domain Models
- Service Layer
- Separation of Concerns
- PyMuPDF Integration

---

## Architecture

Paper Analysis Page

↓

Upload Service

↓

Parser Service

↓

Document Model

---

## Lessons Learned

- Parsing and uploading should remain separate responsibilities.
- PDFs often contain little or no metadata.
- Structured domain models simplify future RAG stages.

---

## Future Improvements

- OCR support
- Image extraction
- Table extraction
- Layout-aware parsing
- Page-level metadata