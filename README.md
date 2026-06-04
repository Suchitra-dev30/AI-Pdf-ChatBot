# AI PDF Chatbot (RAG)

An AI-powered PDF chatbot that allows users to upload PDF documents and ask natural language questions about their content.

## Features

* Upload PDF documents
* Extract text from PDFs
* Chunk large documents for efficient retrieval
* Generate embeddings using Gemini Embeddings
* Store vectors in ChromaDB
* Perform semantic search using Retrieval-Augmented Generation (RAG)
* Generate context-aware answers using Gemini
* Display source attribution for retrieved answers
* Streamlit frontend for user interaction
* FastAPI backend for API services

## Tech Stack

* Python
* FastAPI
* Streamlit
* LangChain
* Gemini API
* ChromaDB
* PyPDF

## Project Architecture

PDF Upload
↓
Text Extraction
↓
Chunking
↓
Embeddings
↓
ChromaDB Vector Store
↓
Semantic Retrieval
↓
Gemini LLM
↓
Answer + Source Attribution

## Installation

Clone the repository:

git clone <repository-url>

Create virtual environment:

python -m venv venv

Activate virtual environment:

Windows:
venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

## Environment Variables

Create a .env file:

GOOGLE_API_KEY=your_api_key

## Run Backend

cd backend

uvicorn main:app --reload

Backend runs at:

http://127.0.0.1:8000

## Run Frontend

cd frontend

streamlit run app.py

Frontend runs at:

http://localhost:8501

## Sample Questions

* What was the internship duration?
* What projects were completed?
* What was the intern's performance?

## Future Improvements

* Multi-PDF support
* Chat history
* User authentication
* Cloud deployment
* Advanced document retrieval

## Author

Suchitra
