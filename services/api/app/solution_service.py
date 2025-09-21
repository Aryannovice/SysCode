from typing import Dict, List, Optional, Tuple
from .problem_service import ProblemService

class SolutionVerificationService:
    def __init__(self):
        self.problem_service = ProblemService()
    
    def verify_solution(self, problem_id: str, user_solution: Dict) -> Dict:
        """
        Verify a user's solution against the expected solution
        
        Args:
            problem_id: The ID of the problem being solved
            user_solution: User's proposed solution structure
            
        Returns:
            Dict: Verification results with score and feedback
        """
        # Get the expected solution
        expected_solution = self.problem_service.get_solution_for_problem(problem_id)
        if not expected_solution:
            raise ValueError(f"No solution found for problem: {problem_id}")
        
        # Get the problem for context
        problem = self.problem_service.get_problem_by_id(problem_id)
        if not problem:
            raise ValueError(f"Problem not found: {problem_id}")
        
        verification_result = {
            "problem_id": problem_id,
            "overall_score": 0,
            "max_score": 100,
            "component_analysis": {},
            "design_choices_analysis": {},
            "missing_components": [],
            "extra_components": [],
            "recommendations": [],
            "strengths": [],
            "areas_for_improvement": []
        }
        
        # Verify architecture components
        component_score, component_analysis = self._verify_components(
            user_solution.get("architecture_components", []),
            expected_solution.get("architecture_components", [])
        )
        
        # Verify design choices
        design_score, design_analysis = self._verify_design_choices(
            user_solution.get("design_choices", []),
            expected_solution.get("design_choices", []),
            problem.get("expectations", [])
        )
        
        # Calculate overall score (weighted)
        component_weight = 0.4  # 40% for components
        design_weight = 0.6     # 60% for design choices
        
        overall_score = (component_score * component_weight) + (design_score * design_weight)
        
        verification_result.update({
            "overall_score": round(overall_score, 1),
            "component_analysis": component_analysis,
            "design_choices_analysis": design_analysis
        })
        
        # Generate recommendations
        verification_result["recommendations"] = self._generate_recommendations(
            verification_result, expected_solution, problem
        )
        
        return verification_result
    
    def _verify_components(self, user_components: List[str], expected_components: List[str]) -> Tuple[float, Dict]:
        """
        Verify architecture components against expected solution
        
        Returns:
            Tuple[float, Dict]: Score (0-100) and detailed analysis
        """
        analysis = {
            "score": 0,
            "total_expected": len(expected_components),
            "total_provided": len(user_components),
            "matched_components": [],
            "missing_components": [],
            "extra_components": [],
            "partial_matches": []
        }
        
        if not expected_components:
            return 100.0, analysis
        
        # Normalize component names for comparison
        expected_normalized = [self._normalize_component_name(comp) for comp in expected_components]
        user_normalized = [self._normalize_component_name(comp) for comp in user_components]
        
        # Find exact matches
        matched = []
        for i, expected_comp in enumerate(expected_normalized):
            for j, user_comp in enumerate(user_normalized):
                if expected_comp == user_comp:
                    matched.append((expected_components[i], user_components[j]))
                    break
        
        # Find partial matches (for more flexible matching)
        partial_matches = []
        unmatched_expected = [comp for comp in expected_components if comp not in [m[0] for m in matched]]
        unmatched_user = [comp for comp in user_components if comp not in [m[1] for m in matched]]
        
        for expected_comp in unmatched_expected:
            for user_comp in unmatched_user:
                similarity = self._calculate_component_similarity(expected_comp, user_comp)
                if similarity > 0.6:  # 60% similarity threshold
                    partial_matches.append((expected_comp, user_comp, similarity))
        
        # Calculate score
        exact_match_score = (len(matched) / len(expected_components)) * 80  # Max 80 for exact matches
        partial_match_score = sum(match[2] for match in partial_matches) / len(expected_components) * 20  # Max 20 for partial
        
        score = min(100, exact_match_score + partial_match_score)
        
        analysis.update({
            "score": round(score, 1),
            "matched_components": [match[0] for match in matched],
            "missing_components": [comp for comp in expected_components if comp not in [m[0] for m in matched]],
            "extra_components": [comp for comp in user_components if comp not in [m[1] for m in matched]],
            "partial_matches": [(match[0], match[1]) for match in partial_matches]
        })
        
        return score, analysis
    
    def _verify_design_choices(self, user_choices: List[str], expected_choices: List[str], problem_expectations: List[str]) -> Tuple[float, Dict]:
        """
        Verify design choices against expected solution and problem expectations
        
        Returns:
            Tuple[float, Dict]: Score (0-100) and detailed analysis
        """
        analysis = {
            "score": 0,
            "addressed_expectations": [],
            "missing_expectations": [],
            "design_rationale_score": 0,
            "scalability_considerations": [],
            "trade_offs_identified": []
        }
        
        if not expected_choices and not problem_expectations:
            return 100.0, analysis
        
        # Check how many problem expectations are addressed
        expectations_score = 0
        addressed_expectations = []
        
        for expectation in problem_expectations:
            expectation_addressed = False
            for choice in user_choices:
                if self._choice_addresses_expectation(choice, expectation):
                    addressed_expectations.append(expectation)
                    expectation_addressed = True
                    break
            
            if expectation_addressed:
                expectations_score += 1
        
        if problem_expectations:
            expectations_percentage = (expectations_score / len(problem_expectations)) * 100
        else:
            expectations_percentage = 100
        
        # Evaluate design rationale quality
        rationale_score = self._evaluate_design_rationale(user_choices, expected_choices)
        
        # Final score (weighted combination)
        final_score = (expectations_percentage * 0.7) + (rationale_score * 0.3)
        
        analysis.update({
            "score": round(final_score, 1),
            "addressed_expectations": addressed_expectations,
            "missing_expectations": [exp for exp in problem_expectations if exp not in addressed_expectations],
            "design_rationale_score": round(rationale_score, 1)
        })
        
        return final_score, analysis
    
    def _normalize_component_name(self, component: str) -> str:
        """Normalize component names for comparison"""
        return component.lower().replace(" ", "").replace("-", "").replace("_", "")
    
    def _calculate_component_similarity(self, comp1: str, comp2: str) -> float:
        """Calculate similarity between two component names"""
        # Simple similarity based on common words
        words1 = set(comp1.lower().split())
        words2 = set(comp2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _choice_addresses_expectation(self, choice: str, expectation: str) -> bool:
        """Check if a design choice addresses a problem expectation"""
        # Simple keyword-based matching (can be enhanced with NLP)
        choice_words = set(choice.lower().split())
        expectation_words = set(expectation.lower().split())
        
        # Remove common words
        common_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        choice_words = choice_words - common_words
        expectation_words = expectation_words - common_words
        
        # Check for overlap
        overlap = choice_words.intersection(expectation_words)
        return len(overlap) >= 2  # At least 2 meaningful words overlap
    
    def _evaluate_design_rationale(self, user_choices: List[str], expected_choices: List[str]) -> float:
        """Evaluate the quality of design rationale"""
        if not user_choices:
            return 0.0
        
        # Check for presence of key design concepts
        design_concepts = [
            "scalability", "availability", "consistency", "partition", "cache", 
            "database", "load", "performance", "fault", "redundancy", "replication"
        ]
        
        concept_mentions = 0
        total_concepts = len(design_concepts)
        
        user_text = " ".join(user_choices).lower()
        
        for concept in design_concepts:
            if concept in user_text:
                concept_mentions += 1
        
        # Score based on concept coverage and depth
        coverage_score = (concept_mentions / total_concepts) * 100
        
        # Bonus for detailed explanations (longer descriptions generally indicate more thought)
        avg_choice_length = sum(len(choice.split()) for choice in user_choices) / len(user_choices)
        detail_bonus = min(20, avg_choice_length * 2)  # Max 20 bonus points
        
        return min(100, coverage_score + detail_bonus)
    
    def _generate_recommendations(self, verification_result: Dict, expected_solution: Dict, problem: Dict) -> List[str]:
        """Generate recommendations based on verification results"""
        recommendations = []
        
        # Component recommendations
        if verification_result["component_analysis"]["missing_components"]:
            missing = verification_result["component_analysis"]["missing_components"]
            recommendations.append(f"Consider adding these missing components: {', '.join(missing[:3])}")
        
        # Design choice recommendations
        if verification_result["design_choices_analysis"]["missing_expectations"]:
            missing_exp = verification_result["design_choices_analysis"]["missing_expectations"]
            recommendations.append(f"Address these requirements: {missing_exp[0]}" if missing_exp else "")
        
        # Score-based recommendations
        overall_score = verification_result["overall_score"]
        if overall_score < 60:
            recommendations.append("Focus on covering the core system requirements first")
        elif overall_score < 80:
            recommendations.append("Good foundation! Consider adding more scalability and fault tolerance details")
        else:
            recommendations.append("Excellent design! Consider edge cases and performance optimizations")
        
        # Add specific recommendations from expected solution
        if expected_solution.get("extensions"):
            recommendations.append(f"Extension ideas: {expected_solution['extensions'][:100]}...")
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    def compare_solutions(self, problem_id: str, user_solution: Dict, alternative_approach: str = None) -> Dict:
        """
        Compare user solution with expected solution and optionally an alternative approach
        
        Args:
            problem_id: Problem identifier
            user_solution: User's solution
            alternative_approach: Optional alternative approach name
            
        Returns:
            Dict: Comparison results
        """
        expected_solution = self.problem_service.get_solution_for_problem(problem_id)
        if not expected_solution:
            raise ValueError(f"No solution found for problem: {problem_id}")
        
        comparison = {
            "user_vs_expected": self.verify_solution(problem_id, user_solution),
            "expected_approach": {
                "name": expected_solution.get("approach_name", "Standard Approach"),
                "components": expected_solution.get("architecture_components", []),
                "scalability": expected_solution.get("scalability", ""),
                "trade_offs": expected_solution.get("design_choices", [])
            }
        }
        
        return comparison

