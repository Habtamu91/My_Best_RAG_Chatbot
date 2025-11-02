"""Upload route for handling PDF uploads."""
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import UploadResponse
from app.utils.pdf_loader import extract_text_from_pdf, save_pdf_to_disk
from app.utils.chunker import chunk_text
from app.services.vectorstore import get_vector_store
from app.utils.config import RAW_DATA_DIR

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file, extract text, chunk it, and store embeddings.
    
    Args:
        file: Uploaded PDF file
        
    Returns:
        UploadResponse with upload details
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Save to disk
        file_path = save_pdf_to_disk(file_content, file.filename, RAW_DATA_DIR)
        
        # Extract text from PDF
        text = extract_text_from_pdf(file_content)
        
        if not text or not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
        # Chunk text
        chunks = chunk_text(text)
        
        if not chunks:
            raise HTTPException(status_code=400, detail="Failed to chunk document")
        
        # Get vector store and add documents
        vector_store = get_vector_store()
        metadatas = [
            {"filename": file.filename, "chunk_index": i}
            for i in range(len(chunks))
        ]
        doc_ids = vector_store.add_documents(chunks, metadatas)
        
        return UploadResponse(
            message="PDF uploaded and processed successfully",
            filename=file.filename,
            chunks_count=len(chunks)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

