"""Embedding service for generating vector embeddings."""
from typing import List
import numpy as np
from app.utils.config import EMBEDDING_MODEL, USE_OPENAI, USE_GEMINI, OPENAI_API_KEY, GEMINI_API_KEY


class EmbeddingService:
    """Service for generating text embeddings."""
    
    def __init__(self):
        self.model = None
        self.use_openai = False
        self._load_model()
    
    def _load_model(self):
        """Load the embedding model."""
        if USE_GEMINI and GEMINI_API_KEY:
            # Use Gemini embeddings
            self.use_openai = False
            self.use_gemini = True
            try:
                import google.generativeai as genai
                genai.configure(api_key=GEMINI_API_KEY)
                self.genai = genai
            except ImportError:
                raise RuntimeError(
                    "Google Generative AI library not installed. "
                    "Install it with: pip install google-generativeai"
                )
        elif USE_OPENAI and OPENAI_API_KEY:
            # Use OpenAI embeddings
            self.use_openai = True
            self.use_gemini = False
        else:
            # Use sentence-transformers as fallback (local, free)
            self.use_openai = False
            self.use_gemini = False
            try:
                from sentence_transformers import SentenceTransformer
                self.model = SentenceTransformer(EMBEDDING_MODEL)
            except ImportError as e:
                raise RuntimeError(
                    f"Failed to import sentence-transformers: {str(e)}\n"
                    "Install it with: pip install sentence-transformers\n"
                    "Or configure Gemini/OpenAI API key in .env file"
                )
            except Exception as e:
                raise RuntimeError(f"Failed to load embedding model: {str(e)}")
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector as list of floats
        """
        if self.use_gemini:
            # Use Gemini embeddings
            try:
                result = self.genai.embed_content(
                    model="models/text-embedding-004",
                    content=text
                )
                return result['embedding']
            except Exception as e:
                raise RuntimeError(f"Error generating Gemini embedding: {str(e)}")
        elif self.use_openai:
            # Use OpenAI embeddings
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        else:
            # Use sentence-transformers (local, free)
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding.tolist()
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of input texts
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
        
        if self.use_gemini:
            # Use Gemini embeddings (batch)
            embeddings = []
            for text in texts:
                try:
                    result = self.genai.embed_content(
                        model="models/text-embedding-004",
                        content=text
                    )
                    embeddings.append(result['embedding'])
                except Exception as e:
                    raise RuntimeError(f"Error generating Gemini embedding: {str(e)}")
            return embeddings
        elif self.use_openai:
            # Use OpenAI embeddings
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=texts
            )
            return [item.embedding for item in response.data]
        else:
            # Use sentence-transformers (batch processing, local, free)
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            return embeddings.tolist()


# Global instance
_embedding_service = None

def get_embedding_service() -> EmbeddingService:
    """Get or create the global embedding service instance."""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service

