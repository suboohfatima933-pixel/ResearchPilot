# Phase 04 – PDF Upload

## Objective

Implement a secure PDF upload pipeline that prepares research papers for AI processing.

---

## What Was Built

- PDF upload page
- Upload service
- PDF validation
- File size validation
- Automatic upload directory creation
- Timestamp-based unique filenames
- Safe filename sanitization

---

## Engineering Concepts

- File Upload Pipeline
- Service Layer
- File Validation
- Path Management using pathlib
- Separation of Concerns

---

## Architecture

User

↓

Paper Analysis Page

↓

Upload Service

↓

Validation

↓

data/uploads/

---

## Design Decisions

- Store uploaded PDFs inside `data/uploads`
- Generate unique filenames using timestamps
- Preserve the original filename for display
- Keep upload and parsing as separate phases

---

## Lessons Learned

- Uploading and parsing should be separate responsibilities.
- Safe file handling is an important part of production AI applications.
- Human-readable filenames simplify debugging.

---

## Future Improvements

- Duplicate file detection
- MIME type validation
- SHA-256 file hashing
- Cloud storage support (AWS S3, Azure Blob)