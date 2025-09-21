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

- **Interactive Canvas**: Drag-and-drop system architecture components(in Version2, I will implement)
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

Some pics:
<img width="840" height="839" alt="image" src="https://github.com/user-attachments/assets/390e7f64-2aaf-4ec7-82a7-2e8b7701ba93" />


<img width="1892" height="859" alt="Screenshot 2025-09-20 180719" src="https://github.com/user-attachments/assets/30555312-5088-4d32-a264-c388a7a08209" />


<img width="1916" height="905" alt="Screenshot 2025-09-21 193026" src="https://github.com/user-attachments/assets/573ec290-27a4-41ef-869d-b6ecf9ca296a" />


<img width="1912" height="862" alt="Screenshot 2025-09-21 193040" src="https://github.com/user-attachments/assets/e5d1741f-feb8-49e9-94a9-4de3685b6828" />

<img width="1871" height="832" alt="Screenshot 2025-09-20 180753" src="https://github.com/user-attachments/assets/8f7300c0-e9c6-4799-ae8a-3ddff9c88df6" />



