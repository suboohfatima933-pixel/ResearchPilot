# Phase 16: Learning Center

## Overview

The Learning Center phase transforms uploaded research papers into an
interactive learning experience.

Unlike Paper Analysis, Research Insights, or Chat with Paper, the
Learning Center is designed specifically to help users understand,
study, test, and retain knowledge from research papers.

The system retrieves representative evidence from the selected paper and
uses AI to generate structured learning material based on the selected
difficulty level.

---

## Features Implemented

### Research Paper Selection

Users can select any previously uploaded and processed research paper
from the available document collection.

Learning material is generated specifically for the selected paper.

---

### Learning Levels

Users can choose between three learning levels:

- Beginner
- Intermediate
- Advanced

Each level changes how the AI explains and presents the research
content.

---

### Beginner Learning Level

The Beginner level focuses on:

- Simple and clear explanations
- Fundamental understanding
- Explanation of technical terms when necessary
- Easier conceptual learning

---

### Intermediate Learning Level

The Intermediate level focuses on:

- Normal academic language
- Important methodology
- Key findings
- Moderate conceptual depth

---

### Advanced Learning Level

The Advanced level focuses on:

- Academic terminology
- Deeper concepts
- Critical understanding
- More technically challenging quiz questions

---

## Multi-Query Evidence Retrieval

The Learning Service uses multiple targeted retrieval queries to collect
representative evidence from different areas of the research paper.

The retrieval process covers areas such as:

- Main research topic and purpose
- Important concepts
- Methodology
- Key findings and conclusions
- Technical details and insights

Retrieved chunks are deduplicated to prevent the same evidence from
appearing multiple times in the generated context.

---

## Semantic Retrieval

The Learning Center reuses the existing ResearchPilot RAG
infrastructure:

- EmbeddingService
- VectorStoreService
- Document-scoped FAISS indexes
- Similarity-based retrieval

This allows generated learning material to remain grounded in the
selected research paper.

---

## Simplified Explanation

The system generates a clear explanation of the research paper based on
the selected learning level.

The explanation helps users understand the overall research before
moving to individual concepts and quiz-based learning.

---

## Key Concepts

Important concepts from the research paper are extracted and explained.

Each concept contains:

- Concept name
- Clear explanation

The user interface presents concepts using expandable sections for
focused learning.

---

## Flashcards

The system generates question-and-answer flashcards from the research
paper.

Users can:

1. Read the question
2. Think about the answer
3. Reveal the answer interactively

This provides a simple active recall learning experience.

---

## Knowledge Quiz

The Learning Center generates multiple-choice questions based on the
retrieved research evidence.

Each quiz question contains:

- A question
- Four answer options
- One correct answer
- An explanation

The correct answer is required to exactly match one of the generated
options.

---

## Quiz Validation

The system prevents incomplete quiz submission.

Users must answer all generated questions before the quiz can be
submitted.

---

## Quiz Results

After submission, the system calculates:

- Number of correct answers
- Total questions
- Percentage score

A visual progress indicator is also displayed.

---

## Answer Review

Users can review their quiz performance after submission.

The system displays:

- Correct answers
- Incorrect answers
- Correct answers for missed questions
- Explanations for every question

This helps reinforce learning after completing the quiz.

---

## Quiz Retake

Users can reset their quiz results and retake the quiz.

The retake functionality clears previous quiz answers and submission
state while keeping the generated learning material available.

---

## Structured Learning Models

The Learning Center uses Pydantic models for structured validation.

### KeyConcept

Represents an important concept from the research paper.

Fields:

- Concept
- Explanation

### Flashcard

Represents an active recall learning card.

Fields:

- Question
- Answer

### QuizQuestion

Represents a multiple-choice knowledge question.

Fields:

- Question
- Options
- Correct answer
- Explanation

### LearningContent

Contains the complete AI-generated learning experience.

Fields:

- Simplified explanation
- Key concepts
- Flashcards
- Quiz questions

---

## JSON Response Validation

The AI is instructed to return structured JSON only.

The Learning Service:

1. Cleans the AI response
2. Removes optional markdown code fences
3. Parses the JSON response
4. Validates the result using Pydantic
5. Returns a structured LearningContent model

Invalid responses are handled with a clear error.

---

## Session State Handling

Generated learning material is stored in Streamlit session state.

The system stores:

- Generated learning content
- Selected document ID
- Selected difficulty level
- Quiz answers
- Quiz submission state

This prevents generated learning content from disappearing during normal
Streamlit reruns.

---

## Cross-Paper Content Protection

The system prevents learning material generated for one paper from being
displayed when another paper is selected.

It also prevents learning material generated for one difficulty level
from being displayed when the user switches to another level.

---

## Architecture

The Learning Center follows the ResearchPilot service architecture:

```text
Learning Center Page
        ↓
LearningService
        ↓
EmbeddingService
        ↓
VectorStoreService
        ↓
Multi-Query Evidence Retrieval
        ↓
Grounded Learning Context
        ↓
LLMService
        ↓
JSON Response
        ↓
Pydantic Validation
        ↓
LearningContent
        ↓
Interactive Learning UI