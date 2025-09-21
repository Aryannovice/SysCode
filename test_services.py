"""
Direct testing of our services without running the API server
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'api'))

from app.problem_service import ProblemService
from app.solution_service import SolutionVerificationService

def test_problem_service():
    """Test the ProblemService directly"""
    print("🧪 Testing ProblemService...")
    
    try:
        service = ProblemService()
        
        # Test getting all problems
        problems = service.get_all_problems()
        print(f"✅ Loaded {len(problems)} problems")
        
        # Test getting beginner problems
        beginner_problems = service.get_problems_by_difficulty("beginner")
        print(f"✅ Found {len(beginner_problems)} beginner problems")
        
        # Test random problem generation
        random_problem = service.get_problem_by_difficulty("beginner")
        print(f"✅ Random beginner problem: {random_problem['id']} - {random_problem['title']}")
        
        # Test getting specific problem
        specific_problem = service.get_problem_by_id(random_problem['id'])
        print(f"✅ Retrieved specific problem: {specific_problem['title']}")
        
        # Test stats
        stats = service.get_problem_stats()
        print(f"✅ Stats: {stats['total_problems']} total, {stats['difficulty_breakdown']}")
        
        return random_problem['id']
        
    except Exception as e:
        print(f"❌ ProblemService Error: {e}")
        return None

def test_solution_service(problem_id):
    """Test the SolutionVerificationService"""
    print(f"\n🧪 Testing SolutionVerificationService with problem: {problem_id}")
    
    try:
        service = SolutionVerificationService()
        
        # Test getting expected solution
        expected_solution = service.problem_service.get_solution_for_problem(problem_id)
        if expected_solution:
            print(f"✅ Found expected solution: {expected_solution['approach_name']}")
            print(f"   Components: {expected_solution.get('architecture_components', [])}")
        else:
            print(f"❌ No expected solution found for {problem_id}")
            return
        
        # Test solution verification with a sample solution
        user_solution = {
            "architecture_components": [
                "Load Balancer",
                "API Servers", 
                "Database"
            ],
            "design_choices": [
                "Use Redis for caching frequently accessed data",
                "Implement horizontal scaling with multiple servers",
                "Apply rate limiting to prevent abuse"
            ],
            "explanation": "This architecture focuses on scalability and performance."
        }
        
        verification_result = service.verify_solution(problem_id, user_solution)
        
        print(f"✅ Solution Verification Complete:")
        print(f"   Overall Score: {verification_result['overall_score']}/100")
        print(f"   Component Analysis Score: {verification_result['component_analysis']['score']}")
        print(f"   Design Choices Score: {verification_result['design_choices_analysis']['score']}")
        print(f"   Matched Components: {verification_result['component_analysis']['matched_components']}")
        print(f"   Missing Components: {verification_result['component_analysis']['missing_components']}")
        print(f"   Recommendations: {len(verification_result['recommendations'])} items")
        
        if verification_result['recommendations']:
            print(f"   First Recommendation: {verification_result['recommendations'][0]}")
        
    except Exception as e:
        print(f"❌ SolutionVerificationService Error: {e}")
        import traceback
        traceback.print_exc()

def test_file_loading():
    """Test if our JSON files can be loaded"""
    print("🧪 Testing JSON file loading...")
    
    import json
    from pathlib import Path
    
    try:
        # Test problems.json
        problems_path = Path("services/api/app/ProblemsandSolutions/problems.json")
        with open(problems_path, 'r', encoding='utf-8') as f:
            problems = json.load(f)
        print(f"✅ Loaded problems.json: {len(problems)} problems")
        
        # Test solutions.json  
        solutions_path = Path("services/api/app/ProblemsandSolutions/solutions.json")
        with open(solutions_path, 'r', encoding='utf-8') as f:
            solutions = json.load(f)
        print(f"✅ Loaded solutions.json: {len(solutions)} solutions")
        
        # Check if problem IDs match between files
        problem_ids = {p['id'] for p in problems}
        solution_ids = {s['problem_id'] for s in solutions}
        matching_ids = problem_ids.intersection(solution_ids)
        print(f"✅ Matching IDs: {len(matching_ids)} out of {len(problem_ids)} problems have solutions")
        
        return True
        
    except Exception as e:
        print(f"❌ File Loading Error: {e}")
        return False

def main():
    """Run all direct service tests"""
    print("🚀 Starting Direct Service Tests...\n")
    
    # Test file loading first
    if not test_file_loading():
        print("❌ Cannot load JSON files. Please check file paths.")
        return
    
    # Test problem service
    problem_id = test_problem_service()
    
    if problem_id:
        # Test solution service
        test_solution_service(problem_id)
    
    print("\n✅ All direct service tests completed!")

if __name__ == "__main__":
    main()
