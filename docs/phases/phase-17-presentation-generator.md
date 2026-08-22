# Phase 17: Presentation Generator

## Overview

Phase 17 introduces the Presentation Generator, allowing users to transform research papers into structured, AI-generated presentations.

The feature retrieves representative evidence from a selected research paper, builds grounded context, generates structured presentation content using AI, and exports the final presentation as a downloadable PowerPoint file.

---

## Features Implemented

### 📊 Presentation Generation

- Research paper selection
- Multiple presentation types
- Adjustable slide count
- AI-generated presentation structure
- Slide titles and concise bullet points
- AI-generated speaker notes
- Logical slide-by-slide narrative generation

### 🧠 Grounded Evidence Retrieval

The presentation generation process retrieves representative evidence from the selected research paper across key research areas:

- Main research topic and purpose
- Research problem
- Methodology and approach
- Important findings
- Conclusions and implications
- Limitations and future research directions

Retrieved chunks are deduplicated before being used as source evidence.

---

## Presentation Types

The following presentation types are supported:

### Research Summary

Provides a balanced overview of:

- Research problem
- Methodology
- Key findings
- Conclusions
- Research significance

### Academic Presentation

Uses a formal academic structure focused on:

- Research objectives
- Methodology
- Findings
- Limitations
- Conclusions

### Executive Summary

Focuses on:

- Most important findings
- Key implications
- Decision-focused insights
- Research impact

### Educational Presentation

Focuses on:

- Clear explanations
- Progressive introduction of concepts
- Learning and understanding
- Reduced unnecessary technical complexity

---

## AI Response Validation

The AI is instructed to return structured JSON only.

Generated responses are parsed and validated using Pydantic models.

The presentation structure includes:

- Presentation title
- List of slides
- Slide title
- Slide content
- Speaker notes

Invalid JSON responses are handled with clear validation errors.

---

## Slide Preview

Generated presentations can be reviewed inside ResearchPilot before export.

The preview provides:

- Slide-by-slide inspection
- Expandable slide sections
- Slide titles
- Generated bullet points
- Speaker notes

---

## PowerPoint Export

Phase 17 also introduces real PowerPoint export.

Generated presentations can be exported as `.pptx` files.

The export includes:

- Presentation title slide
- Source document reference
- Generated content slides
- Bullet point formatting
- Slide numbering
- 16:9 widescreen layout
- Unique timestamped filenames

Exported presentations are saved in:

```text
data/presentations/