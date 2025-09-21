"""
Document Ingestion Pipeline for RAG System
"""
import logging
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
import openai
from .config import rag_config

logger = logging.getLogger(__name__)

class DocumentChunk:
    """Represents a document chunk with metadata"""
    
    def __init__(self, content: str, source: str, chunk_id: str, metadata: Dict[str, Any] = None):
        self.content = content
        self.source = source
        self.chunk_id = chunk_id
        self.metadata = metadata or {}
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "content": self.content,
            "source": self.source,
            "chunk_id": self.chunk_id,
            "metadata": self.metadata
        }

class DocumentProcessor:
    """Process markdown documents into chunks"""
    
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks"""
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # Try to break at sentence or paragraph boundaries
            if end < len(text):
                # Look for sentence endings within the last 100 characters
                boundary_search = text[max(end-100, start):end]
                sentence_ends = [i for i, char in enumerate(boundary_search) if char in '.!?\n']
                
                if sentence_ends:
                    # Use the last sentence ending
                    boundary_offset = sentence_ends[-1] + 1
                    end = max(end-100, start) + boundary_offset
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - overlap
            
        return chunks
    
    @staticmethod
    def process_markdown(file_path: Path) -> List[DocumentChunk]:
        """Process a markdown file into chunks"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract title from first header or filename
            lines = content.split('\n')
            title = file_path.stem.replace('_', ' ').replace('-', ' ').title()
            
            for line in lines:
                if line.startswith('# '):
                    title = line[2:].strip()
                    break
            
            # Create chunks
            text_chunks = DocumentProcessor.chunk_text(
                content, 
                rag_config.chunk_size, 
                rag_config.chunk_overlap
            )
            
            document_chunks = []
            for i, chunk_text in enumerate(text_chunks):
                chunk_id = f"{file_path.stem}_{i}"
                
                # Create metadata
                metadata = {
                    "title": title,
                    "filename": file_path.name,
                    "chunk_index": i,
                    "total_chunks": len(text_chunks),
                    "content_hash": hashlib.md5(chunk_text.encode()).hexdigest()[:8]
                }
                
                chunk = DocumentChunk(
                    content=chunk_text,
                    source=str(file_path),
                    chunk_id=chunk_id,
                    metadata=metadata
                )
                document_chunks.append(chunk)
            
            return document_chunks
            
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return []

class RAGIngestor:
    """Manages document ingestion into ChromaDB"""
    
    def __init__(self):
        self.client = None
        self.collection = None
        self.openai_client = None
        self._initialize()
    
    def _initialize(self):
        """Initialize ChromaDB and OpenAI clients"""
        try:
            # Initialize ChromaDB
            self.client = chromadb.PersistentClient(
                path=rag_config.chroma_persist_directory,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Get or create collection
            try:
                self.collection = self.client.get_collection(
                    name=rag_config.collection_name
                )
                logger.info(f"Using existing collection: {rag_config.collection_name}")
            except:
                self.collection = self.client.create_collection(
                    name=rag_config.collection_name,
                    metadata={"description": "System Design Knowledge Base"}
                )
                logger.info(f"Created new collection: {rag_config.collection_name}")
            
            # Initialize OpenAI client
            if rag_config.openai_api_key:
                self.openai_client = openai.OpenAI(api_key=rag_config.openai_api_key)
                logger.info("OpenAI client initialized")
            else:
                logger.warning("OpenAI API key not found")
                
        except Exception as e:
            logger.error(f"Error initializing RAG system: {e}")
            raise
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for texts using OpenAI"""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")
        
        try:
            response = self.openai_client.embeddings.create(
                model=rag_config.embedding_model,
                input=texts
            )
            
            embeddings = [data.embedding for data in response.data]
            logger.info(f"Generated embeddings for {len(texts)} texts")
            return embeddings
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise
    
    def ingest_documents(self, force_refresh: bool = False) -> Dict[str, Any]:
        """Ingest all markdown documents from modules directory"""
        if not rag_config.modules_path.exists():
            raise FileNotFoundError(f"Modules directory not found: {rag_config.modules_path}")
        
        # Check if documents already exist (unless force refresh)
        if not force_refresh and self.collection.count() > 0:
            logger.info("Documents already ingested. Use force_refresh=True to re-ingest.")
            return {
                "status": "skipped",
                "reason": "Documents already exist",
                "document_count": self.collection.count()
            }
        
        # Clear collection if force refresh
        if force_refresh and self.collection.count() > 0:
            self.client.delete_collection(rag_config.collection_name)
            self.collection = self.client.create_collection(
                name=rag_config.collection_name,
                metadata={"description": "System Design Knowledge Base"}
            )
            logger.info("Cleared existing collection for refresh")
        
        # Process all markdown files
        markdown_files = list(rag_config.modules_path.glob("*.md"))
        all_chunks = []
        
        for file_path in markdown_files:
            logger.info(f"Processing {file_path.name}")
            chunks = DocumentProcessor.process_markdown(file_path)
            all_chunks.extend(chunks)
        
        if not all_chunks:
            return {
                "status": "error",
                "reason": "No document chunks generated",
                "document_count": 0
            }
        
        # Prepare data for ChromaDB
        ids = [chunk.chunk_id for chunk in all_chunks]
        documents = [chunk.content for chunk in all_chunks]
        metadatas = [chunk.metadata for chunk in all_chunks]
        
        # Generate embeddings
        logger.info(f"Generating embeddings for {len(documents)} chunks...")
        embeddings = self.generate_embeddings(documents)
        
        # Insert into ChromaDB
        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )
        
        result = {
            "status": "success",
            "files_processed": len(markdown_files),
            "chunks_created": len(all_chunks),
            "document_count": self.collection.count(),
            "collection_name": rag_config.collection_name
        }
        
        logger.info(f"Ingestion complete: {result}")
        return result
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection"""
        if not self.collection:
            return {"error": "Collection not initialized"}
        
        try:
            count = self.collection.count()
            
            # Get sample of documents to analyze
            if count > 0:
                sample = self.collection.get(limit=min(count, 10))
                sources = set()
                for metadata in sample.get('metadatas', []):
                    if 'filename' in metadata:
                        sources.add(metadata['filename'])
                
                return {
                    "total_chunks": count,
                    "collection_name": rag_config.collection_name,
                    "sample_sources": list(sources),
                    "source_count": len(sources),
                    "config": rag_config.to_dict()
                }
            else:
                return {
                    "total_chunks": 0,
                    "collection_name": rag_config.collection_name,
                    "status": "empty"
                }
                
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {"error": str(e)}
    
    def reset_collection(self) -> Dict[str, Any]:
        """Reset the collection (delete all documents)"""
        try:
            if self.collection:
                self.client.delete_collection(rag_config.collection_name)
                self.collection = self.client.create_collection(
                    name=rag_config.collection_name,
                    metadata={"description": "System Design Knowledge Base"}
                )
            
            return {
                "status": "success",
                "message": "Collection reset successfully"
            }
        except Exception as e:
            logger.error(f"Error resetting collection: {e}")
            return {"error": str(e)}

# Global ingestor instance
rag_ingestor = RAGIngestor()

