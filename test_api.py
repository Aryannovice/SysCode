import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000/api/v1"

def test_health_check():
    """Test if the API is running"""
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"✅ Health Check: {response.status_code} - {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health Check Failed: {e}")
        return False

def test_problem_generation():
    """Test problem generation endpoints"""
    print("\n🧪 Testing Problem Generation...")
    
    try:
        # Test beginner problem generation
        response = requests.get(f"{BASE_URL}/problems/generate?difficulty=beginner")
        if response.status_code == 200:
            problem = response.json()
            print(f"✅ Beginner Problem Generated:")
            print(f"   ID: {problem.get('id')}")
            print(f"   Title: {problem.get('title')}")
            print(f"   Difficulty: {problem.get('difficulty')}")
            return problem.get('id')  # Return problem ID for solution testing
        else:
            print(f"❌ Beginner Problem Generation Failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Problem Generation Error: {e}")
        return None

def test_problem_by_id(problem_id):
    """Test getting specific problem by ID"""
    print(f"\n🧪 Testing Get Problem by ID: {problem_id}")
    
    try:
        response = requests.get(f"{BASE_URL}/problems/{problem_id}")
        if response.status_code == 200:
            problem = response.json()
            print(f"✅ Problem Retrieved:")
            print(f"   Title: {problem.get('title')}")
            print(f"   Expectations: {len(problem.get('expectations', []))} items")
        else:
            print(f"❌ Get Problem Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get Problem Error: {e}")

def test_solution_verification(problem_id):
    """Test solution verification"""
    print(f"\n🧪 Testing Solution Verification for: {problem_id}")
    
    # Sample user solution
    user_solution = {
        "architecture_components": [
            "Load Balancer",
            "API Servers", 
            "Database",
            "Cache"
        ],
        "design_choices": [
            "Use Redis for caching frequently accessed URLs",
            "Implement database sharding for scalability",
            "Use consistent hashing for load distribution",
            "Apply rate limiting to prevent abuse"
        ],
        "explanation": "My approach focuses on scalability and performance by using caching and load balancing."
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/solutions/verify/{problem_id}",
            json=user_solution
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Solution Verification Success:")
            print(f"   Overall Score: {result.get('overall_score')}/100")
            print(f"   Component Score: {result.get('component_analysis', {}).get('score')}")
            print(f"   Design Score: {result.get('design_choices_analysis', {}).get('score')}")
            print(f"   Matched Components: {result.get('component_analysis', {}).get('matched_components')}")
            print(f"   Missing Components: {result.get('component_analysis', {}).get('missing_components')}")
            print(f"   Recommendations: {len(result.get('recommendations', []))} items")
        else:
            print(f"❌ Solution Verification Failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Solution Verification Error: {e}")

def test_get_expected_solution(problem_id):
    """Test getting expected solution"""
    print(f"\n🧪 Testing Get Expected Solution for: {problem_id}")
    
    try:
        response = requests.get(f"{BASE_URL}/solutions/{problem_id}")
        if response.status_code == 200:
            solution = response.json()
            print(f"✅ Expected Solution Retrieved:")
            print(f"   Approach: {solution.get('approach_name')}")
            print(f"   Components: {len(solution.get('architecture_components', []))} items")
            print(f"   Has Explanation: {'explanation' in solution}")
        else:
            print(f"❌ Get Expected Solution Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get Expected Solution Error: {e}")

def test_all_problems_stats():
    """Test getting all problems with stats"""
    print("\n🧪 Testing All Problems Stats...")
    
    try:
        response = requests.get(f"{BASE_URL}/problems")
        if response.status_code == 200:
            data = response.json()
            stats = data.get('stats', {})
            print(f"✅ Problems Stats Retrieved:")
            print(f"   Total Problems: {stats.get('total_problems')}")
            print(f"   Difficulty Breakdown: {stats.get('difficulty_breakdown')}")
            print(f"   Popular Tags: {list(stats.get('tag_breakdown', {}).keys())[:5]}")
        else:
            print(f"❌ Get Problems Stats Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get Problems Stats Error: {e}")

def main():
    """Run all tests"""
    print("🚀 Starting API Tests...")
    
    # Wait a moment for server to start
    time.sleep(2)
    
    # Test health check first
    if not test_health_check():
        print("❌ Server not running. Please start the API server first.")
        return
    
    # Test problem generation
    problem_id = test_problem_generation()
    
    if problem_id:
        # Test other endpoints with the generated problem
        test_problem_by_id(problem_id)
        test_solution_verification(problem_id)
        test_get_expected_solution(problem_id)
    
    # Test stats
    test_all_problems_stats()
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    main()

