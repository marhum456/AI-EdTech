# RAG-Based AI Assessment MVP

A **RAG-based AI assessment MVP** developed at **OptimusFox, Lahore**, focused on transforming learning materials into structured, lesson-grounded assessments.

> **Lesson-Grounded Quiz Generation with Subject-Aware LLM Routing**

The MVP combines **Python, FastAPI, document processing, embeddings, ChromaDB, subject-aware LLM routing, Groq, MongoDB Atlas, and Swagger UI** to create an end-to-end AI assessment workflow.

> **Learning Material → Knowledge Extraction → Lesson Context → AI Question Generation → Quiz → Evaluation & Progress**

---

## Overview

The **RAG-Based AI Assessment MVP** explores how generative AI and retrieval-based architectures can support modern learning and assessment workflows.

The current MVP provides three primary API workflows:

1. **Lesson Upload** — ingest and process learning material.
2. **Quiz Generation** — generate a structured assessment using lesson context and subject-aware LLM routing.
3. **Quiz Submission** — evaluate submitted answers and store progress.

The system separates content ingestion, retrieval, model routing, generation, storage, and evaluation into distinct stages.

---

## Architecture

```text
                    RAG-BASED AI ASSESSMENT MVP

 ┌───────────────────────┐
 │   Learning Material   │
 │      PDF / Lesson     │
 └───────────┬───────────┘
             │
             ▼
 ┌───────────────────────┐
 │   Lesson Upload API   │
 │ POST /admin/lessons/  │
 │        upload         │
 └───────────┬───────────┘
             │
             ▼
 ┌───────────────────────┐
 │  Content Extraction   │
 │   Cleaning / Parsing  │
 └───────────┬───────────┘
             │
             ▼
 ┌───────────────────────┐
 │ Chunking + Embeddings │
 │       ChromaDB        │
 └───────────┬───────────┘
             │
             │ Quiz Request
             │
             ▼
 ┌───────────────────────┐
 │ Lesson-Level Context  │
 │       Retrieval       │
 └───────────┬───────────┘
             │
             ▼
 ┌───────────────────────┐
 │  Subject-Aware LLM    │
 │       Routing         │
 │        Groq           │
 └───────────┬───────────┘
             │
             ▼
 ┌───────────────────────┐
 │   Quiz Generation     │
 │   POST /quiz/generate │
 └───────────┬───────────┘
             │
             ▼
 ┌───────────────────────┐
 │     MongoDB Atlas     │
 │ Quiz + Progress Data  │
 └───────────┬───────────┘
             │
             ▼
 ┌───────────────────────┐
 │    Quiz Submission    │
 │   POST /quiz/submit   │
 └───────────┬───────────┘
             │
             ▼
 ┌───────────────────────┐
 │ Evaluation + Progress │
 └───────────────────────┘
```

---

## End-to-End Workflow

### 1. Lesson Upload

Learning material is submitted through:

```http
POST /admin/lessons/upload
```

The ingestion pipeline processes the uploaded material:

```text
PDF Upload
    ↓
Validation
    ↓
Text Extraction
    ↓
Cleaning / Normalization
    ↓
Chunking
    ↓
Embeddings
    ↓
ChromaDB
```

The processed content is then available for lesson-grounded assessment generation.

---

### 2. Content Extraction

The uploaded learning material is converted into structured text.

The extraction stage focuses on:

- Extracting text from PDF documents
- Cleaning and normalizing content
- Preserving useful document structure
- Preparing content for chunking and embeddings

```text
Learning Material
       ↓
Structured Text
```

---

### 3. Chunking, Embeddings & Vector Storage

The extracted lesson content is divided into manageable chunks.

Each chunk is converted into an embedding and stored in **ChromaDB**.

```text
Lesson Content
      ↓
    Chunks
      ↓
  Embeddings
      ↓
   ChromaDB
```

The stored content is associated with the relevant learning context, such as subject, course, and lesson.

---

# RAG-Based Assessment Generation

The assessment pipeline uses a retrieval-based approach to provide the LLM with context from the selected lesson.

The current implementation uses **lesson-scoped context retrieval** rather than relying on generic top-k retrieval for question generation.

When a quiz is requested, the system identifies the selected lesson and retrieves the content associated with that lesson.

```text
Selected Lesson
      ↓
Lesson Context
      ↓
LLM Prompt Context
      ↓
Question Generation
```

This allows generated questions to remain grounded in the learning material available for the selected lesson.

### Why Lesson-Level Context?

For assessment generation, the goal is to provide broader coverage of the selected lesson rather than supplying only a small number of semantically similar chunks.

This is useful when an assessment is intended to represent the lesson as a whole.

---

## Subject-Aware LLM Routing

The MVP includes a routing layer that selects the appropriate model configuration based on the subject.

```text
                  Quiz Request
                       │
                       ▼
               Subject / Context
                       │
                       ▼
              Subject-Aware Router
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
       Subject Model       Other Routing
              │                 │
              └────────┬────────┘
                       ▼
                    Groq LLM
                       │
                       ▼
                Quiz Generation
```

This separates:

- **Retrieval** — supplies lesson context
- **Routing** — determines the model configuration
- **LLM** — generates the assessment
- **Storage** — persists generated assessment data

---

## Quiz Generation API

The main assessment-generation endpoint is:

```http
POST /quiz/generate
```

The workflow is:

```text
Subject
   +
Course
   +
Lesson
   ↓
Retrieve Lesson Context
   ↓
Subject-Aware Routing
   ↓
Groq LLM
   ↓
Generate Questions
   ↓
Structured Quiz
   ↓
MongoDB Atlas
```

The generated assessment is returned in a structured format suitable for consumption by a frontend or learning platform.

---

## Quiz Storage

Generated assessments are stored in **MongoDB Atlas**.

MongoDB is used for application-level data such as:

- Generated quizzes
- Quiz metadata
- Lesson associations
- Assessment information
- Progress information
- Submission results

The vector database and application database have separate responsibilities.

| Component | Responsibility |
|---|---|
| **ChromaDB** | Lesson content, chunks, embeddings, and retrieval context |
| **MongoDB Atlas** | Quizzes, metadata, submissions, and progress |
| **Groq** | LLM inference and question generation |
| **FastAPI** | API layer and application workflow |

---

## Quiz Submission & Evaluation

Students submit their answers through:

```http
POST /quiz/submit
```

The workflow is:

```text
Student Answers
      ↓
Answer Validation
      ↓
Evaluation
      ↓
Result / Feedback
      ↓
Progress Storage
      ↓
MongoDB Atlas
```

This completes the core assessment lifecycle.

---

# API Overview

| Endpoint | Method | Purpose |
|---|---|---|
| `/admin/lessons/upload` | POST | Upload and process lesson material |
| `/quiz/generate` | POST | Generate a lesson-grounded AI quiz |
| `/quiz/submit` | POST | Evaluate submitted answers and store progress |

---

## Example API Flow

### Step 1 — Upload Lesson

```http
POST /admin/lessons/upload
```

```text
PDF
 ↓
Extraction
 ↓
Chunking
 ↓
Embeddings
 ↓
ChromaDB
```

### Step 2 — Generate Quiz

```http
POST /quiz/generate
```

```text
Subject + Course + Lesson
          ↓
   Lesson Context
          ↓
 Subject-Aware Routing
          ↓
       Groq LLM
          ↓
   Structured Quiz
          ↓
     MongoDB Atlas
```

### Step 3 — Submit Quiz

```http
POST /quiz/submit
```

```text
Answers
   ↓
Evaluation
   ↓
Result / Feedback
   ↓
Progress
```

---

# Tech Stack

| Technology | Role |
|---|---|
| **Python 3.12** | Core development language |
| **FastAPI** | Backend API framework |
| **Groq** | LLM inference and quiz generation |
| **ChromaDB** | Vector storage and lesson-context retrieval |
| **MongoDB Atlas** | Quiz and progress persistence |
| **Swagger UI** | API testing and exploration |

---

# Core Features

- Lesson material ingestion
- PDF text extraction
- Content cleaning and normalization
- Content chunking
- Embedding generation
- ChromaDB vector storage
- Lesson-scoped context retrieval
- Subject-aware LLM routing
- Groq-powered question generation
- Structured quiz generation
- MongoDB Atlas persistence
- Automated answer evaluation
- Progress tracking
- FastAPI API layer
- Swagger UI API testing

---

# Design Principles

### 1. Separate Ingestion from Generation

Content processing happens before quiz generation.

```text
Ingestion
   ↓
Processed Lesson Content
   ↓
Assessment Generation
```

This avoids repeatedly processing the original document whenever a quiz is requested.

### 2. Ground Generation in Lesson Content

The generation layer receives context derived from the selected lesson instead of relying solely on the LLM's general knowledge.

### 3. Separate Model Routing from Generation

The routing layer determines which model configuration should handle the subject, while the generation layer focuses on producing the assessment.

### 4. Separate Vector and Application Storage

```text
ChromaDB
→ Knowledge / Retrieval

MongoDB Atlas
→ Application / Assessment Data
```

### 5. Expose the Workflow Through APIs

The AI pipeline is exposed through APIs rather than being implemented only as an isolated script.

This allows the assessment workflow to be consumed by a frontend or future learning platform integration.

---

# Future Direction

- **Moodle Integration**
- **Modular Quiz Plugin**
- **AI Assignment Assistant Plugin** 
- **Personalized Learning & Analytics**
- **Scalable Processing**

---

# Project Goal

The goal of this MVP is to explore how AI, retrieval-based architectures, and subject-aware LLM routing can improve learning assessment workflows.

The core architecture connects:

```text
Learning Content
      ↓
Knowledge Extraction
      ↓
Lesson Context
      ↓
Subject-Aware AI
      ↓
Assessment Generation
      ↓
Evaluation
      ↓
Learning Progress
```

---

# Project Status

This project represents an evolving **AI assessment MVP** developed to demonstrate the core assessment-generation workflow.

The current implementation covers:

**Lesson Upload → Content Processing → Vector Storage → Lesson Context → Subject-Aware LLM → Quiz Generation → Quiz Storage → Submission & Evaluation**

Future LMS integration and additional learning workflows can be built on top of this foundation.

---

# Developed At

**OptimusFox — Lahore, Pakistan**

---

# Author

**Muhammad Arhum**

AI Engineer | LLMs | RAG | Backend Development
