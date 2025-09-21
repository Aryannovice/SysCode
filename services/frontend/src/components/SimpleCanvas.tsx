import React, { useState, useCallback } from 'react';
import ReactFlow, {
  Node,
  Edge,
  addEdge,
  Connection,
  useNodesState,
  useEdgesState,
  Controls,
  Background,
  BackgroundVariant,
} from 'reactflow';
import 'reactflow/dist/style.css';

// Simple initial setup to test React Flow
const initialNodes: Node[] = [
  {
    id: '1',
    position: { x: 100, y: 100 },
    data: { label: 'API Gateway' },
    style: { background: '#06B6D4', color: 'white', padding: '10px', borderRadius: '8px' }
  },
  {
    id: '2',
    position: { x: 100, y: 200 },
    data: { label: 'Microservice' },
    style: { background: '#3B82F6', color: 'white', padding: '10px', borderRadius: '8px' }
  },
  {
    id: '3',
    position: { x: 300, y: 200 },
    data: { label: 'Database' },
    style: { background: '#F59E0B', color: 'white', padding: '10px', borderRadius: '8px' }
  }
];

const initialEdges: Edge[] = [
  { id: 'e1-2', source: '1', target: '2', animated: true },
  { id: 'e2-3', source: '2', target: '3' }
];

const SimpleCanvas: React.FC = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds: Edge[]) => addEdge(params, eds)),
    [setEdges]
  );

  return (
    <div style={{ width: '100%', height: '500px' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        fitView
      >
        <Controls />
        <Background variant={BackgroundVariant.Dots} />
      </ReactFlow>
    </div>
  );
};

export default SimpleCanvas;
