import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useParams, Link } from 'react-router-dom';
import FlowCanvas from './components/FlowCanvas';
import ChatBox from './components/ChatBox';
import ProblemSelector from './components/ProblemSelector';
import SolutionSubmission from './components/SolutionSubmission';
import { api, Problem, VerificationResult } from './api';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <header className="app-header">
          <h1>System Design LeetCode Platform</h1>
          <p>Practice system design with AI-powered feedback</p>
        </header>
        
        <Routes>
          <Route path="/" element={<ProblemSelector />} />
          <Route path="/design/:problemId" element={<DesignWorkspace />} />
        </Routes>
      </div>
    </Router>
  );
}

const DesignWorkspace: React.FC = () => {
  const { problemId } = useParams<{ problemId: string }>();
  const [problem, setProblem] = useState<Problem | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'canvas' | 'solution'>('solution');
  const [verificationResult, setVerificationResult] = useState<VerificationResult | null>(null);
  const [isHeaderCollapsed, setIsHeaderCollapsed] = useState(false);

  useEffect(() => {
    const fetchProblem = async () => {
      if (!problemId) return;
      
      try {
        const problemData = await api.getProblem(problemId);
        setProblem(problemData);
      } catch (error) {
        console.error('Failed to fetch problem:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProblem();
  }, [problemId]);

  const handleSubmissionComplete = (result: VerificationResult) => {
    setVerificationResult(result);
  };

  if (loading) {
    return <div className="loading">Loading problem...</div>;
  }

  if (!problem) {
    return (
      <div className="error">
        <h2>Problem not found</h2>
        <Link to="/">← Back to problem selection</Link>
      </div>
    );
  }

  return (
    <div className="design-workspace">
      <div className={`workspace-header ${isHeaderCollapsed ? 'collapsed' : ''}`}>
        <div className="header-toggle">
          <button 
            className="collapse-button"
            onClick={() => setIsHeaderCollapsed(!isHeaderCollapsed)}
            title={isHeaderCollapsed ? 'Expand header' : 'Collapse header'}
          >
            {isHeaderCollapsed ? '▼' : '▲'}
          </button>
        </div>
        
        <div className="header-content">
          <div className="problem-info">
            <Link to="/" className="back-button">← Back to Problems</Link>
            <h2>{problem.title}</h2>
            <div className="problem-meta">
              <span className={`difficulty difficulty-${problem.difficulty}`}>
                {problem.difficulty}
              </span>
              <div className="tags">
                {problem.tags.map(tag => (
                  <span key={tag} className="tag">{tag}</span>
                ))}
              </div>
            </div>
          </div>
          
          <div className="workspace-tabs">
            <button 
              className={`tab-button ${activeTab === 'solution' ? 'active' : ''}`}
              onClick={() => setActiveTab('solution')}
            >
              <div className="tab-indicator solution"></div>
              Solution Builder
            </button>
            <button 
              className={`tab-button ${activeTab === 'canvas' ? 'active' : ''}`}
              onClick={() => setActiveTab('canvas')}
            >
              <div className="tab-indicator canvas"></div>
              Visual Canvas
            </button>
          </div>
        </div>
      </div>

      {!isHeaderCollapsed && (
        <div className="problem-description">
          <h3>Problem Description</h3>
          <p>{problem.description}</p>
          
          <div className="requirements">
            <h4>Requirements ({problem.expectations.length})</h4>
            <ul>
              {problem.expectations.map((exp, idx) => (
                <li key={idx}>{exp}</li>
              ))}
            </ul>
          </div>
        </div>
      )}

      <div className="workspace-content">
        {activeTab === 'solution' && (
          <div className="solution-workspace">
            <SolutionSubmission 
              problemId={problemId!}
              onSubmissionComplete={handleSubmissionComplete}
            />
          </div>
        )}
        
        {activeTab === 'canvas' && (
          <div className="canvas-workspace">
            <div className="workspace-left">
              <FlowCanvas />
            </div>
            <div className="workspace-right">
              <ChatBox problemId={problemId} />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;