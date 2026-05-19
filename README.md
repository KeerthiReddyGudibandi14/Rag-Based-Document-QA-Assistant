
<h1 align="center">RAG-Based Document Q&A Assistant</h1>

<p align="center">
  <strong>Full-stack RAG application for PDF upload, semantic retrieval, and grounded document question answering.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/ChromaDB-5B21B6?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Hugging%20Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black" />
  <img src="https://img.shields.io/badge/Groq%20LLM-F55036?style=for-the-badge" />
</p>

---

## Overview

The RAG-Based Document Q&A Assistant lets users upload a PDF, ask questions about the document, and receive answers generated from retrieved document context.

The system extracts text from uploaded PDFs, splits the content into chunks, creates local embeddings, stores them in ChromaDB, retrieves the most relevant sections, and uses Groq LLM to generate answers based on the retrieved context.

## Features

- Upload PDF documents through a React frontend
- Extract text from uploaded PDFs
- Split documents into searchable chunks
- Generate local Hugging Face embeddings
- Store and search document vectors using ChromaDB
- Retrieve relevant document context for each question
- Generate grounded answers using Groq LLM
- Display both the final answer and retrieved source context
- Full-stack integration between React frontend and FastAPI backend

## Tech Stack

### Frontend
- React
- JavaScript
- CSS
- Axios

### Backend
- Python
- FastAPI
- REST APIs

### RAG / AI
- LangChain
- ChromaDB
- Hugging Face Embeddings
- Groq LLM

### Document Processing
- PyPDFLoader
- Text Chunking
- Semantic Search

---

## Architecture

```text
PDF Upload
   ↓
Text Extraction
   ↓
Document Chunking
   ↓
Local Hugging Face Embeddings
   ↓
ChromaDB Vector Store
   ↓
Semantic Retrieval
   ↓
Groq LLM Answer Generation
   ↓
Answer + Retrieved Context in UI
