import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api, Problem } from '../api';

const ProblemSelector: React.FC = () => {
  const [problems, setProblems] = useState<Problem[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedDifficulty, setSelectedDifficulty] = useState<'all' | 'beginner' | 'intermediate'>('all');
  const [stats, setStats] = useState<any>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProblems = async () => {
      try {
        const response = await api.getAllProblems();
        setProblems(response.problems);
        setStats(response.stats);
      } catch (error) {
        console.error('Failed to fetch problems:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProblems();
  }, []);

  const generateRandomProblem = async (difficulty: 'beginner' | 'intermediate') => {
    try {
      setLoading(true);
      const problem = await api.generateRandomProblem(difficulty);
      navigate(`/design/${problem.id}`);
    } catch (error) {
      console.error('Failed to generate problem:', error);
      alert('Failed to generate problem. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleProblemSelect = (problemId: string) => {
    navigate(`/design/${problemId}`);
  };

  const filteredProblems = selectedDifficulty === 'all' 
    ? problems 
    : problems.filter(p => p.difficulty === selectedDifficulty);

  if (loading) {
    return <div className="loading">Loading problems...</div>;
  }

  return (
    <div className="problem-selector">
      <div className="selector-header">
        <h2>System Design Practice Platform</h2>
        <p>Choose a problem to start practicing system design</p>
        
        {stats && (
          <div className="platform-stats">
            <div className="stat-item">
              <div className="stat-icon total"></div>
              <span>{stats.total_problems} Total Problems</span>
            </div>
            <div className="stat-item">
              <div className="stat-icon beginner"></div>
              <span>{stats.difficulty_breakdown?.beginner || 0} Beginner</span>
            </div>
            <div className="stat-item">
              <div className="stat-icon intermediate"></div>
              <span>{stats.difficulty_breakdown?.intermediate || 0} Intermediate</span>
            </div>
          </div>
        )}
      </div>

      {/* Quick Start Section */}
      <div className="quick-start">
        <h3>Quick Start</h3>
        <p>Get a random problem to practice immediately</p>
        <div className="quick-start-buttons">
          <button 
            className="quick-button beginner"
            onClick={() => generateRandomProblem('beginner')}
            disabled={loading}
          >
            <div className="button-indicator beginner"></div>
            Random Beginner Problem
          </button>
          <button 
            className="quick-button intermediate"
            onClick={() => generateRandomProblem('intermediate')}
            disabled={loading}
          >
            <div className="button-indicator intermediate"></div>
            Random Intermediate Problem
          </button>
        </div>
      </div>

      {/* Filter Section */}
      <div className="filter-section">
        <h3>Browse All Problems</h3>
        <div className="difficulty-filter">
          <button 
            className={selectedDifficulty === 'all' ? 'active' : ''}
            onClick={() => setSelectedDifficulty('all')}
          >
            All ({problems.length})
          </button>
          <button 
            className={selectedDifficulty === 'beginner' ? 'active' : ''}
            onClick={() => setSelectedDifficulty('beginner')}
          >
            Beginner ({problems.filter(p => p.difficulty === 'beginner').length})
          </button>
          <button 
            className={selectedDifficulty === 'intermediate' ? 'active' : ''}
            onClick={() => setSelectedDifficulty('intermediate')}
          >
            Intermediate ({problems.filter(p => p.difficulty === 'intermediate').length})
          </button>
        </div>
      </div>

      {/* Problems Grid */}
      <div className="problems-grid">
        {filteredProblems.map(problem => (
          <div
            key={problem.id}
            className={`problem-card difficulty-${problem.difficulty.toLowerCase()}`}
            onClick={() => handleProblemSelect(problem.id)}
          >
            <div className="problem-header">
              <h3>{problem.title}</h3>
              <div className="problem-meta">
                <span className={`difficulty difficulty-${problem.difficulty.toLowerCase()}`}>
                  {problem.difficulty}
                </span>
                <div className="tags">
                  {problem.tags.slice(0, 2).map(tag => (
                    <span key={tag} className="tag">{tag}</span>
                  ))}
                </div>
              </div>
            </div>
            
            <p className="problem-description">
              {problem.description.slice(0, 150)}
              {problem.description.length > 150 ? '...' : ''}
            </p>
            
            <div className="problem-details">
              <div className="expectations">
                <strong>Key Requirements ({problem.expectations.length}):</strong>
                <ul>
                  {problem.expectations.slice(0, 2).map((exp, idx) => (
                    <li key={idx}>{exp}</li>
                  ))}
                  {problem.expectations.length > 2 && (
                    <li>+{problem.expectations.length - 2} more requirements...</li>
                  )}
                </ul>
              </div>
            </div>

            <button className="start-button">
              Start Design Challenge
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProblemSelector;