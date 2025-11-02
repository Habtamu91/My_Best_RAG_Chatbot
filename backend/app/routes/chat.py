"""Chat route for handling questions and generating responses."""
from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.services.vectorstore import get_vector_store
from app.services.generator import get_response_generator

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a user question and generate a response using RAG.
    
    Args:
        request: ChatRequest with user question
        
    Returns:
        ChatResponse with answer and sources
    """
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        # Get vector store and search for relevant documents
        vector_store = get_vector_store()
        
        # Check if vector store has any documents
        if vector_store.use_chroma:
            # For Chroma, we can check collection count
            collection = vector_store.collection
            if collection.count() == 0:
                return ChatResponse(
                    answer="No documents have been uploaded yet. Please upload a PDF document first.",
                    sources=[]
                )
        else:
            # For FAISS, check if index has vectors
            if vector_store.index.ntotal == 0:
                return ChatResponse(
                    answer="No documents have been uploaded yet. Please upload a PDF document first.",
                    sources=[]
                )
        
        # Search for relevant documents
        relevant_docs = vector_store.search(request.question)
        
        if not relevant_docs:
            return ChatResponse(
                answer="I couldn't find relevant information to answer your question. Please try rephrasing your question or upload more documents.",
                sources=[]
            )
        
        # Generate response using LLM
        generator = get_response_generator()
        answer = generator.generate_response(request.question, relevant_docs)
        
        # Prepare sources
        sources = [
            {
                "text": doc['text'][:200] + "..." if len(doc['text']) > 200 else doc['text'],
                "score": doc['score'],
                "metadata": doc.get('metadata', {})
            }
            for doc in relevant_docs
        ]
        
        return ChatResponse(
            answer=answer,
            sources=sources
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")

