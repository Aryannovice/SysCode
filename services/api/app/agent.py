import asyncio
import uuid
import json
from typing import Dict, List, AsyncGenerator
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class SystemDesignProblem:
    id: str
    title: str
    description: str
    requirements: List[str]
    scale: str
    difficulty: str

class SystemDesignAgent:
    def __init__(self):
        self.active_designs = {}
        self.problems_db = self._load_problems()
    
    def _load_problems(self) -> List[SystemDesignProblem]:
        """Load sample system design problems"""
        return [
            SystemDesignProblem(
                id="chat-app",
                title="Design a Chat Application like WhatsApp",
                description="Design a real-time messaging system that supports 1-on-1 and group chats",
                requirements=[
                    "Real-time messaging",
                    "Message history",
                    "User presence status",
                    "File sharing",
                    "Push notifications"
                ],
                scale="100M users",
                difficulty="Medium"
            ),
            SystemDesignProblem(
                id="url-shortener",
                title="Design a URL Shortener like bit.ly",
                description="Design a service that shortens long URLs and provides analytics",
                requirements=[
                    "URL shortening",
                    "Custom aliases",
                    "Analytics tracking",
                    "Rate limiting",
                    "High availability"
                ],
                scale="100M URLs/day",
                difficulty="Easy"
            ),
            SystemDesignProblem(
                id="social-media",
                title="Design a Social Media Feed",
                description="Design a timeline/newsfeed system like Facebook or Twitter",
                requirements=[
                    "User posts and interactions",
                    "Personalized timeline",
                    "Real-time updates",
                    "Media uploads",
                    "Content ranking"
                ],
                scale="1B users",
                difficulty="Hard"
            )
        ]
    
    async def analyze_design(self, problem_statement: str, requirements: List[str]) -> Dict:
        """Analyze a system design problem and provide initial guidance"""
        design_id = str(uuid.uuid4())
        
        # Simulate AI analysis (replace with actual LLM integration)
        analysis = self._generate_analysis(problem_statement, requirements)
        components = self._suggest_components(problem_statement, requirements)
        suggestions = self._generate_suggestions(problem_statement, requirements)
        
        # Store design session
        self.active_designs[design_id] = {
            "problem": problem_statement,
            "requirements": requirements,
            "components": components,
            "created_at": asyncio.get_event_loop().time()
        }
        
        return {
            "design_id": design_id,
            "analysis": analysis,
            "suggestions": suggestions,
            "components": components
        }
    
    def _generate_analysis(self, problem: str, requirements: List[str]) -> str:
        """Generate initial analysis of the problem"""
        return f"""
        Based on your problem statement "{problem}", I can see this requires:
        
        1. **Scale Considerations**: We need to think about read/write patterns and data consistency
        2. **Key Components**: This system will likely need databases, caching, and API services
        3. **Critical Paths**: Identify the most performance-sensitive operations
        4. **Trade-offs**: Consider CAP theorem implications and consistency vs availability
        
        Let's start by breaking down your requirements: {', '.join(requirements)}
        """
    
    def _suggest_components(self, problem: str, requirements: List[str]) -> List[Dict]:
        """Suggest initial system components"""
        components = []
        
        # Basic components every system needs
        components.append({
            "type": "load_balancer",
            "name": "Load Balancer",
            "description": "Distributes incoming requests across multiple servers",
            "rationale": "Ensures high availability and handles traffic spikes",
            "alternatives": ["NGINX", "AWS ALB", "HAProxy"]
        })
        
        components.append({
            "type": "api_gateway",
            "name": "API Gateway",
            "description": "Single entry point for all client requests",
            "rationale": "Handles authentication, rate limiting, and request routing",
            "alternatives": ["AWS API Gateway", "Kong", "Zuul"]
        })
        
        # Database selection based on requirements
        if any("real-time" in req.lower() for req in requirements):
            components.append({
                "type": "database",
                "name": "Primary Database",
                "description": "Main data store optimized for OLTP operations",
                "rationale": "Handles transactional data with ACID properties",
                "alternatives": ["PostgreSQL", "MySQL", "MongoDB"]
            })
            
            components.append({
                "type": "cache",
                "name": "Redis Cache",
                "description": "In-memory data store for fast access",
                "rationale": "Reduces database load and improves response times",
                "alternatives": ["Redis", "Memcached", "Hazelcast"]
            })
        
        return components
    
    def _generate_suggestions(self, problem: str, requirements: List[str]) -> List[str]:
        """Generate suggestions for improvement"""
        return [
            "Consider data partitioning strategies for scale",
            "Implement proper monitoring and alerting",
            "Plan for disaster recovery and backups",
            "Think about security at every layer",
            "Design for horizontal scaling from the start"
        ]
    
    async def stream_feedback(self, design_id: str) -> AsyncGenerator[Dict, None]:
        """Stream real-time feedback for a design"""
        if design_id not in self.active_designs:
            yield {"error": "Design not found"}
            return
        
        feedback_items = [
            {"type": "tip", "message": "Consider implementing database sharding for better performance"},
            {"type": "warning", "message": "Don't forget to plan for data backup and recovery"},
            {"type": "suggestion", "message": "Add monitoring for all critical components"},
            {"type": "question", "message": "How will you handle data consistency across services?"},
            {"type": "best_practice", "message": "Implement circuit breakers for external service calls"}
        ]
        
        for item in feedback_items:
            await asyncio.sleep(2)  # Simulate processing time
            yield item
    
    async def evaluate_component(self, design_id: str, component_type: str, component_details: Dict) -> Dict:
        """Evaluate a specific component choice"""
        if design_id not in self.active_designs:
            raise ValueError("Design not found")
        
        # Simulate component evaluation
        score = 85  # Mock score
        feedback = f"Good choice for {component_type}. Consider these optimizations: caching strategy, connection pooling, and monitoring setup."
        
        return {
            "feedback": feedback,
            "score": score,
            "recommendations": [
                "Add health checks",
                "Implement proper logging",
                "Configure auto-scaling"
            ]
        }
    
    def get_available_problems(self) -> List[Dict]:
        """Return list of available problems"""
        return [
            {
                "id": p.id,
                "title": p.title,
                "description": p.description,
                "requirements": p.requirements,
                "scale": p.scale,
                "difficulty": p.difficulty
            }
            for p in self.problems_db
        ]