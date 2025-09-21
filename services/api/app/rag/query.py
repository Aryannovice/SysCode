"""
RAG Query Engine for System Design Assistant
"""
import logging
from typing import List, Dict, Any, Optional, Tuple
import openai
from .config import rag_config
from .ingest import rag_ingestor

logger = logging.getLogger(__name__)

class RetrievedDocument:
    """Represents a retrieved document with similarity score"""
    
    def __init__(self, content: str, metadata: Dict[str, Any], similarity_score: float, chunk_id: str):
        self.content = content
        self.metadata = metadata
        self.similarity_score = similarity_score
        self.chunk_id = chunk_id
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "content": self.content,
            "metadata": self.metadata,
            "similarity_score": self.similarity_score,
            "chunk_id": self.chunk_id
        }

class RAGQueryEngine:
    """Handles vector similarity search and context retrieval"""
    
    def __init__(self):
        self.ingestor = rag_ingestor
        self.openai_client = None
        self._initialize()
    
    def _initialize(self):
        """Initialize OpenAI client"""
        if rag_config.openai_api_key:
            self.openai_client = openai.OpenAI(api_key=rag_config.openai_api_key)
            logger.info("RAG Query Engine initialized")
        else:
            logger.warning("OpenAI API key not found for RAG queries")
    
    def generate_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for a query string"""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")
        
        try:
            response = self.openai_client.embeddings.create(
                model=rag_config.embedding_model,
                input=[query]
            )
            
            return response.data[0].embedding
            
        except Exception as e:
            logger.error(f"Error generating query embedding: {e}")
            raise
    
    def search_similar_documents(self, query: str, top_k: int = None, filters: Dict[str, Any] = None) -> List[RetrievedDocument]:
        """Search for similar documents using vector similarity"""
        if not self.ingestor.collection:
            raise ValueError("Document collection not initialized")
        
        top_k = top_k or rag_config.top_k_results
        
        try:
            # Generate query embedding
            query_embedding = self.generate_query_embedding(query)
            
            # Prepare ChromaDB query parameters
            query_params = {
                "query_embeddings": [query_embedding],
                "n_results": top_k
            }
            
            # Add metadata filters if provided
            if filters:
                query_params["where"] = filters
            
            # Perform similarity search
            results = self.ingestor.collection.query(**query_params)
            
            # Process results
            retrieved_docs = []
            
            if results and results.get('documents') and results['documents'][0]:
                documents = results['documents'][0]
                metadatas = results.get('metadatas', [None])[0] or []
                distances = results.get('distances', [None])[0] or []
                ids = results.get('ids', [None])[0] or []
                
                for i, (doc, metadata, distance, doc_id) in enumerate(zip(documents, metadatas, distances, ids)):
                    # Convert distance to similarity score (assuming cosine distance)
                    similarity_score = 1.0 - distance if distance is not None else 0.0
                    
                    # Filter by similarity threshold
                    if similarity_score >= rag_config.similarity_threshold:
                        retrieved_doc = RetrievedDocument(
                            content=doc,
                            metadata=metadata or {},
                            similarity_score=similarity_score,
                            chunk_id=doc_id
                        )
                        retrieved_docs.append(retrieved_doc)
            
            logger.info(f"Retrieved {len(retrieved_docs)} relevant documents for query: '{query[:100]}...'")
            return retrieved_docs
            
        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            return []
    
    def search_by_topic(self, topic: str, top_k: int = None) -> List[RetrievedDocument]:
        """Search documents by specific system design topic"""
        # Skip filters for now due to ChromaDB version compatibility
        return self.search_similar_documents(
            query=f"system design {topic} architecture patterns best practices",
            top_k=top_k
        )
    
    def get_context_for_question(self, question: str, problem_context: str = None) -> Dict[str, Any]:
        """Get relevant context for answering a question"""
        try:
            # Enhance query with problem context if provided
            enhanced_query = question
            if problem_context:
                enhanced_query = f"{problem_context} {question}"
            
            # Search for relevant documents
            retrieved_docs = self.search_similar_documents(enhanced_query)
            
            if not retrieved_docs:
                return {
                    "context": "",
                    "sources": [],
                    "retrieved_count": 0,
                    "query": enhanced_query
                }
            
            # Combine relevant content
            context_parts = []
            sources = []
            
            for doc in retrieved_docs:
                # Add document content
                context_parts.append(f"## {doc.metadata.get('title', 'Unknown Topic')}\n{doc.content}")
                
                # Track sources
                source_info = {
                    "title": doc.metadata.get('title', 'Unknown'),
                    "filename": doc.metadata.get('filename', 'unknown.md'),
                    "similarity_score": doc.similarity_score,
                    "chunk_id": doc.chunk_id
                }
                sources.append(source_info)
            
            # Combine context with length limit
            full_context = "\n\n".join(context_parts)
            
            # Truncate if too long
            if len(full_context) > rag_config.max_context_length:
                full_context = full_context[:rag_config.max_context_length] + "..."
                logger.info(f"Context truncated to {rag_config.max_context_length} characters")
            
            return {
                "context": full_context,
                "sources": sources,
                "retrieved_count": len(retrieved_docs),
                "query": enhanced_query,
                "total_tokens_estimate": len(full_context) // 4  # Rough token estimate
            }
            
        except Exception as e:
            logger.error(f"Error getting context for question: {e}")
            return {
                "context": "",
                "sources": [],
                "retrieved_count": 0,
                "error": str(e)
            }

class RAGResponseGenerator:
    """Generates responses using retrieved context and LLM"""
    
    def __init__(self):
        self.query_engine = RAGQueryEngine()
        self.openai_client = None
        self._initialize()
    
    def _initialize(self):
        """Initialize OpenAI client"""
        if rag_config.openai_api_key:
            self.openai_client = openai.OpenAI(api_key=rag_config.openai_api_key)
            logger.info("RAG Response Generator initialized")
        else:
            logger.warning("OpenAI API key not found for response generation")
    
    def answer_question(self, question: str, problem_context: str = None, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """Generate an answer using RAG approach"""
        if not self.openai_client:
            return {
                "answer": "RAG system not available - OpenAI API key required",
                "sources": [],
                "error": "OpenAI client not initialized"
            }
        
        try:
            # Get relevant context
            context_data = self.query_engine.get_context_for_question(question, problem_context)
            
            if context_data.get("error"):
                return {
                    "answer": "I'm sorry, I couldn't retrieve relevant information to answer your question.",
                    "sources": [],
                    "error": context_data["error"]
                }
            
            # Prepare prompt
            system_prompt = self._create_system_prompt()
            user_prompt = self._create_user_prompt(question, context_data["context"], problem_context)
            
            # Prepare conversation messages
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history[-4:])  # Last 4 exchanges
            
            messages.append({"role": "user", "content": user_prompt})
            
            # Generate response
            response = self.openai_client.chat.completions.create(
                model=rag_config.chat_model,
                messages=messages,
                temperature=0.3,
                max_tokens=1500
            )
            
            answer = response.choices[0].message.content
            
            return {
                "answer": answer,
                "sources": context_data["sources"],
                "retrieved_count": context_data["retrieved_count"],
                "context_length": len(context_data["context"]),
                "query_used": context_data["query"]
            }
            
        except Exception as e:
            logger.error(f"Error generating RAG response: {e}")
            return {
                "answer": "I encountered an error while processing your question. Please try again.",
                "sources": [],
                "error": str(e)
            }
    
    def _create_system_prompt(self) -> str:
        """Create system prompt for RAG responses"""
        return """You are an expert system design consultant with deep knowledge of distributed systems, scalability patterns, and architectural best practices.

Your role is to provide clear, practical, and educational answers about system design concepts. Use the provided context from our knowledge base to give accurate information, but also apply your expertise to provide comprehensive explanations.

Guidelines:
- Provide clear, well-structured explanations
- Use real-world examples when helpful
- Mention trade-offs and considerations
- Be practical and actionable in your advice
- If the context doesn't fully cover the question, acknowledge this and provide your best general guidance
- Keep responses focused and educational
- Use bullet points or numbered lists for clarity when appropriate

Always aim to help the user understand not just the "what" but also the "why" and "when" of system design decisions."""
    
    def _create_user_prompt(self, question: str, context: str, problem_context: str = None) -> str:
        """Create user prompt with question and context"""
        prompt_parts = []
        
        if problem_context:
            prompt_parts.append(f"Context: The user is working on a system design problem: {problem_context}")
        
        if context.strip():
            prompt_parts.append(f"Relevant Knowledge Base Information:\n{context}")
        else:
            prompt_parts.append("Note: No specific information was found in the knowledge base for this question. Please provide your best general guidance on this system design topic.")
        
        prompt_parts.append(f"Question: {question}")
        
        return "\n\n".join(prompt_parts)
    
    def get_related_topics(self, topic: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get related system design topics"""
        try:
            retrieved_docs = self.query_engine.search_by_topic(topic, top_k=limit)
            
            related_topics = []
            for doc in retrieved_docs:
                topic_info = {
                    "title": doc.metadata.get('title', 'Unknown Topic'),
                    "filename": doc.metadata.get('filename', 'unknown.md'),
                    "similarity_score": doc.similarity_score,
                    "preview": doc.content[:200] + "..." if len(doc.content) > 200 else doc.content
                }
                related_topics.append(topic_info)
            
            return related_topics
            
        except Exception as e:
            logger.error(f"Error getting related topics: {e}")
            return []

# Global instances
rag_query_engine = RAGQueryEngine()
rag_response_generator = RAGResponseGenerator()

