"""
LLM Integration Service for enhanced problem evaluation and assistance
"""
import openai
import os
from typing import Dict, List, Optional
import json
import logging
from .problem_service import ProblemService
from .solution_service import SolutionVerificationService
from .rag.query import rag_response_generator

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self, api_key: str = None):
        """
        Initialize LLM service with OpenAI integration
        
        Args:
            api_key: OpenAI API key (if not provided, will try from environment)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = None
        
        if self.api_key:
            try:
                self.client = openai.OpenAI(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client: {e}")
                self.client = None
        
        self.problem_service = ProblemService()
        self.solution_service = SolutionVerificationService()
    
    def is_available(self) -> bool:
        """Check if LLM service is available"""
        return self.client is not None
    
    def enhance_solution_evaluation(self, problem_id: str, user_solution: Dict, basic_score: float) -> Dict:
        """
        Use LLM to provide enhanced evaluation of user solutions
        
        Args:
            problem_id: Problem identifier
            user_solution: User's solution
            basic_score: Score from rule-based verification
            
        Returns:
            Dict: Enhanced evaluation with LLM insights
        """
        if not self.is_available():
            return {
                "basic_score": basic_score,
                "llm_enhanced_score": basic_score,
                "llm_feedback": "LLM service not available - API key required",
                "error": "OpenAI API key not configured"
            }
        
        try:
            problem = self.problem_service.get_problem_by_id(problem_id)
            expected_solution = self.problem_service.get_solution_for_problem(problem_id)
            
            if not problem or not expected_solution:
                raise ValueError(f"Problem or solution not found: {problem_id}")
            
            # Create prompt for LLM evaluation
            prompt = self._create_evaluation_prompt(problem, expected_solution, user_solution, basic_score)
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert system design interviewer. Provide detailed, constructive feedback on system design solutions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            llm_evaluation = self._parse_llm_evaluation(response.choices[0].message.content)
            
            return {
                "basic_score": basic_score,
                "llm_enhanced_score": llm_evaluation.get("adjusted_score", basic_score),
                "llm_feedback": llm_evaluation.get("feedback", ""),
                "strengths": llm_evaluation.get("strengths", []),
                "improvements": llm_evaluation.get("improvements", []),
                "advanced_concepts": llm_evaluation.get("advanced_concepts", []),
                "industry_relevance": llm_evaluation.get("industry_relevance", "")
            }
            
        except Exception as e:
            logger.error(f"LLM evaluation failed: {e}")
            return {
                "basic_score": basic_score,
                "llm_enhanced_score": basic_score,
                "llm_feedback": "LLM evaluation unavailable",
                "error": str(e)
            }
    
    def generate_dynamic_hints(self, problem_id: str, user_progress: Dict = None) -> List[str]:
        """
        Generate contextual hints based on problem and user progress
        
        Args:
            problem_id: Problem identifier
            user_progress: Optional user progress information
            
        Returns:
            List[str]: Contextual hints
        """
        if not self.is_available():
            return [
                "Consider the core components needed for this system",
                "Think about scalability and performance requirements", 
                "Don't forget about data storage and retrieval patterns"
            ]
        
        try:
            problem = self.problem_service.get_problem_by_id(problem_id)
            if not problem:
                raise ValueError(f"Problem not found: {problem_id}")
            
            prompt = self._create_hints_prompt(problem, user_progress)
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful system design mentor. Provide gentle hints that guide learning without giving away the solution."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            hints_text = response.choices[0].message.content
            hints = self._parse_hints(hints_text)
            
            return hints[:5]  # Limit to 5 hints
            
        except Exception as e:
            logger.error(f"Hint generation failed: {e}")
            return [
                "Consider the core components needed for this system",
                "Think about scalability and performance requirements",
                "Don't forget about data storage and retrieval patterns"
            ]
    
    def answer_educational_question(self, question: str, context_problem_id: str = None) -> Dict:
        """
        Answer system design educational questions using RAG approach
        
        Args:
            question: User's question
            context_problem_id: Optional problem context
            
        Returns:
            Dict: Answer with explanation and relevant concepts
        """
        try:
            # Get problem context if provided
            problem_context = None
            if context_problem_id:
                problem = self.problem_service.get_problem_by_id(context_problem_id)
                if problem:
                    problem_context = f"{problem['title']}: {problem['description'][:200]}..."
            
            # Use RAG system for enhanced responses
            rag_response = rag_response_generator.answer_question(
                question=question,
                problem_context=problem_context
            )
            
            if rag_response.get("error"):
                # Fallback to basic LLM if RAG fails
                return self._fallback_educational_answer(question, problem_context)
            
            # Extract related concepts from sources
            related_concepts = []
            for source in rag_response.get("sources", []):
                title = source.get("title", "")
                if title and title not in related_concepts:
                    related_concepts.append(title)
            
            return {
                "answer": rag_response["answer"],
                "related_concepts": related_concepts[:5],  # Limit to 5
                "sources": rag_response.get("sources", []),
                "retrieved_count": rag_response.get("retrieved_count", 0),
                "confidence": "high" if rag_response.get("retrieved_count", 0) > 0 else "medium",
                "rag_enhanced": True
            }
            
        except Exception as e:
            logger.error(f"RAG educational question answering failed: {e}")
            # Fallback to basic LLM
            return self._fallback_educational_answer(question, context_problem_id)
    
    def _fallback_educational_answer(self, question: str, context_problem_id: str = None) -> Dict:
        """Fallback method for educational questions when RAG is unavailable"""
        if not self.is_available():
            return {
                "answer": "I'm sorry, the AI assistant is not available right now. Please check that the OpenAI API key is configured.",
                "related_concepts": [],
                "confidence": "low",
                "error": "LLM service unavailable"
            }
        
        try:
            # Get relevant context if problem ID provided
            context = ""
            if context_problem_id:
                problem = self.problem_service.get_problem_by_id(context_problem_id)
                if problem:
                    context = f"Context: The user is working on '{problem['title']}' - {problem['description'][:200]}..."
            
            prompt = self._create_educational_prompt(question, context)
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert system design educator. Provide clear, practical explanations with real-world examples. Focus on helping users understand concepts deeply."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=1200
            )
            
            answer_content = response.choices[0].message.content
            
            return {
                "answer": answer_content,
                "related_concepts": self._extract_related_concepts(answer_content),
                "confidence": "medium",
                "rag_enhanced": False
            }
            
        except Exception as e:
            logger.error(f"Educational question answering failed: {e}")
            return {
                "answer": "I'm sorry, I couldn't process your question right now. Please try again later.",
                "error": str(e)
            }
    
    def generate_follow_up_questions(self, problem_id: str, user_solution: Dict) -> List[str]:
        """
        Generate follow-up questions to deepen understanding
        
        Args:
            problem_id: Problem identifier
            user_solution: User's solution
            
        Returns:
            List[str]: Follow-up questions
        """
        if not self.is_available():
            return [
                "How would you handle this system at 10x scale?",
                "What happens if one of your components fails?",
                "How would you monitor this system in production?"
            ]
        
        try:
            problem = self.problem_service.get_problem_by_id(problem_id)
            if not problem:
                return []
            
            prompt = f"""
            Based on this system design problem and user solution, generate 3-5 thoughtful follow-up questions 
            that would help the user think deeper about their design:
            
            Problem: {problem['title']}
            User's Components: {user_solution.get('architecture_components', [])}
            User's Choices: {user_solution.get('design_choices', [])}
            
            Generate questions about:
            - Edge cases and failure scenarios
            - Scalability and performance considerations  
            - Alternative approaches and trade-offs
            - Real-world implementation challenges
            
            Format as a numbered list.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Generate insightful follow-up questions for system design learning."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=600
            )
            
            questions_text = response.choices[0].message.content
            questions = self._parse_questions(questions_text)
            
            return questions
            
        except Exception as e:
            logger.error(f"Follow-up question generation failed: {e}")
            return []
    
    def _create_evaluation_prompt(self, problem: Dict, expected_solution: Dict, user_solution: Dict, basic_score: float) -> str:
        """Create prompt for LLM solution evaluation"""
        return f"""
        Evaluate this system design solution as an expert interviewer:
        
        PROBLEM: {problem['title']}
        Description: {problem['description']}
        Requirements: {problem['expectations']}
        
        USER'S SOLUTION:
        Components: {user_solution.get('architecture_components', [])}
        Design Choices: {user_solution.get('design_choices', [])}
        Explanation: {user_solution.get('explanation', 'No explanation provided')}
        
        EXPECTED SOLUTION (for reference):
        Approach: {expected_solution['approach_name']}
        Components: {expected_solution['architecture_components']}
        
        Current basic score: {basic_score}/100
        
        Please provide:
        1. Adjusted score (0-100) considering nuance and understanding
        2. Specific strengths in the solution
        3. Key areas for improvement
        4. Advanced concepts they could consider
        5. How this applies to real-world systems
        
        Format as JSON:
        {{
            "adjusted_score": 85,
            "feedback": "Overall assessment...",
            "strengths": ["Good use of...", "Proper consideration of..."],
            "improvements": ["Consider adding...", "Think about..."],
            "advanced_concepts": ["Could explore...", "For scale, consider..."],
            "industry_relevance": "This design is similar to..."
        }}
        """
    
    def _create_hints_prompt(self, problem: Dict, user_progress: Dict = None) -> str:
        """Create prompt for generating hints"""
        progress_info = ""
        if user_progress:
            progress_info = f"User has attempted: {user_progress.get('attempted_components', [])}"
        
        return f"""
        Generate helpful hints for this system design problem:
        
        Problem: {problem['title']}
        Description: {problem['description']}
        Difficulty: {problem['difficulty']}
        {progress_info}
        
        Provide 3-5 progressive hints that:
        - Start with high-level architectural thinking
        - Guide toward key components without revealing exact solutions
        - Help think about scalability and trade-offs
        - Are appropriate for {problem['difficulty']} level
        
        Format as numbered list.
        """
    
    def _create_educational_prompt(self, question: str, context: str = "") -> str:
        """Create prompt for educational questions"""
        return f"""
        {context}
        
        Question: {question}
        
        Please provide a clear, educational answer that:
        - Explains concepts with real-world examples
        - Mentions relevant trade-offs
        - Suggests when to use different approaches
        - Includes practical implementation considerations
        
        Keep the explanation accessible but technically accurate.
        """
    
    def _parse_llm_evaluation(self, content: str) -> Dict:
        """Parse LLM evaluation response"""
        try:
            # Try to extract JSON from the response
            start = content.find('{')
            end = content.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = content[start:end]
                return json.loads(json_str)
        except:
            pass
        
        # Fallback: simple parsing
        return {
            "adjusted_score": 0,
            "feedback": content,
            "strengths": [],
            "improvements": [],
            "advanced_concepts": [],
            "industry_relevance": ""
        }
    
    def _parse_hints(self, content: str) -> List[str]:
        """Parse hints from LLM response"""
        lines = content.strip().split('\n')
        hints = []
        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                # Remove numbering and clean up
                clean_hint = line.split('.', 1)[-1].strip() if '.' in line else line
                clean_hint = clean_hint.lstrip('- •').strip()
                if clean_hint:
                    hints.append(clean_hint)
        return hints
    
    def _parse_questions(self, content: str) -> List[str]:
        """Parse questions from LLM response"""
        lines = content.strip().split('\n')
        questions = []
        for line in lines:
            line = line.strip()
            if line and ('?' in line):
                # Clean up numbering
                clean_question = line.split('.', 1)[-1].strip() if '.' in line else line
                clean_question = clean_question.lstrip('- •').strip()
                if clean_question:
                    questions.append(clean_question)
        return questions
    
    def _extract_related_concepts(self, content: str) -> List[str]:
        """Extract related system design concepts mentioned in content"""
        concepts = [
            "load balancing", "caching", "database sharding", "microservices",
            "cdn", "api gateway", "message queues", "pub/sub", "eventual consistency",
            "cap theorem", "horizontal scaling", "vertical scaling", "rate limiting"
        ]
        
        content_lower = content.lower()
        found_concepts = []
        for concept in concepts:
            if concept in content_lower:
                found_concepts.append(concept.title())
        
        return found_concepts[:5]  # Limit to 5 concepts
