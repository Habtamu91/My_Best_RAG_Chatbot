"""PDF loading utilities using PyPDF2."""
from pathlib import Path
from typing import List
import PyPDF2
from io import BytesIO


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extract text from PDF bytes.
    
    Args:
        pdf_bytes: PDF file as bytes
        
    Returns:
        Extracted text as a single string
    """
    text_content = []
    
    try:
        pdf_file = BytesIO(pdf_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            if text.strip():
                text_content.append(text)
    
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {str(e)}")
    
    return "\n\n".join(text_content)


def save_pdf_to_disk(pdf_bytes: bytes, filename: str, save_dir: Path) -> Path:
    """
    Save PDF to disk.
    
    Args:
        pdf_bytes: PDF file as bytes
        filename: Original filename
        save_dir: Directory to save the PDF
        
    Returns:
        Path to saved file
    """
    save_dir.mkdir(parents=True, exist_ok=True)
    file_path = save_dir / filename
    
    with open(file_path, "wb") as f:
        f.write(pdf_bytes)
    
    return file_path

