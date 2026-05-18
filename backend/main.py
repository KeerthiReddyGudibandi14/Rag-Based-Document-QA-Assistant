import os
import shutil
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from groq import Groq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


load_dotenv()

app = FastAPI(title="RAG-Based Document Q&A Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
DB_DIR = Path("chroma_db")

UPLOAD_DIR.mkdir(exist_ok=True)


class QuestionRequest(BaseModel):
    question: str


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def get_groq_answer(question: str, context: str):
    groq_api_key = os.getenv("GROQ_API_KEY")

    if not groq_api_key:
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY is missing. Please add it to backend/.env",
        )

    client = Groq(api_key=groq_api_key)

    prompt = f"""
You are a helpful AI knowledge assistant.

Rules:
- Do not assume the candidate's gender.
- Do not use pronouns such as he, she, they, him, her, them, his, hers, or their.
- If the candidate's full name is clearly available in the context, start the first sentence with the full name followed by "is".
- Example format: "Keerthi Reddy Gudibandi is a Computer Science graduate student..."
- Do not write awkward phrases like "Name, the candidate, is."
- After the first sentence, refer to the person as "the candidate."
- If the name is not clear, start with "The candidate is..."
- If the answer is not available in the context, say: "The document does not contain enough information."
- Keep the answer concise and directly based on the document.

Document Context:
{context}

User Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You answer questions using only the provided document context. "
                    "Do not make up information."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
        max_tokens=400,
    )

    return response.choices[0].message.content


@app.get("/")
def home():
    return {"message": "RAG-Based Document Q&A Assistant backend is running"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    loader = PyPDFLoader(str(file_path))
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = splitter.split_documents(documents)

    if not chunks:
        raise HTTPException(
            status_code=400,
            detail="No text could be extracted from the PDF.",
        )

    # Clear old vector database so each upload uses the latest document only
    if DB_DIR.exists():
        shutil.rmtree(DB_DIR)

    embeddings = get_embeddings()

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(DB_DIR),
    )

    return {
        "message": "File uploaded and processed successfully",
        "filename": file.filename,
        "chunks_created": len(chunks),
    }


@app.post("/ask")
async def ask_question(request: QuestionRequest):
    if not DB_DIR.exists():
        raise HTTPException(
            status_code=400,
            detail="Please upload and process a document first.",
        )

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    embeddings = get_embeddings()

    vector_db = Chroma(
        persist_directory=str(DB_DIR),
        embedding_function=embeddings,
    )

    retriever = vector_db.as_retriever(search_kwargs={"k": 5})
    retrieved_docs = retriever.invoke(request.question)

    if not retrieved_docs:
        return {
            "question": request.question,
            "answer": "The document does not contain enough information.",
            "retrieved_context": "",
        }

    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    context = context[:5000]

    answer = get_groq_answer(request.question, context)

    return {
        "question": request.question,
        "answer": answer,
        "retrieved_context": context[:1500],
    }