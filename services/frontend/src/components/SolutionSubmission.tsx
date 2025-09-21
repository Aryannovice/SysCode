import React, { useState } from 'react';
import { api, UserSolution, VerificationResult } from '../api';

interface SolutionSubmissionProps {
  problemId: string;
  onSubmissionComplete?: (result: VerificationResult) => void;
}

const SolutionSubmission: React.FC<SolutionSubmissionProps> = ({
  problemId,
  onSubmissionComplete
}) => {
  const [solution, setSolution] = useState<UserSolution>({
    architecture_components: [],
    design_choices: [],
    explanation: ''
  });
  
  const [componentInput, setComponentInput] = useState('');
  const [choiceInput, setChoiceInput] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<VerificationResult | null>(null);

  const addComponent = () => {
    if (componentInput.trim()) {
      setSolution(prev => ({
        ...prev,
        architecture_components: [...prev.architecture_components, componentInput.trim()]
      }));
      setComponentInput('');
    }
  };

  const removeComponent = (index: number) => {
    setSolution(prev => ({
      ...prev,
      architecture_components: prev.architecture_components.filter((_, i) => i !== index)
    }));
  };

  const addDesignChoice = () => {
    if (choiceInput.trim()) {
      setSolution(prev => ({
        ...prev,
        design_choices: [...prev.design_choices, choiceInput.trim()]
      }));
      setChoiceInput('');
    }
  };

  const removeDesignChoice = (index: number) => {
    setSolution(prev => ({
      ...prev,
      design_choices: prev.design_choices.filter((_, i) => i !== index)
    }));
  };

  const handleSubmit = async () => {
    if (solution.architecture_components.length === 0) {
      alert('Please add at least one architecture component');
      return;
    }

    try {
      setSubmitting(true);
      const verificationResult = await api.verifySolution(problemId, solution);
      setResult(verificationResult);
      
      if (onSubmissionComplete) {
        onSubmissionComplete(verificationResult);
      }
    } catch (error) {
      console.error('Failed to verify solution:', error);
      alert('Failed to verify solution. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="solution-submission">
      <div className="submission-header">
        <h3>🛠️ Design Your Solution</h3>
        <p>Add your architecture components and design choices</p>
      </div>

      {/* Architecture Components Section */}
      <div className="section">
        <h4>Architecture Components</h4>
        <div className="input-group">
          <input
            type="text"
            value={componentInput}
            onChange={(e) => setComponentInput(e.target.value)}
            placeholder="e.g., Load Balancer, API Gateway, Database..."
            onKeyPress={(e) => e.key === 'Enter' && addComponent()}
          />
          <button onClick={addComponent} disabled={!componentInput.trim()}>
            Add Component
          </button>
        </div>
        
        <div className="items-list">
          {solution.architecture_components.map((component, index) => (
            <div key={index} className="item-tag">
              <span>{component}</span>
              <button onClick={() => removeComponent(index)}>×</button>
            </div>
          ))}
        </div>
      </div>

      {/* Design Choices Section */}
      <div className="section">
        <h4>Design Choices & Rationale</h4>
        <div className="input-group">
          <input
            type="text"
            value={choiceInput}
            onChange={(e) => setChoiceInput(e.target.value)}
            placeholder="e.g., Use Redis for caching to improve performance..."
            onKeyPress={(e) => e.key === 'Enter' && addDesignChoice()}
          />
          <button onClick={addDesignChoice} disabled={!choiceInput.trim()}>
            Add Choice
          </button>
        </div>
        
        <div className="items-list">
          {solution.design_choices.map((choice, index) => (
            <div key={index} className="item-tag choice-tag">
              <span>{choice}</span>
              <button onClick={() => removeDesignChoice(index)}>×</button>
            </div>
          ))}
        </div>
      </div>

      {/* Explanation Section */}
      <div className="section">
        <h4>Overall Explanation (Optional)</h4>
        <textarea
          value={solution.explanation}
          onChange={(e) => setSolution(prev => ({ ...prev, explanation: e.target.value }))}
          placeholder="Explain your overall approach, key decisions, and how your solution addresses the requirements..."
          rows={4}
        />
      </div>

      {/* Submit Button */}
      <div className="submit-section">
        <button 
          className="submit-button"
          onClick={handleSubmit}
          disabled={submitting || solution.architecture_components.length === 0}
        >
          {submitting ? '🔄 Evaluating...' : '🎯 Submit Solution'}
        </button>
      </div>

      {/* Results Display */}
      {result && (
        <div className="verification-results">
          <div className="results-header">
            <h3>📊 Solution Evaluation Results</h3>
            <div className="overall-score">
              <span className="score-label">Overall Score:</span>
              <span className="score-value">{result.overall_score}/100</span>
            </div>
          </div>

          <div className="results-grid">
            {/* Component Analysis */}
            <div className="result-section">
              <h4>🏗️ Component Analysis</h4>
              <div className="score">Score: {result.component_analysis.score}/100</div>
              
              {result.component_analysis.matched_components.length > 0 && (
                <div className="matched">
                  <strong>✅ Matched Components:</strong>
                  <ul>
                    {result.component_analysis.matched_components.map((comp, idx) => (
                      <li key={idx}>{comp}</li>
                    ))}
                  </ul>
                </div>
              )}
              
              {result.component_analysis.missing_components.length > 0 && (
                <div className="missing">
                  <strong>❌ Missing Components:</strong>
                  <ul>
                    {result.component_analysis.missing_components.map((comp, idx) => (
                      <li key={idx}>{comp}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            {/* Design Choices Analysis */}
            <div className="result-section">
              <h4>💡 Design Choices</h4>
              <div className="score">Score: {result.design_choices_analysis.score}/100</div>
              
              {result.design_choices_analysis.addressed_expectations.length > 0 && (
                <div className="addressed">
                  <strong>✅ Addressed Requirements:</strong>
                  <ul>
                    {result.design_choices_analysis.addressed_expectations.map((exp, idx) => (
                      <li key={idx}>{exp}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>

          {/* LLM Enhancement */}
          {result.llm_enhancement && !(result.llm_enhancement as any).error && (
            <div className="llm-enhancement">
              <h4>🤖 AI Enhanced Feedback</h4>
              <div className="llm-score">
                Enhanced Score: {result.llm_enhancement.llm_enhanced_score}/100
              </div>
              <div className="llm-feedback">
                <p>{result.llm_enhancement.llm_feedback}</p>
              </div>
              
              {result.llm_enhancement.strengths.length > 0 && (
                <div className="strengths">
                  <strong>💪 Strengths:</strong>
                  <ul>
                    {result.llm_enhancement.strengths.map((strength, idx) => (
                      <li key={idx}>{strength}</li>
                    ))}
                  </ul>
                </div>
              )}
              
              {result.llm_enhancement.improvements.length > 0 && (
                <div className="improvements">
                  <strong>🎯 Areas for Improvement:</strong>
                  <ul>
                    {result.llm_enhancement.improvements.map((improvement, idx) => (
                      <li key={idx}>{improvement}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {/* Recommendations */}
          {result.recommendations.length > 0 && (
            <div className="recommendations">
              <h4>💡 Recommendations</h4>
              <ul>
                {result.recommendations.map((rec, idx) => (
                  <li key={idx}>{rec}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Follow-up Questions */}
          {result.follow_up_questions && result.follow_up_questions.length > 0 && (
            <div className="follow-up-questions">
              <h4>❓ Follow-up Questions</h4>
              <p>Consider these questions to deepen your understanding:</p>
              <ul>
                {result.follow_up_questions.map((question, idx) => (
                  <li key={idx}>{question}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default SolutionSubmission;
