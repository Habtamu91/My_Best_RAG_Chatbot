# RAG Chatbot - PDF Question Answering System

A complete RAG (Retrieval-Augmented Generation) Chatbot that allows users to upload PDF documents and ask questions about them, getting intelligent responses powered by embeddings and LLM.

## 🎯 Features

- **PDF Upload**: Upload PDF documents and automatically extract, chunk, and embed the text
- **Vector Storage**: Store embeddings locally using Chroma or FAISS
- **Intelligent Q&A**: Ask questions about uploaded documents and get context-aware answers
- **Modern UI**: Clean, responsive web interface with chat bubbles and upload section
- **RESTful API**: FastAPI backend with CORS support

## 📁 Project Structure

```
RAG_Chatbot/
│
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI application
│   │   ├── routes/
│   │   │   ├── chat.py             # Chat endpoint
│   │   │   └── upload.py           # Upload endpoint
│   │   ├── services/
│   │   │   ├── embedding.py        # Embedding service
│   │   │   ├── vectorstore.py      # Vector store service
│   │   │   └── generator.py        # LLM response generator
│   │   ├── utils/
│   │   │   ├── pdf_loader.py       # PDF text extraction
│   │   │   ├── chunker.py          # Text chunking
│   │   │   └── config.py           # Configuration
│   │   └── models/
│   │       └── schemas.py          # Pydantic schemas
│   ├── requirements.txt
│   └── run.py                      # Server runner
│
├── frontend/
│   ├── index.html                  # Main HTML
│   ├── style.css                   # Styling
│   ├── script.js                   # Frontend logic
│   └── assets/                     # Static assets
│
├── data/
│   ├── raw/                        # Uploaded PDFs
│   ├── processed/                  # Processed data
│   └── vector_db/                  # Vector database files
│
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip
- A modern web browser

### Step 1: Install Backend Dependencies

```bash
cd RAG_Chatbot/backend
pip install -r requirements.txt
```

### Step 2: Set Up Environment Variables

Create a `.env` file in the `backend` directory (or in the project root):

```env
# OpenAI API Configuration (optional but recommended)
OPENAI_API_KEY=your_openai_api_key_here
USE_OPENAI=true

# HuggingFace API Configuration (optional)
HUGGINGFACE_API_KEY=your_huggingface_api_key_here

# Model Settings
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
LLM_MODEL=gpt-3.5-turbo

# Chunking Settings
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Retrieval Settings
TOP_K_RESULTS=3

# Vector Store Settings (chroma or faiss)
VECTOR_STORE_TYPE=chroma

# Server Settings
HOST=0.0.0.0
PORT=8000
```

**Note**: If you don't have an OpenAI API key, the system will automatically use sentence-transformers for embeddings. However, for the best Q&A experience, an OpenAI API key is recommended for response generation.

### Step 3: Start the Backend Server

```bash
cd RAG_Chatbot/backend
python run.py
```

Or using uvicorn directly:

```bash
cd RAG_Chatbot/backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

### Step 4: Open the Frontend

Open `frontend/index.html` in your web browser. You can:

1. **Double-click** the `index.html` file, or
2. **Serve it via a local server**:
   ```bash
   # Using Python
   cd RAG_Chatbot/frontend
   python -m http.server 8080
   # Then open http://localhost:8080
   ```

### Step 5: Use the Chatbot

1. **Upload a PDF**: Click "Choose PDF file" and select a PDF document
2. **Process**: Click "Upload PDF" to process the document
3. **Ask Questions**: Type your question in the chat input and press Enter or click Send

## 🔧 Configuration Options

### Embedding Models

- **OpenAI** (recommended): Set `USE_OPENAI=true` and provide `OPENAI_API_KEY`
- **Sentence Transformers** (default): Automatically used if OpenAI is not configured

### Vector Stores

- **Chroma** (default): Persistent vector store, recommended for production
- **FAISS**: Fast in-memory search, requires loading/saving index

Set `VECTOR_STORE_TYPE=chroma` or `VECTOR_STORE_TYPE=faiss` in your `.env` file.

### Chunking Settings

Adjust these in `.env`:
- `CHUNK_SIZE`: Size of each text chunk (default: 1000 characters)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 200 characters)

## 📡 API Endpoints

### `POST /api/upload`
Upload a PDF file for processing.

**Request**: `multipart/form-data` with `file` field

**Response**:
```json
{
  "message": "PDF uploaded and processed successfully",
  "filename": "document.pdf",
  "chunks_count": 15
}
```

### `POST /api/chat`
Ask a question about uploaded documents.

**Request**:
```json
{
  "question": "What is the main topic of this document?"
}
```

**Response**:
```json
{
  "answer": "The main topic is...",
  "sources": [
    {
      "text": "Relevant text excerpt...",
      "score": 0.95,
      "metadata": {...}
    }
  ]
}
```

### `GET /health`
Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "message": "RAG Chatbot API is running"
}
```

## 🧩 Technologies Used

### Backend
- **FastAPI**: Modern Python web framework
- **PyPDF2**: PDF text extraction
- **Sentence Transformers**: Local embeddings
- **OpenAI API**: Embeddings and LLM (optional)
- **ChromaDB**: Vector database
- **FAISS**: Alternative vector search (optional)
- **LangChain**: LLM framework components

### Frontend
- **HTML5**: Structure
- **CSS3**: Modern styling with gradients and animations
- **JavaScript**: Fetch API for backend communication

## 🐛 Troubleshooting

### Backend Issues

1. **Import errors**: Make sure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. **Port already in use**: Change the port in `.env` or kill the process using port 8000

3. **Chroma/FAISS errors**: Ensure the `data/vector_db` directory exists and is writable

### Frontend Issues

1. **Cannot connect to API**: 
   - Verify the backend is running on `http://localhost:8000`
   - Check browser console for CORS errors
   - Ensure the API URL in `script.js` matches your backend URL

2. **PDF upload fails**: 
   - Check file size (large files may timeout)
   - Ensure PDF is not corrupted
   - Check backend logs for errors

## 🔐 Security Notes

- The current CORS configuration allows all origins (`*`). For production, update `app/main.py` to specify allowed origins.
- API keys should be kept secure and never committed to version control.
- Consider adding authentication for production deployments.

## 📝 License

This project is open source and available for educational and commercial use.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [LangChain Documentation](https://python.langchain.com/)

---

**Built with ❤️ using FastAPI and modern web technologies**

