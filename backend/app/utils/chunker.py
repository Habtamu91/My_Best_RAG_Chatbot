"""Text chunking utilities."""
from typing import List
from app.utils.config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_text(text: str, chunk_size: int = None, chunk_overlap: int = None) -> List[str]:
    """
    Split text into overlapping chunks.
    
    Args:
        text: Input text to chunk
        chunk_size: Size of each chunk (default from config)
        chunk_overlap: Overlap between chunks (default from config)
        
    Returns:
        List of text chunks
    """
    if chunk_size is None:
        chunk_size = CHUNK_SIZE
    if chunk_overlap is None:
        chunk_overlap = CHUNK_OVERLAP
    
    if not text or not text.strip():
        return []
    
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        # Calculate end position
        end = start + chunk_size
        
        # Extract chunk
        chunk = text[start:end]
        
        # Try to break at a sentence or paragraph boundary
        if end < text_length:
            # Look for paragraph break first
            last_para = chunk.rfind("\n\n")
            if last_para > chunk_size * 0.5:  # Only break if we're past 50% of chunk
                chunk = chunk[:last_para + 2]
                end = start + last_para + 2
            else:
                # Look for sentence break
                last_period = max(chunk.rfind(". "), chunk.rfind(".\n"))
                if last_period > chunk_size * 0.5:
                    chunk = chunk[:last_period + 2]
                    end = start + last_period + 2
        
        chunks.append(chunk.strip())
        
        # Move start position with overlap
        start = end - chunk_overlap
        if start >= end:  # Prevent infinite loop
            start = end
    
    return chunks if chunks else [text]

