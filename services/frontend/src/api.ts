const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

// New interfaces matching your backend
export interface Problem {
  id: string;
  title: string;
  description: string;
  tags: string[];
  difficulty: string;
  expectations: string[];
}

export interface UserSolution {
  architecture_components: string[];
  design_choices: string[];
  explanation?: string;
}

export interface VerificationResult {
  problem_id: string;
  overall_score: number;
  max_score: number;
  component_analysis: {
    score: number;
    matched_components: string[];
    missing_components: string[];
    extra_components: string[];
  };
  design_choices_analysis: {
    score: number;
    addressed_expectations: string[];
    missing_expectations: string[];
  };
  recommendations: string[];
  llm_enhancement?: {
    llm_enhanced_score: number;
    llm_feedback: string;
    strengths: string[];
    improvements: string[];
    advanced_concepts: string[];
    industry_relevance: string;
  };
  follow_up_questions?: string[];
}

export interface AssistantRequest {
  question: string;
  context_problem_id?: string;
}

export interface AssistantResponse {
  question: string;
  answer: string;
  related_concepts: string[];
  confidence: string;
}

class APIClient {
  // Problem Management
  async getAllProblems(): Promise<{problems: Problem[], stats: any}> {
    const response = await fetch(`${API_BASE}/problems`);
    if (!response.ok) {
      throw new Error('Failed to fetch problems');
    }
    return response.json();
  }

  async generateRandomProblem(difficulty: 'beginner' | 'intermediate'): Promise<Problem> {
    const response = await fetch(`${API_BASE}/problems/generate?difficulty=${difficulty}`);
    if (!response.ok) {
      throw new Error('Failed to generate problem');
    }
    return response.json();
  }

  async getProblem(problemId: string): Promise<Problem> {
    const response = await fetch(`${API_BASE}/problems/${problemId}`);
    if (!response.ok) {
      throw new Error('Failed to fetch problem');
    }
    return response.json();
  }

  async getProblemsByDifficulty(difficulty: string): Promise<{difficulty: string, count: number, problems: Problem[]}> {
    const response = await fetch(`${API_BASE}/problems/difficulty/${difficulty}`);
    if (!response.ok) {
      throw new Error('Failed to fetch problems by difficulty');
    }
    return response.json();
  }

  // Solution Verification
  async verifySolution(problemId: string, userSolution: UserSolution): Promise<VerificationResult> {
    const response = await fetch(`${API_BASE}/solutions/verify/${problemId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userSolution),
    });
    
    if (!response.ok) {
      throw new Error('Failed to verify solution');
    }
    
    return response.json();
  }

  async getExpectedSolution(problemId: string) {
    const response = await fetch(`${API_BASE}/solutions/${problemId}`);
    if (!response.ok) {
      throw new Error('Failed to fetch expected solution');
    }
    return response.json();
  }

  async compareSolutions(problemId: string, userSolution: UserSolution) {
    const response = await fetch(`${API_BASE}/solutions/compare/${problemId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userSolution),
    });
    
    if (!response.ok) {
      throw new Error('Failed to compare solutions');
    }
    
    return response.json();
  }

  // LLM-Enhanced Features
  async getDynamicHints(problemId: string, progress?: any): Promise<{problem_id: string, hints: string[], total_hints: number}> {
    const url = new URL(`${API_BASE}/problems/${problemId}/hints`);
    if (progress) {
      url.searchParams.append('progress', JSON.stringify(progress));
    }
    
    const response = await fetch(url.toString());
    if (!response.ok) {
      throw new Error('Failed to get hints');
    }
    return response.json();
  }

  async askAssistant(request: AssistantRequest): Promise<AssistantResponse> {
    const response = await fetch(`${API_BASE}/assistant/ask`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });
    
    if (!response.ok) {
      throw new Error('Failed to ask assistant');
    }
    
    return response.json();
  }

  async getAssistantStatus(): Promise<{llm_available: boolean, openai_configured: boolean, features: any}> {
    const response = await fetch(`${API_BASE}/assistant/status`);
    if (!response.ok) {
      throw new Error('Failed to get assistant status');
    }
    return response.json();
  }

  // Legacy methods for compatibility (can be removed later)
  async getProblems() {
    const data = await this.getAllProblems();
    return data.problems;
  }
}

export const api = new APIClient();






