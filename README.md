## ✨ Current Features

### 🔍 Research Discovery

- Search research papers by topic using arXiv
- View paper metadata
  - Title
  - Authors
  - Publication Date
  - Categories
  - Abstract
- Open paper PDF directly
- View paper on arXiv
- Search using Enter key or Search button
- Graceful error handling

### 📄 Paper Analysis

- Upload research papers
- Validate PDF files
- Parse documents using PyMuPDF
- Extract text
- Extract metadata
- Preview extracted content

### 📄 Research Discovery

- Search research papers from arXiv
- View paper metadata
- Browse abstracts
- Explore research topics

### 📑 Document Processing

- Secure PDF upload
- Automatic PDF validation
- PDF parsing using PyMuPDF
- Metadata extraction
- Text extraction
- Character statistics

### ✂️ Intelligent Chunking

- Recursive Character Text Splitter
- Configurable chunk size
- Chunk overlap
- Chunk Inspector
- Chunk Statistics
- Average chunk size

### 🧠 Semantic Embeddings

- BAAI/bge-small-en-v1.5
- Sentence Transformers
- Normalized embeddings
- Embedding metrics
- Vector dimension reporting

### 🗄️ Vector Store

- FAISS IndexFlatIP
- Persistent vector index
- Metadata persistence
- Vector Store dashboard
- Index validation

### 🔎 Semantic Retrieval

- Query embeddings
- FAISS similarity search
- Similarity threshold filtering
- Semantic search UI
- Top-K retrieval

### 🧠 Basic RAG

- Retrieval-Augmented Generation
- Ollama LLM integration
- gpt-oss:120b-cloud
- Grounded document answers
- Semantic retrieval
- Similarity threshold filtering
- Source chunk display
- Environment-based model configuration

### 🧠 Basic RAG

- Retrieval-Augmented Generation
- Ollama LLM integration
- Centralized LLM configuration
- `gpt-oss:120b-cloud`
- Grounded document answers
- Semantic retrieval
- Similarity threshold filtering
- Context-aware prompting
- Source chunk display
- RAGService orchestration
- LLMService abstraction

### 💬 Conversational RAG & Chat

- Conversational RAG
- Document-scoped chat sessions
- Conversation-aware query contextualization
- Follow-up question handling
- `ChatService`
- `ChatSession` model
- Multiple independent conversations
- Chat history panel
- New Chat functionality
- Document-specific retrieval
- ChatGPT-style conversation interface
- Retrieved source display

### 🗄️ Persistent Chat & Database

- SQLite database
- `DatabaseService`
- `ChatRepository`
- Persistent chat sessions
- Persistent chat messages
- Chat restoration after application restart
- Chat and message relationships
- Database-backed chat history
- Chat timestamps
- Persistent chat CRUD foundation

### 💬 Chat with Paper

- Persistent document-based chat sessions
- Choose an existing research paper or upload a new one
- End-to-end PDF processing from the chat workflow
- Automatic parsing, chunking, embedding, and vector storage
- Context-aware conversational RAG
- Follow-up question contextualization
- Persistent chat history and messages
- Document-grounded AI responses
- Source chunk display with similarity scores
- Create multiple chats across research papers
- Duplicate chat prevention
- Rename chat conversations
- Delete chats with associated messages
- SQLite-backed chat persistence
- FAISS vector store integration

### ⚖️ Compare Papers

- Select and compare two different research papers.
- Compare research objectives.
- Compare methodologies.
- Compare key findings.
- Compare strengths and limitations.
- Compare conclusions.
- Ask custom comparison questions.
- Retrieve evidence independently from both papers.
- Generate AI-powered, evidence-grounded comparisons.

### 🔍 Retrieval Debugger

- Interactive semantic retrieval testing
- Research paper selection
- Adjustable Top K retrieval
- Adjustable similarity threshold
- Query embedding inspection
- Total vector count visibility
- Retrieved result count
- Ranked chunk results
- Similarity score visualization
- Chunk ID and character range inspection
- Retrieved content preview
- Irrelevant query validation
- Threshold-based retrieval testing

### 💡 Research Insights

- Interactive AI-powered research insight generation
- Research paper selection
- Semantic evidence retrieval from selected papers
- Multiple targeted retrieval queries for broader paper coverage
- Executive summary generation
- Research problem identification
- Research objectives extraction
- Methodology analysis
- Key findings identification
- Research limitations detection
- Research gap identification
- Practical impact analysis
- Key takeaways generation
- Grounded insights based on retrieved paper evidence
- Structured Pydantic-based insight generation
- JSON response validation and parsing
- Session-state persistence for generated insights

### 🎓 Learning Center

- Interactive AI-powered learning experience for research papers
- Research paper selection
- Beginner, Intermediate, and Advanced learning levels
- Difficulty-based AI-generated learning material
- Multi-query semantic evidence retrieval
- Simplified research paper explanation
- Key concept extraction and explanation
- Interactive expandable concept learning
- AI-generated question and answer flashcards
- Interactive answer reveal functionality
- AI-generated multiple-choice knowledge quiz
- Four options for each quiz question
- Correct answer validation
- Quiz completion validation
- Automatic score and percentage calculation
- Visual quiz progress indicator
- Correct and incorrect answer review
- Answer explanations for better understanding
- Quiz retake functionality
- Grounded learning content based on retrieved paper evidence
- Structured Pydantic-based learning content validation
- JSON response parsing and validation
- Session-state handling for learning material and quiz results

### 📊 Presentation Generator

- AI-generated presentations from research papers
- Research paper selection
- Multiple presentation types
- Adjustable slide count
- Grounded evidence retrieval from the selected paper
- Representative evidence collection across key research areas
- Context-aware presentation generation
- Research Summary presentation mode
- Academic Presentation mode
- Executive Summary presentation mode
- Educational Presentation mode
- Structured AI-generated presentation content
- Pydantic validation for presentation responses
- Strict JSON response parsing
- Invalid AI response handling
- Grounded content generation to reduce hallucinations
- Slide-by-slide presentation preview
- Expandable slide content inspection
- Slide titles and concise bullet points
- AI-generated speaker notes
- Real PowerPoint `.pptx` export
- Automatic title slide generation
- 16:9 widescreen PowerPoint layout
- Generated content slides
- Bullet point formatting
- Slide numbering
- Unique timestamped export filenames
- Downloadable PowerPoint presentations

### 🔄 Agent Workflow

- Core ResearchPilot pipeline visualization
- Document processing workflow
- Document chunking visualization
- Embedding generation workflow
- Document-scoped vector storage explanation
- Semantic evidence retrieval workflow
- Grounded AI analysis visualization
- Research output workflow
- Step-by-step pipeline overview
- Research Insights workflow
- Compare Papers workflow
- Chat with Paper workflow
- Learning Center workflow
- Presentation Generator workflow
- Clear explanation of the grounded AI approach
- Architecture-focused workflow inspection
