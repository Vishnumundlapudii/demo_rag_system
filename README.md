# 🦜 LangChain Documentation Chatbot

A conversational RAG system built with LangChain and Streamlit that answers questions about LangChain documentation.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Copy `.env` file and add your API keys:
```bash
# For OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# OR for custom E2E endpoint
E2E_LLM_ENDPOINT=https://your-e2e-endpoint.com/v1
E2E_API_KEY=your_e2e_api_key_here
```

### 3. Run the Chatbot
```bash
streamlit run streamlit_app.py
```

## 📁 Project Structure
```
Rag_system/
├── .env                 # Environment configuration
├── requirements.txt     # Python dependencies
├── rag_backend.py      # RAG system backend
├── streamlit_app.py    # Streamlit chat interface
├── chroma_db/          # Vector database (auto-created)
└── README.md           # This file
```

## 🎯 Features

- **💬 Conversational Interface**: Chat with memory using Streamlit
- **📚 LangChain Documentation**: Real-time access to official docs
- **🔍 Source References**: Shows documentation sources for answers
- **🧹 Clear History**: Reset conversation anytime
- **⚡ Fast Setup**: Automatic vector store creation and caching

## 🔧 Configuration Options

Edit `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `E2E_LLM_ENDPOINT` | Custom LLM endpoint | Optional |
| `CHUNK_SIZE` | Text chunk size | 1000 |
| `CHUNK_OVERLAP` | Chunk overlap | 200 |
| `VECTOR_STORE_PATH` | Vector DB path | ./chroma_db |

## 💡 Sample Questions

- "What is LangChain and how does it work?"
- "How do I create a vector store in LangChain?"
- "What are the different types of document loaders?"
- "How does conversational memory work?"
- "What's the difference between chains and agents?"

## 🔄 How It Works

1. **Document Loading**: Scrapes LangChain documentation URLs
2. **Text Processing**: Splits content into manageable chunks
3. **Vector Storage**: Creates embeddings and stores in Chroma DB
4. **Conversational RAG**: Uses memory-enabled retrieval chain
5. **Chat Interface**: Streamlit provides user-friendly interface

## 🛠️ Troubleshooting

- **Vector store issues**: Delete `chroma_db/` folder to rebuild
- **API errors**: Check your API keys in `.env`
- **Memory issues**: Reduce `CHUNK_SIZE` in `.env`
- **Slow responses**: Limit `MAX_DOCS_TO_LOAD` in `.env`

## 📦 Dependencies

- LangChain (core framework)
- Streamlit (web interface)
- ChromaDB (vector storage)
- OpenAI (embeddings & LLM)
- BeautifulSoup (web scraping)