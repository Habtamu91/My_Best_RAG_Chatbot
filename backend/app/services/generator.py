"""Response generator service using LLM."""
from typing import List, Dict
from app.utils.config import USE_OPENAI, USE_GEMINI, OPENAI_API_KEY, GEMINI_API_KEY, LLM_MODEL, GEMINI_MODEL


class ResponseGenerator:
    """Service for generating responses using LLM."""
    
    def __init__(self):
        self.use_gemini = USE_GEMINI and GEMINI_API_KEY
        self.use_openai = USE_OPENAI and OPENAI_API_KEY
        
        if self.use_gemini:
            try:
                import google.generativeai as genai
                genai.configure(api_key=GEMINI_API_KEY)
                self.genai = genai
                self.model = GEMINI_MODEL
            except ImportError:
                raise RuntimeError(
                    "Google Generative AI library not installed. "
                    "Install it with: pip install google-generativeai"
                )
        elif self.use_openai:
            from openai import OpenAI
            self.client = OpenAI(api_key=OPENAI_API_KEY)
            self.model = LLM_MODEL
        else:
            # Fallback to local model
            self.client = None
            self.genai = None
            self.model = None
    
    def generate_response(self, query: str, context_docs: List[Dict]) -> str:
        """
        Generate a response based on query and retrieved context.
        
        Args:
            query: User's question
            context_docs: Retrieved relevant documents
            
        Returns:
            Generated response
        """
        if not context_docs:
            return "I don't have any relevant information to answer your question. Please upload a PDF document first."
        
        # Prepare context
        context = "\n\n".join([
            f"Document {i+1}:\n{doc['text']}"
            for i, doc in enumerate(context_docs)
        ])
        
        if self.use_gemini:
            # Use Gemini API
            try:
                prompt = f"""You are a helpful assistant that answers questions based on the provided context from uploaded documents.
If the answer cannot be found in the context, say so. Be concise and accurate.

Context from documents:
{context}

Question: {query}

Please provide a clear and accurate answer based on the context above:"""
                
                # Try different model name formats
                model = None
                model_names_to_try = [
                    self.model,  # Try the configured model first
                    "models/gemini-pro",  # Try with models/ prefix
                    "gemini-pro",  # Try without prefix
                    "models/gemini-1.5-flash",  # Try newer model with prefix
                    "gemini-1.5-flash",  # Try newer model without prefix
                ]
                
                for model_name in model_names_to_try:
                    try:
                        model = self.genai.GenerativeModel(model_name)
                        response = model.generate_content(prompt)
                        return response.text.strip()  # Success - return response
                    except:
                        continue
                
                # If all models failed
                raise Exception("Could not find a working Gemini model. Check your API key and available models.")
            except Exception as e:
                return f"Error generating response with Gemini: {str(e)}"
        
        elif self.use_openai:
            # Use OpenAI API
            system_prompt = """You are a helpful assistant that answers questions based on the provided context from uploaded documents. 
            If the answer cannot be found in the context, say so. Be concise and accurate."""
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"}
            ]
            
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=500
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                return f"Error generating response: {str(e)}"
        else:
            # Fallback: Simple template-based response
            return self._generate_template_response(query, context)
    
    def _generate_template_response(self, query: str, context: str) -> str:
        """Generate a simple template-based response when LLM is not available."""
        return f"""Based on the documents provided:

{context[:500]}...

Regarding your question "{query}", the relevant information is contained in the context above. 
For more detailed answers, please configure Gemini API, OpenAI API, or HuggingFace API in your .env file."""


# Global instance
_response_generator = None

def get_response_generator() -> ResponseGenerator:
    """Get or create the global response generator instance."""
    global _response_generator
    if _response_generator is None:
        _response_generator = ResponseGenerator()
    return _response_generator

