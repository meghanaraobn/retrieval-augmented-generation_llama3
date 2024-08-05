from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from huggingface_hub import login
from app.index_manager import IndexManager
from app.index_query_service import IndexQueryService
from app.index_service_context_loader import IndexServiceContextLoader
import os

app = FastAPI()

# Global variables for services
index_manager: IndexManager = None
index_query_service: IndexQueryService = None
index_service_context_loader: IndexServiceContextLoader = None

@app.on_event("startup")
def startup_event():
    global index_service_context_loader, index_manager, index_query_service

    try:
        # Load environment variables
        load_dotenv()
        
        # Hugging Face login
        hf_token = os.getenv('HF_TOKEN')
        if hf_token is None:
            raise ValueError("Hugging Face token not set in environment variables")
        login(token=hf_token)
        
        # Initialize services
        index_service_context_loader = IndexServiceContextLoader()
        index_manager = IndexManager(index_service_context_loader)
        index_query_service = IndexQueryService(index_service_context_loader)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Startup failed: {str(e)}")

@app.on_event("shutdown")
def shutdown_event():
    global index_service_context_loader, index_manager, index_query_service

    # Clean up resources
    index_service_context_loader = None
    index_manager = None
    index_query_service = None

@app.get("/")
async def read_root():
    return {"message": "Retrieval Augmented Generation (RAG)!"}

@app.post("/create_index")
async def create_index(document_path: str):
    """
    Create an index for the given document.

    Args:
        document_path (str): The document to be indexed.

    Returns:
        JSONResponse: A response indicating success or failure.
    """
    global index_manager
    try:
        index_manager.create_document_index(document_path)
        return JSONResponse(status_code=200, content={"message": "Document indexed successfully."})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete_index/{ref_document_id}")
async def delete_index(ref_document_id: str):
    """
    Delete a document from the index based on the reference document id.

    Args:
        ref_document_id (str): The id of the document to be deleted from the index.

    Returns:
        JSONResponse: A response indicating the result of the deletion.
    """
    global index_manager
    try:
        index_manager.delete_document_index(ref_document_id)
        return JSONResponse(status_code=200, content={"message": f"Deleted document from index with id: {ref_document_id}"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query_documents")
async def query_documents(query_string: str):
    """
    Query the indexed documents with the provided query string.

    Args:
        query_string (str): The query string to search in the indexed documents.

    Returns:
        JSONResponse: A response containing the detailed results for the query.
    """
    global index_query_service
    try:
        response = index_query_service.query_documents(query_string)
        return JSONResponse(status_code=200, content=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))