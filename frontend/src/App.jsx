import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [uploadMessage, setUploadMessage] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [retrievedContext, setRetrievedContext] = useState("");
  const [loadingUpload, setLoadingUpload] = useState(false);
  const [loadingAnswer, setLoadingAnswer] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      setUploadMessage("Please select a PDF file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoadingUpload(true);
      setUploadMessage("");

      const response = await axios.post(
        "http://127.0.0.1:8000/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setUploadMessage(
  `${response.data.filename} processed successfully. Ready for questions.`
);
    } catch (error) {
      setUploadMessage("Upload failed. Please check backend server.");
    } finally {
      setLoadingUpload(false);
    }
  };

  const handleAsk = async () => {
    if (!question.trim()) {
      setAnswer("Please enter a question.");
      return;
    }

    try {
      setLoadingAnswer(true);
      setAnswer("");

      const response = await axios.post("http://127.0.0.1:8000/ask", {
        question,
      });

      setAnswer(response.data.answer);
      setRetrievedContext(response.data.retrieved_context || "");
    } catch (error) {
      setAnswer("Please upload and process a document before asking a question.");
      setRetrievedContext("");
    } finally {
      setLoadingAnswer(false);
    }
  };

  return (
    <div className="app">
      <div className="container">
        <p className="badge">Fullstack-GenAI</p>

        <h1>RAG-Based Document Q&A Assistant</h1>

        <p className="subtitle">
          Upload a PDF document, ask questions, and get context-aware answers
          using retrieval-augmented generation.
        </p>

        <div className="card">
          <h2>Upload Document</h2>
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setFile(e.target.files[0])}
          />
          <button onClick={handleUpload} disabled={loadingUpload}>
            {loadingUpload ? "Processing..." : "Upload & Process"}
          </button>
          {uploadMessage && <p className="message">{uploadMessage}</p>}
        </div>

        <div className="card">
          <h2>Ask a Question</h2>
          <textarea
            placeholder="Ask something about the uploaded document..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />
          <button onClick={handleAsk} disabled={loadingAnswer}>
            {loadingAnswer ? "Generating..." : "Ask Question"}
          </button>

          {answer && (
  <div className="answer">
    <h3>Answer</h3>
    <p>{answer}</p>
  </div>
)}

{retrievedContext && (
  <div className="context-box">
    <h3>Retrieved Context</h3>
    <p>
      These are the most relevant document sections retrieved from the vector
      database before generating the answer.
    </p>
    <pre>{retrievedContext}</pre>
  </div>
)}
        </div>
      </div>
    </div>
  );
}

export default App;