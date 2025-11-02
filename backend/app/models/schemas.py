"""Pydantic schemas for request/response models."""
from pydantic import BaseModel
from typing import Optional, List


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    question: str


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    answer: str
    sources: Optional[List[dict]] = None


class UploadResponse(BaseModel):
    """Response model for upload endpoint."""
    message: str
    filename: str
    chunks_count: int


class HealthResponse(BaseModel):
    """Response model for health endpoint."""
    status: str
    message: str

