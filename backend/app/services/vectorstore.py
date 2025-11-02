"""Vector store service for storing and retrieving embeddings."""
from typing import List, Dict, Optional
import uuid
from pathlib import Path
from app.utils.config import VECTOR_DB_DIR, VECTOR_STORE_TYPE, TOP_K_RESULTS
from app.services.embedding import get_embedding_service


class VectorStore:
    """Vector store for managing document embeddings."""
    
    def __init__(self):
        self.store_type = VECTOR_STORE_TYPE.lower()
        self.embedding_service = get_embedding_service()
        
        if self.store_type == "chroma":
            self._init_chroma()
        else:
            self._init_faiss()
    
    def _init_chroma(self):
        """Initialize Chroma vector store."""
        try:
            import chromadb
            from chromadb.config import Settings
            
            self.client = chromadb.PersistentClient(
                path=str(VECTOR_DB_DIR / "chroma"),
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name="rag_chatbot",
                metadata={"hnsw:space": "cosine"}
            )
            self.use_chroma = True
        except ImportError:
            raise ImportError("Chroma not installed. Install with: pip install chromadb")
    
    def _init_faiss(self):
        """Initialize FAISS vector store."""
        try:
            import faiss
            import numpy as np
            import pickle
            
            # Make faiss available to class
            self.faiss = faiss
            
            self.index_file = VECTOR_DB_DIR / "faiss_index.bin"
            self.metadata_file = VECTOR_DB_DIR / "faiss_metadata.pkl"
            
            # Get embedding dimension
            test_embedding = self.embedding_service.embed_text("test")
            self.dimension = len(test_embedding)
            
            # Load or create FAISS index
            if self.index_file.exists():
                self.index = faiss.read_index(str(self.index_file))
                with open(self.metadata_file, "rb") as f:
                    self.metadata = pickle.load(f)
            else:
                self.index = faiss.IndexFlatIP(self.dimension)  # Inner product for cosine similarity
                self.metadata = []
            
            self.use_chroma = False
        except ImportError:
            raise ImportError("FAISS not installed. Install with: pip install faiss-cpu")
    
    def add_documents(self, texts: List[str], metadatas: Optional[List[Dict]] = None) -> List[str]:
        """
        Add documents to the vector store.
        
        Args:
            texts: List of text chunks to add
            metadatas: Optional list of metadata dicts
            
        Returns:
            List of document IDs
        """
        if not texts:
            return []
        
        # Generate embeddings
        embeddings = self.embedding_service.embed_documents(texts)
        
        if self.use_chroma:
            # Add to Chroma
            ids = [str(uuid.uuid4()) for _ in texts]
            if metadatas is None:
                metadatas = [{}] * len(texts)
            
            self.collection.add(
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            return ids
        else:
            # Add to FAISS
            import numpy as np
            import pickle
            
            ids = []
            for i, (text, embedding, metadata) in enumerate(zip(texts, embeddings, metadatas or [{}] * len(texts))):
                doc_id = str(uuid.uuid4())
                ids.append(doc_id)
                
                # Add embedding to index
                embedding_array = np.array([embedding], dtype=np.float32)
                # Normalize for cosine similarity
                import faiss
                faiss.normalize_L2(embedding_array)
                self.index.add(embedding_array)
                
                # Store metadata
                metadata['id'] = doc_id
                metadata['text'] = text
                self.metadata.append(metadata)
            
            # Save index and metadata
            import faiss
            import pickle
            faiss.write_index(self.index, str(self.index_file))
            with open(self.metadata_file, "wb") as f:
                pickle.dump(self.metadata, f)
            
            return ids
    
    def search(self, query: str, top_k: int = None) -> List[Dict]:
        """
        Search for similar documents.
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of similar documents with scores
        """
        if top_k is None:
            top_k = TOP_K_RESULTS
        
        # Generate query embedding
        query_embedding = self.embedding_service.embed_text(query)
        
        if self.use_chroma:
            # Search Chroma
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            
            documents = []
            if results['ids'] and results['ids'][0]:
                for i in range(len(results['ids'][0])):
                    documents.append({
                        'text': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'score': 1 - results['distances'][0][i]  # Convert distance to similarity
                    })
            return documents
        else:
            # Search FAISS
            import numpy as np
            import faiss
            
            query_array = np.array([query_embedding], dtype=np.float32)
            faiss.normalize_L2(query_array)
            
            scores, indices = self.index.search(query_array, min(top_k, self.index.ntotal))
            
            documents = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(self.metadata):
                    doc = {
                        'text': self.metadata[idx]['text'],
                        'metadata': self.metadata[idx],
                        'score': float(score)
                    }
                    documents.append(doc)
            
            return documents


# Global instance
_vector_store = None

def get_vector_store() -> VectorStore:
    """Get or create the global vector store instance."""
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store

