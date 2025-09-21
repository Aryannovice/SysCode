# System Design LeetCode Assistant

AI-powered system design learning platform with interactive canvas and intelligent problem solving.

## Quick Start

### Docker (Recommended)
```bash
docker-compose up --build
```
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`

### Manual Setup

**Backend (FastAPI)**
```bash
cd services/api
python -m app.main
```

**Frontend (React)**
```bash
cd services/frontend
npm install && npm start
```

## Features

- **Interactive Canvas**: Drag-and-drop system architecture components
- **AI Assistant**: LeetCode-style system design problems with intelligent hints
- **RAG System**: Context-aware responses using ChromaDB
- **Real-time Visualization**: 2D/3D component relationships

## Tech Stack

**Backend**: FastAPI, ChromaDB, OpenAI  
**Frontend**: React, TypeScript, ReactFlow, Three.js

## API Endpoints

- `GET /api/v1/problems` - List all problems
- `GET /api/v1/problems/{id}` - Get specific problem
- `POST /api/v1/assistant/chat` - Chat with AI assistant
- `GET /health` - Health check
