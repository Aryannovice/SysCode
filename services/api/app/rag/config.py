"""
RAG Configuration for System Design Assistant
"""
import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    # Try loading from current directory
    load_dotenv()

class RAGConfig:
    """Configuration settings for RAG system"""
    
    def __init__(self):
        # OpenAI Settings
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
        self.chat_model = os.getenv("CHAT_MODEL", "gpt-4")
        
        # ChromaDB Settings
        self.chroma_persist_directory = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
        self.collection_name = os.getenv("COLLECTION_NAME", "system_design_knowledge")
        
        # Document Processing Settings
        self.chunk_size = int(os.getenv("CHUNK_SIZE", "1000"))
        self.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "200"))
        
        # Retrieval Settings
        self.top_k_results = int(os.getenv("TOP_K_RESULTS", "5"))
        self.similarity_threshold = float(os.getenv("SIMILARITY_THRESHOLD", "0.3"))
        
        # RAG Settings
        self.max_context_length = int(os.getenv("MAX_CONTEXT_LENGTH", "8000"))
        self.enable_reranking = os.getenv("ENABLE_RERANKING", "true").lower() == "true"
        
        # Paths
        self.modules_path = Path(__file__).parent / "modules"
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary for logging/debugging"""
        return {
            "embedding_model": self.embedding_model,
            "chat_model": self.chat_model,
            "collection_name": self.collection_name,
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "top_k_results": self.top_k_results,
            "similarity_threshold": self.similarity_threshold,
            "max_context_length": self.max_context_length,
            "enable_reranking": self.enable_reranking,
            "modules_path": str(self.modules_path),
            "openai_configured": bool(self.openai_api_key)
        }
    
    def validate(self) -> bool:
        """Validate configuration settings"""
        if not self.openai_api_key:
            return False
        if not self.modules_path.exists():
            return False
        return True

# Global config instance
rag_config = RAGConfig()

