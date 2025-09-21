import json
import random
from pathlib import Path
from typing import Dict, List, Optional

class ProblemService:
    def __init__(self):
        self.problems_path = Path(__file__).parent / "ProblemsandSolutions" / "problems.json"
        self.solutions_path = Path(__file__).parent / "ProblemsandSolutions" / "solutions.json"
        self._problems = None
        self._solutions = None
    
    def _load_problems(self) -> List[Dict]:
        """Load problems from JSON file"""
        if self._problems is None:
            try:
                with open(self.problems_path, 'r', encoding='utf-8') as f:
                    self._problems = json.load(f)
            except FileNotFoundError:
                raise FileNotFoundError(f"Problems file not found at {self.problems_path}")
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in problems file: {e}")
        return self._problems
    
    def _load_solutions(self) -> List[Dict]:
        """Load solutions from JSON file"""
        if self._solutions is None:
            try:
                with open(self.solutions_path, 'r', encoding='utf-8') as f:
                    self._solutions = json.load(f)
            except FileNotFoundError:
                raise FileNotFoundError(f"Solutions file not found at {self.solutions_path}")
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in solutions file: {e}")
        return self._solutions
    
    def get_problem_by_difficulty(self, difficulty: str) -> Dict:
        """
        Select a random problem by difficulty level
        
        Args:
            difficulty: "beginner" or "intermediate"
            
        Returns:
            Dict: Problem object from problems.json
            
        Raises:
            ValueError: If difficulty is invalid or no problems found
        """
        if difficulty not in ["beginner", "intermediate"]:
            raise ValueError("Difficulty must be 'beginner' or 'intermediate'")
        
        problems = self._load_problems()
        
        # Filter problems by difficulty
        filtered_problems = [p for p in problems if p.get("difficulty") == difficulty]
        
        if not filtered_problems:
            raise ValueError(f"No problems found for difficulty: {difficulty}")
        
        # Return random problem
        return random.choice(filtered_problems)
    
    def get_problem_by_id(self, problem_id: str) -> Optional[Dict]:
        """
        Get a specific problem by ID
        
        Args:
            problem_id: Problem identifier
            
        Returns:
            Dict: Problem object or None if not found
        """
        problems = self._load_problems()
        
        for problem in problems:
            if problem.get("id") == problem_id:
                return problem
        
        return None
    
    def get_all_problems(self) -> List[Dict]:
        """Get all available problems"""
        return self._load_problems()
    
    def get_problems_by_difficulty(self, difficulty: str) -> List[Dict]:
        """
        Get all problems for a specific difficulty
        
        Args:
            difficulty: "beginner" or "intermediate"
            
        Returns:
            List[Dict]: List of problems
        """
        if difficulty not in ["beginner", "intermediate"]:
            raise ValueError("Difficulty must be 'beginner' or 'intermediate'")
        
        problems = self._load_problems()
        return [p for p in problems if p.get("difficulty") == difficulty]
    
    def get_solution_for_problem(self, problem_id: str) -> Optional[Dict]:
        """
        Get the solution for a specific problem
        
        Args:
            problem_id: Problem identifier
            
        Returns:
            Dict: Solution object or None if not found
        """
        solutions = self._load_solutions()
        
        for solution in solutions:
            if solution.get("problem_id") == problem_id:
                return solution
        
        return None
    
    def get_problem_stats(self) -> Dict:
        """Get statistics about available problems"""
        problems = self._load_problems()
        
        stats = {
            "total_problems": len(problems),
            "difficulty_breakdown": {},
            "tag_breakdown": {}
        }
        
        # Count by difficulty
        for problem in problems:
            difficulty = problem.get("difficulty", "unknown")
            stats["difficulty_breakdown"][difficulty] = stats["difficulty_breakdown"].get(difficulty, 0) + 1
        
        # Count by tags
        for problem in problems:
            tags = problem.get("tags", [])
            for tag in tags:
                stats["tag_breakdown"][tag] = stats["tag_breakdown"].get(tag, 0) + 1
        
        return stats
