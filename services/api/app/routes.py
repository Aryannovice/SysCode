from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
import asyncio
import logging

# Import services with error handling
try:
    from .schemas import DesignRequest, DesignResponse, FeedbackRequest
except ImportError as e:
    logging.warning(f"Could not import schemas: {e}")
    # Create minimal schemas if import fails
    from pydantic import BaseModel
    class DesignRequest(BaseModel):
        problem_statement: str
        requirements: list = []
    class DesignResponse(BaseModel):
        design_id: str
        analysis: str
        suggestions: list = []
        components: list = []
    class FeedbackRequest(BaseModel):
        component_type: str
        component_details: dict = {}

try:
    from .agent import SystemDesignAgent
    agent = SystemDesignAgent()
except ImportError as e:
    logging.warning(f"Could not import SystemDesignAgent: {e}")
    agent = None

try:
    from .problem_service import ProblemService
    problem_service = ProblemService()
except ImportError as e:
    logging.warning(f"Could not import ProblemService: {e}")
    problem_service = None

try:
    from .llm_service import LLMService
    llm_service = LLMService()
except ImportError as e:
    logging.warning(f"Could not import LLMService: {e}")
    llm_service = None

try:
    from .solution_service import SolutionVerificationService
    solution_service = SolutionVerificationService()
except ImportError as e:
    logging.warning(f"Could not import SolutionVerificationService: {e}")
    solution_service = None

try:
    from .rag.ingest import rag_ingestor
    from .rag.query import rag_response_generator, rag_query_engine
    rag_available = True
except ImportError as e:
    logging.warning(f"Could not import RAG components: {e}")
    rag_available = False
    rag_ingestor = None
    rag_response_generator = None
    rag_query_engine = None

router = APIRouter()

# Pydantic models for request bodies
class QuestionRequest(BaseModel):
    question: str
    problem_context: str = None
    conversation_history: list = None

class SolutionRequest(BaseModel):
    architecture_components: list
    design_choices: list = []
    explanation: str = ""

@router.post("/design/submit", response_model=DesignResponse)
async def submit_design(request: DesignRequest):
    """Submit a system design problem and get initial analysis"""
    try:
        result = await agent.analyze_design(request.problem_statement, request.requirements)
        return DesignResponse(
            design_id=result["design_id"],
            analysis=result["analysis"],
            suggestions=result["suggestions"],
            components=result["components"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/design/{design_id}/stream")
async def stream_design_feedback(design_id: str):
    """Stream real-time feedback for a design"""
    
    async def generate_feedback():
        try:
            async for chunk in agent.stream_feedback(design_id):
                yield f"data: {json.dumps(chunk)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(
        generate_feedback(),
        media_type="text/plain",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )

@router.post("/design/{design_id}/feedback")
async def provide_feedback(design_id: str, feedback: FeedbackRequest):
    """Provide feedback on a specific design component"""
    try:
        result = await agent.evaluate_component(
            design_id, 
            feedback.component_type, 
            feedback.component_details
        )
        return {"feedback": result["feedback"], "score": result["score"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/problems")
async def list_problems():
    """Get list of available system design problems"""
    try:
        return {
            "problems": problem_service.get_all_problems(),
            "stats": problem_service.get_problem_stats()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/problems/generate")
async def generate_problem(difficulty: str = Query(..., description="Problem difficulty: 'beginner' or 'intermediate'")):
    """Generate a random problem by difficulty level"""
    try:
        problem = problem_service.get_problem_by_difficulty(difficulty)
        return problem
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/problems/{problem_id}")
async def get_problem(problem_id: str):
    """Get a specific problem by ID"""
    try:
        problem = problem_service.get_problem_by_id(problem_id)
        if not problem:
            raise HTTPException(status_code=404, detail=f"Problem with ID '{problem_id}' not found")
        return problem
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/problems/difficulty/{difficulty}")
async def get_problems_by_difficulty(difficulty: str):
    """Get all problems for a specific difficulty level"""
    try:
        problems = problem_service.get_problems_by_difficulty(difficulty)
        return {
            "difficulty": difficulty,
            "count": len(problems),
            "problems": problems
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# RAG and AI Assistant Endpoints

@router.post("/assistant/ask")
async def ask_assistant(request: QuestionRequest):
    """Ask the RAG-enhanced AI assistant a question"""
    if not rag_available or not rag_response_generator:
        raise HTTPException(status_code=503, detail="RAG system not available")
    
    try:
        response = rag_response_generator.answer_question(
            question=request.question,
            problem_context=request.problem_context,
            conversation_history=request.conversation_history
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/assistant/status")
async def get_assistant_status():
    """Get the status of the AI assistant and RAG system"""
    try:
        collection_stats = {}
        if rag_available and rag_ingestor:
            collection_stats = rag_ingestor.get_collection_stats()
        
        return {
            "llm_available": llm_service.is_available() if llm_service else False,
            "rag_available": rag_available and not collection_stats.get("error"),
            "collection_stats": collection_stats,
            "capabilities": {
                "question_answering": rag_available,
                "solution_evaluation": llm_service.is_available() if llm_service else False,
                "hint_generation": llm_service.is_available() if llm_service else False,
                "follow_up_questions": llm_service.is_available() if llm_service else False
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/assistant/topics/{topic}")
async def get_related_topics(topic: str, limit: int = Query(5, ge=1, le=20)):
    """Get related topics for a given system design topic"""
    try:
        related_topics = rag_response_generator.get_related_topics(topic, limit)
        return {
            "topic": topic,
            "related_topics": related_topics,
            "count": len(related_topics)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Solution verification with LLM enhancement
@router.post("/solutions/verify/{problem_id}")
async def verify_solution(problem_id: str, solution: SolutionRequest):
    """Verify a solution with LLM enhancement"""
    try:
        # Basic verification
        basic_verification = solution_service.verify_solution(
            problem_id, 
            solution.dict()
        )
        
        # LLM enhancement
        llm_enhancement = llm_service.enhance_solution_evaluation(
            problem_id, 
            solution.dict(), 
            basic_verification['overall_score']
        )
        
        # Follow-up questions
        follow_up_questions = llm_service.generate_follow_up_questions(
            problem_id, 
            solution.dict()
        )
        
        return {
            **basic_verification,
            "llm_enhancement": llm_enhancement,
            "follow_up_questions": follow_up_questions
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/problems/{problem_id}/hints")
async def get_problem_hints(problem_id: str):
    """Get AI-generated hints for a problem"""
    try:
        hints = llm_service.generate_dynamic_hints(problem_id)
        return {
            "problem_id": problem_id,
            "hints": hints,
            "count": len(hints)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# RAG Management Endpoints

@router.post("/rag/ingest")
async def ingest_documents(force_refresh: bool = Query(False)):
    """Ingest documents into the RAG system"""
    try:
        result = rag_ingestor.ingest_documents(force_refresh=force_refresh)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/rag/stats")
async def get_rag_stats():
    """Get RAG system statistics"""
    try:
        stats = rag_ingestor.get_collection_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/rag/reset")
async def reset_rag_collection():
    """Reset the RAG collection (admin endpoint)"""
    try:
        result = rag_ingestor.reset_collection()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/rag/search")
async def search_knowledge(query: str, top_k: int = Query(5, ge=1, le=20)):
    """Search the knowledge base directly"""
    try:
        results = rag_query_engine.search_similar_documents(query, top_k)
        
        return {
            "query": query,
            "results": [doc.to_dict() for doc in results],
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
