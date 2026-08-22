# Phase 15: Research Insights

## Overview

The Research Insights phase adds an AI-powered research analysis
experience to ResearchPilot.

Unlike the Paper Analysis page, which focuses on analyzing and
interacting with individual aspects of a research paper, this feature
generates a broader structured understanding of the selected paper.

The system retrieves relevant evidence from the paper using multiple
targeted queries and uses the retrieved context to generate grounded
research insights.

---

## Features Implemented

### Research Paper Selection

Users can select any previously uploaded and processed research paper
for insight generation.

The page retrieves available documents from the persistent document
repository.

---

### AI-Powered Insight Generation

ResearchPilot generates structured insights from the selected research
paper using the LLM service.

The generated insights are based on retrieved evidence rather than
sending the entire paper directly to the language model.

---

### Multi-Query Evidence Retrieval

The system uses multiple targeted retrieval queries to gather evidence
covering different aspects of the research paper.

This provides broader coverage of the paper and helps generate insights
about areas such as:

- Research problem
- Research objectives
- Methodology
- Key findings
- Limitations
- Research gaps
- Practical implications

---

### Semantic Retrieval

Relevant document chunks are retrieved using:

- Query embeddings
- Document-scoped FAISS vector stores
- Similarity-based semantic search
- Configurable retrieval limits

This ensures that the generated insights remain grounded in the content
of the selected research paper.

---

### Executive Summary

The system generates a concise high-level summary of the research paper.

The summary provides an overview of the main purpose, approach, and
important outcomes of the research.

---

### Research Problem Identification

ResearchPilot identifies the primary problem, challenge, or research
question addressed by the paper.

---

### Research Objectives Extraction

The system extracts the main objectives or goals of the research.

The objectives are returned as structured items for easy reading.

---

### Methodology Analysis

ResearchPilot generates an overview of the methodology used in the
research based on the retrieved evidence.

---

### Key Findings

Important findings and outcomes from the research are identified and
presented as a structured list.

---

### Research Limitations

The system identifies limitations discussed or indicated within the
available research evidence.

If sufficient evidence is unavailable, the AI is instructed not to
invent unsupported limitations.

---

### Research Gaps

ResearchPilot identifies potential research gaps or areas that require
further investigation based on the retrieved paper content.

---

### Practical Impact

The system generates insights about the potential practical impact,
applications, or implications of the research.

---

### Key Takeaways

The page provides a concise list of the most important takeaways from
the research paper.

---

## Structured Insight Model

Generated insights are stored using a structured Pydantic-based model.

The model organizes research insights into fields including:

- Executive summary
- Research problem
- Objectives
- Methodology
- Key findings
- Limitations
- Research gaps
- Practical impact
- Key takeaways

This provides consistent validation and structured handling of the AI
response.

---

## Grounded AI Generation

The LLM is instructed to generate insights using only the retrieved
research paper context.

The system avoids unsupported conclusions and instructs the model to
clearly indicate when sufficient evidence is unavailable.

---

## Session State Handling

Generated insights are stored in Streamlit session state.

This prevents generated results from disappearing unnecessarily during
page reruns.

The selected document ID is also stored to ensure that insights from one
research paper are not incorrectly displayed when another paper is
selected.

---

## User Interface

The Research Insights page includes:

1. Research paper selection
2. Generate Research Insights action
3. Loading state during analysis
4. Error handling for missing evidence
5. Executive summary section
6. Research problem section
7. Research objectives section
8. Methodology section
9. Key findings section
10. Limitations section
11. Research gaps section
12. Practical impact section
13. Key takeaways section

---

## Architecture

The feature follows the existing ResearchPilot service architecture:

```text
Research Insights Page
        ↓
ResearchInsightsService
        ↓
EmbeddingService
        ↓
VectorStoreService
        ↓
Retrieved Research Evidence
        ↓
LLMService
        ↓
Structured ResearchInsights Model
        ↓
Research Insights UI