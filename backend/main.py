from fastapi import FastAPI, UploadFile, File
import os
from pydantic import BaseModel
from backend.vector_store import vector_db

from backend.pdf_reader import extract_text_from_pdf
from backend.chunker import chunk_text

app = FastAPI()

chat_history = []

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

class ChatRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "PDF Chatbot Backend Running"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    print("Saving file to:", file_path)

    print(
    "Total docs in DB:",
    vector_db._collection.count()
)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)


    # Extract text from PDF
    text = extract_text_from_pdf(file_path)

    print("Total extracted characters:", len(text))
    print(text[:1000])

    chunks = chunk_text(text)

    print("Created", len(chunks), "chunks")

    for i, chunk in enumerate(chunks, start=1):
        print(f"\nChunk {i}")
        print(chunk)

    if len(chunks) == 0:
        return {
            "filename": file.filename,
            "status": "No readable text found in PDF",
            "chunks": 0
        }

    existing = vector_db._collection.get(
    where={"source": file.filename}
    )

    if existing["ids"]:
        vector_db._collection.delete(
            ids=existing["ids"]
        )

    vector_db.add_texts(
        texts=chunks,
        metadatas=[
            {"source": file.filename}
            for _ in chunks
        ]
    )
    print(
    "Total docs in DB:",
    vector_db._collection.count()
)


    return {
        "filename": file.filename,
        "chunks": len(chunks),
        "status": "uploaded and indexed successfully"
    }


from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)

@app.post("/chat")
async def chat(request: ChatRequest):

    try:

        docs = vector_db.similarity_search(
            request.question,
            k=3
        )

    except Exception as e:

        return {
            "answer": "Service is temporarily unavailable. Please try again later.",
            "source": ""
        }

    if len(docs) == 0:

        return {
            "answer": "No relevant content found. Please upload a PDF first.",
            "source": ""
        }
    
    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )
    history_text = "\n".join(chat_history)

    prompt = f"""
    Previous Conversation:
    {history_text}

    Context:
    {context}

    Question:
    {request.question}

    Answer using the context and conversation history.
    """

    try:
        response = llm.invoke(prompt)

    except Exception:

        return {
            "answer": "Gemini quota exceeded. Please try again later.",
            "source": ""
        }



    source = docs[0].metadata.get(
        "source",
        "Unknown"
    )

    chat_history.append(
        f"User: {request.question}"
    )

    chat_history.append(
        f"Assistant: {response.content}"
    )

    return {
        "answer": response.content,
        "source": source
    }

@app.get("/clear-db")
def clear_db():

    vector_db._collection.delete(
        ids=vector_db.get()["ids"]
    )

    return {"message": "Database cleared"}

@app.get("/stats")
def get_stats():

    return {
        "total_chunks":
        vector_db._collection.count()
    }

