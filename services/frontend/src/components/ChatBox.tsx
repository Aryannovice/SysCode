import React, { useState, useEffect, useRef } from 'react';
import { api, AssistantResponse } from '../api';

interface Message {
  id: string;
  type: 'user' | 'assistant' | 'system' | 'hints';
  content: string;
  timestamp: Date;
  relatedConcepts?: string[];
  confidence?: string;
}

interface ChatBoxProps {
  problemId?: string;
}

const ChatBox: React.FC<ChatBoxProps> = ({ problemId }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'assistant',
      content: 'Hi! I\'m your AI System Design Assistant. Ask me about system design concepts, architecture patterns, or get hints for your current problem. I\'m here to help you learn!',
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [assistantStatus, setAssistantStatus] = useState<any>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Check assistant status on mount
    const checkStatus = async () => {
      try {
        const status = await api.getAssistantStatus();
        setAssistantStatus(status);
        
        if (!status.llm_available) {
          const systemMessage: Message = {
            id: 'status',
            type: 'system',
            content: '⚠️ AI assistant is running in fallback mode. OpenAI API key not configured. You\'ll still get helpful responses, but they won\'t be as intelligent.',
            timestamp: new Date()
          };
          setMessages(prev => [...prev, systemMessage]);
        }
      } catch (error) {
        console.error('Failed to check assistant status:', error);
      }
    };
    checkStatus();
  }, []);

  const getHints = async () => {
    if (!problemId) {
      alert('No problem selected for hints');
      return;
    }
    
    setIsLoading(true);
    try {
      const hintsResponse = await api.getDynamicHints(problemId);
      const hintsMessage: Message = {
        id: Date.now().toString(),
        type: 'hints',
        content: `Here are some hints for this problem:\n\n${hintsResponse.hints.map((hint, idx) => `${idx + 1}. ${hint}`).join('\n')}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, hintsMessage]);
    } catch (error) {
      console.error('Failed to get hints:', error);
      const errorMessage: Message = {
        id: Date.now().toString(),
        type: 'system',
        content: 'Sorry, I couldn\'t get hints right now. Please try again later.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    const question = inputValue;
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await api.askAssistant({
        question,
        context_problem_id: problemId
      });
      
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: response.answer,
        timestamp: new Date(),
        relatedConcepts: response.related_concepts,
        confidence: response.confidence
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Failed to get assistant response:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'system',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className={`chat-box ${isMinimized ? 'minimized' : ''}`}>
      <button 
        className="chat-toggle"
        onClick={() => setIsMinimized(!isMinimized)}
        title={isMinimized ? 'Open chat' : 'Minimize chat'}
      >
        {isMinimized ? '💬' : '−'}
      </button>
      
      {!isMinimized && (
        <>
          <div className="chat-header">
            <h3>🤖 AI Assistant</h3>
            <div className="chat-status">
              <span className={isLoading ? 'thinking' : 'ready'}>
                {isLoading ? 'Thinking...' : assistantStatus?.llm_available ? '🟢 AI Ready' : '🟡 Fallback Mode'}
              </span>
            </div>
          </div>

      <div className="chat-actions">
        {problemId && (
          <button 
            className="hint-button"
            onClick={getHints}
            disabled={isLoading}
          >
            💡 Get Hints
          </button>
        )}
        <div className="quick-questions">
          <small>Quick questions:</small>
          <button onClick={() => setInputValue('What is load balancing?')}>Load Balancing</button>
          <button onClick={() => setInputValue('How does caching work?')}>Caching</button>
          <button onClick={() => setInputValue('What is database sharding?')}>Sharding</button>
        </div>
      </div>

      <div className="chat-messages">
        {messages.map(message => (
          <div key={message.id} className={`message ${message.type}`}>
            <div className="message-content">
              {message.type === 'hints' ? (
                <div className="hints-content">
                  <div className="hints-header">💡 Hints for this problem:</div>
                  <div className="hints-list">
                    {message.content.split('\n').filter(line => line.trim()).map((line, idx) => (
                      <div key={idx} className="hint-item">{line}</div>
                    ))}
                  </div>
                </div>
              ) : (
                <>
                  {message.content.split('\n').map((line, idx) => (
                    <div key={idx}>{line}</div>
                  ))}
                </>
              )}
            </div>
            
            {message.relatedConcepts && message.relatedConcepts.length > 0 && (
              <div className="related-concepts">
                <small>Related concepts: {message.relatedConcepts.join(', ')}</small>
              </div>
            )}
            
            <div className="message-footer">
              <div className="message-timestamp">
                {message.timestamp.toLocaleTimeString()}
              </div>
              {message.confidence && (
                <div className={`confidence confidence-${message.confidence}`}>
                  {message.confidence} confidence
                </div>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message assistant loading">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input">
        <div className="input-container">
          <textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask about system design concepts, patterns, or get help with your current problem..."
            rows={2}
            disabled={isLoading}
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || isLoading}
            className="send-button"
          >
            {isLoading ? '...' : 'Send'}
          </button>
        </div>
      </div>
        </>
      )}
    </div>
  );
};

export default ChatBox;
