from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
from rag import rag_service

# Initialize FastAPI App
app = FastAPI(
    title="AI RAG Chatbot API",
    description="Backend for the Industrial Level RAG Chatbot",
    version="1.0.0"
)

# CORS MIDDLEWARE
# Allow the frontend (running on localhost:3000) to talk to this backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DATA MODELS (Pydantic)
# Defines the structure of data we expect to receive.
class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

# ENDPOINTS

@app.get("/")
def read_root():
    return {"status": "active", "message": "Welcome to the RAG Chatbot API"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Endpoint to upload a PDF file.
    It saves the file temporarily and then triggers the ingestion pipeline.
    """
    temp_file = f"temp_{file.filename}"
    
    # Save the file to disk
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Run the RAG ingestion
        num_chunks = rag_service.add_pdf_to_index(temp_file)
        
        # Cleanup
        os.remove(temp_file)
        
        return {
            "filename": file.filename,
            "status": "success",
            "chunks_processed": num_chunks,
            "message": "Document uploaded and indexed successfully."
        }
    except Exception as e:
        if os.path.exists(temp_file):
            os.remove(temp_file)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
def query_document(request: QueryRequest):
    """
    Endpoint to ask a question.
    """
    try:
        answer = rag_service.query_rag(request.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # If this file is run directly, start the server using uvicorn
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
