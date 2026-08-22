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
