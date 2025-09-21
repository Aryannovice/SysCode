"""
Demo script for RAG-Enhanced System Design Assistant
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'api'))

from app.rag.ingest import rag_ingestor
from app.rag.query import rag_response_generator, rag_query_engine
from app.rag.config import rag_config
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def demo_rag_setup():
    """Demonstrate RAG system setup and ingestion"""
    print("🚀 RAG-Enhanced System Design Assistant Demo")
    print("=" * 60)
    
    # Check configuration
    print("📋 STEP 1: Configuration Check")
    print("-" * 40)
    config_dict = rag_config.to_dict()
    for key, value in config_dict.items():
        if "api_key" in key.lower():
            value = "***" if value else "Not Set"
        print(f"  {key}: {value}")
    
    config_valid = rag_config.validate()
    print(f"\n✅ Configuration Valid: {config_valid}")
    
    if not config_valid:
        print("\n❌ Configuration issues detected:")
        if not rag_config.openai_api_key:
            print("  - OPENAI_API_KEY environment variable not set")
        if not rag_config.modules_path.exists():
            print(f"  - Modules path does not exist: {rag_config.modules_path}")
        return False
    
    return True

def demo_document_ingestion():
    """Demonstrate document ingestion"""
    print(f"\n📚 STEP 2: Document Ingestion")
    print("-" * 40)
    
    try:
        # Check current collection state
        stats = rag_ingestor.get_collection_stats()
        print(f"Current collection state: {stats.get('total_chunks', 0)} chunks")
        
        # Ingest documents
        print("Starting document ingestion...")
        result = rag_ingestor.ingest_documents(force_refresh=False)
        
        print(f"Ingestion Status: {result['status']}")
        if result['status'] == 'success':
            print(f"  Files Processed: {result['files_processed']}")
            print(f"  Chunks Created: {result['chunks_created']}")
            print(f"  Total Documents: {result['document_count']}")
        elif result['status'] == 'skipped':
            print(f"  Reason: {result['reason']}")
            print(f"  Existing Documents: {result['document_count']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ingestion failed: {e}")
        return False

def demo_vector_search():
    """Demonstrate vector similarity search"""
    print(f"\n🔍 STEP 3: Vector Similarity Search")
    print("-" * 40)
    
    test_queries = [
        "How does caching improve performance?",
        "What is load balancing and when to use it?",
        "Explain consistent hashing in distributed systems",
        "How to handle database scaling?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        try:
            results = rag_query_engine.search_similar_documents(query, top_k=3)
            print(f"Found {len(results)} relevant documents:")
            
            for i, doc in enumerate(results, 1):
                print(f"  {i}. {doc.metadata.get('title', 'Unknown')} "
                      f"(similarity: {doc.similarity_score:.3f})")
                print(f"     Preview: {doc.content[:100]}...")
                
        except Exception as e:
            print(f"❌ Search failed for '{query}': {e}")

def demo_rag_qa():
    """Demonstrate RAG-enhanced question answering"""
    print(f"\n🤖 STEP 4: RAG-Enhanced Q&A")
    print("-" * 40)
    
    test_questions = [
        {
            "question": "What are the trade-offs of using caching in system design?",
            "context": None
        },
        {
            "question": "How do I handle high traffic with load balancing?",
            "context": "URL Shortener: Design a URL shortening service that handles millions of requests"
        },
        {
            "question": "When should I use consistent hashing?",
            "context": "Distributed Cache Service: Design a distributed caching system"
        }
    ]
    
    for i, test_case in enumerate(test_questions, 1):
        print(f"\n--- Question {i} ---")
        print(f"Q: {test_case['question']}")
        if test_case['context']:
            print(f"Context: {test_case['context']}")
        
        try:
            response = rag_response_generator.answer_question(
                question=test_case['question'],
                problem_context=test_case['context']
            )
            
            if response.get("error"):
                print(f"❌ Error: {response['error']}")
                continue
            
            print(f"\nA: {response['answer'][:300]}...")
            print(f"Sources Used: {response.get('retrieved_count', 0)}")
            
            # Show sources
            sources = response.get('sources', [])
            if sources:
                print("Knowledge Sources:")
                for source in sources[:2]:  # Show top 2 sources
                    print(f"  - {source.get('title', 'Unknown')} "
                          f"(score: {source.get('similarity_score', 0):.3f})")
                    
        except Exception as e:
            print(f"❌ Q&A failed: {e}")

def demo_related_topics():
    """Demonstrate related topics discovery"""
    print(f"\n🔗 STEP 5: Related Topics Discovery")
    print("-" * 40)
    
    topics = ["caching", "scaling", "database", "load balancing"]
    
    for topic in topics:
        print(f"\nTopic: '{topic}'")
        try:
            related = rag_response_generator.get_related_topics(topic, limit=3)
            print(f"Found {len(related)} related topics:")
            
            for rel_topic in related:
                print(f"  - {rel_topic.get('title', 'Unknown')} "
                      f"(similarity: {rel_topic.get('similarity_score', 0):.3f})")
                      
        except Exception as e:
            print(f"❌ Related topics search failed for '{topic}': {e}")

def demo_collection_stats():
    """Show collection statistics"""
    print(f"\n📊 STEP 6: Collection Statistics")
    print("-" * 40)
    
    try:
        stats = rag_ingestor.get_collection_stats()
        
        if stats.get("error"):
            print(f"❌ Error getting stats: {stats['error']}")
            return
        
        print(f"Collection Name: {stats.get('collection_name', 'Unknown')}")
        print(f"Total Chunks: {stats.get('total_chunks', 0)}")
        print(f"Source Files: {stats.get('source_count', 0)}")
        
        sample_sources = stats.get('sample_sources', [])
        if sample_sources:
            print(f"Sample Sources: {', '.join(sample_sources[:5])}")
            
    except Exception as e:
        print(f"❌ Stats retrieval failed: {e}")

def main():
    """Run the complete RAG system demo"""
    print("🎯 SYSTEM DESIGN RAG ASSISTANT")
    print("   Complete Retrieval-Augmented Generation Demo")
    print("=" * 60)
    
    # Step 1: Setup validation
    if not demo_rag_setup():
        print("\n❌ Setup validation failed. Please check configuration.")
        return
    
    # Step 2: Document ingestion
    if not demo_document_ingestion():
        print("\n❌ Document ingestion failed.")
        return
    
    # Step 3: Vector search demo
    demo_vector_search()
    
    # Step 4: RAG Q&A demo
    demo_rag_qa()
    
    # Step 5: Related topics
    demo_related_topics()
    
    # Step 6: Statistics
    demo_collection_stats()
    
    print(f"\n🎉 RAG SYSTEM DEMO COMPLETE!")
    print("=" * 60)
    
    print(f"\n📋 NEXT STEPS:")
    next_steps = [
        "1. Set OPENAI_API_KEY environment variable if not already set",
        "2. Start the API server: cd services/api && python -m app.main",
        "3. Test RAG endpoints:",
        "   - POST /api/v1/assistant/ask (Ask questions)",
        "   - GET /api/v1/assistant/status (Check system status)",
        "   - GET /api/v1/rag/search?query=caching (Direct search)",
        "   - POST /api/v1/rag/ingest (Re-ingest documents)",
        "4. Integrate with React frontend ChatBox component",
        "5. Monitor performance and tune similarity thresholds"
    ]
    
    for step in next_steps:
        print(f"   {step}")
    
    print(f"\n✨ RAG CAPABILITIES SUMMARY:")
    capabilities = [
        "🔍 Vector similarity search across 16 system design topics",
        "🤖 Context-aware question answering with source attribution",
        "📚 Automatic document chunking and embedding generation",
        "🔗 Related topics discovery for deeper learning",
        "⚡ Fast retrieval with ChromaDB vector database",
        "🎯 Problem-context enhanced responses",
        "📊 Collection statistics and health monitoring",
        "🔄 Easy document refresh and re-ingestion"
    ]
    
    for capability in capabilities:
        print(f"   {capability}")
    
    print(f"\n🏆 Your System Design Assistant is now RAG-enhanced!")
    print("   Ready to provide intelligent, source-backed answers! 🚀")

if __name__ == "__main__":
    main()

