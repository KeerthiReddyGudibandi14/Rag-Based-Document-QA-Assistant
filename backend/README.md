# RAG-Based Document Q&A Assistant

A full-stack RAG application that lets users upload PDF documents, retrieve relevant context using local Hugging Face embeddings and ChromaDB, and generate grounded answers using Groq LLM.

## Tech Stack

- React
- FastAPI
- LangChain
- ChromaDB
- Hugging Face Embeddings
- Groq API

## Features

- PDF upload
- Text extraction
- Document chunking
- Local embedding generation
- Vector search with ChromaDB
- Groq-powered answer generation
- Retrieved context display

## How to Run

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload