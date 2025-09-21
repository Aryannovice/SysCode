import React, { useState, useCallback, useMemo } from 'react';
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
  NodeTypes,
  ConnectionMode,
} from 'reactflow';
import 'reactflow/dist/style.css';
import './SystemDesignCanvas.css';

// Custom Node Components - temporarily disabled
// import MicroserviceNode from './nodes/MicroserviceNode';
// import DatabaseNode from './nodes/DatabaseNode';
// import LoadBalancerNode from './nodes/LoadBalancerNode';
// import CacheNode from './nodes/CacheNode';
// import QueueNode from './nodes/QueueNode';
// import ApiGatewayNode from './nodes/ApiGatewayNode';

// Component Palette
interface ComponentType {
  id: string;
  label: string;
  nodeType: string;
  icon: string;
  color: string;
  description: string;
}

const componentTypes: ComponentType[] = [
  {
    id: 'microservice',
    label: 'Microservice',
    nodeType: 'microservice',
    icon: '🔧',
    color: '#3B82F6',
    description: 'Independent service handling specific business logic'
  },
  {
    id: 'database',
    label: 'Database',
    nodeType: 'database',
    icon: '💾',
    color: '#F59E0B',
    description: 'Data storage and persistence layer'
  },
  {
    id: 'cache',
    label: 'Cache',
    nodeType: 'cache',
    icon: '⚡',
    color: '#EF4444',
    description: 'High-speed data access layer (Redis, Memcached)'
  },
  {
    id: 'load_balancer',
    label: 'Load Balancer',
    nodeType: 'loadBalancer',
    icon: '⚖️',
    color: '#10B981',
    description: 'Distributes traffic across multiple instances'
  },
  {
    id: 'queue',
    label: 'Message Queue',
    nodeType: 'queue',
    icon: '📬',
    color: '#8B5CF6',
    description: 'Asynchronous message processing (RabbitMQ, Kafka)'
  },
  {
    id: 'api_gateway',
    label: 'API Gateway',
    nodeType: 'apiGateway',
    icon: '🚪',
    color: '#06B6D4',
    description: 'Single entry point for all client requests'
  }
];

// Node types for ReactFlow - using default nodes for now
const nodeTypes: NodeTypes = {
  // microservice: MicroserviceNode,
  // database: DatabaseNode,
  // cache: CacheNode,
  // loadBalancer: LoadBalancerNode,
  // queue: QueueNode,
  // apiGateway: ApiGatewayNode,
};

// Initial nodes and edges for demo
const initialNodes: Node[] = [
  {
    id: 'api-gateway-1',
    position: { x: 400, y: 100 },
    data: { label: '🚪 API Gateway' },
    style: { background: '#06B6D4', color: 'white', padding: '12px', borderRadius: '8px', fontWeight: 'bold' }
  },
  {
    id: 'load-balancer-1',
    position: { x: 400, y: 250 },
    data: { label: '⚖️ Load Balancer' },
    style: { background: '#10B981', color: 'white', padding: '12px', borderRadius: '8px', fontWeight: 'bold' }
  },
  {
    id: 'service-1',
    position: { x: 200, y: 400 },
    data: { label: '🔧 User Service' },
    style: { background: '#3B82F6', color: 'white', padding: '12px', borderRadius: '8px', fontWeight: 'bold' }
  },
  {
    id: 'service-2',
    position: { x: 400, y: 400 },
    data: { label: '🔧 Order Service' },
    style: { background: '#3B82F6', color: 'white', padding: '12px', borderRadius: '8px', fontWeight: 'bold' }
  },
  {
    id: 'service-3',
    position: { x: 600, y: 400 },
    data: { label: '🔧 Payment Service' },
    style: { background: '#3B82F6', color: 'white', padding: '12px', borderRadius: '8px', fontWeight: 'bold' }
  },
  {
    id: 'database-1',
    position: { x: 300, y: 550 },
    data: { label: '💾 PostgreSQL' },
    style: { background: '#F59E0B', color: 'white', padding: '12px', borderRadius: '8px', fontWeight: 'bold' }
  },
  {
    id: 'cache-1',
    position: { x: 500, y: 550 },
    data: { label: '⚡ Redis Cache' },
    style: { background: '#EF4444', color: 'white', padding: '12px', borderRadius: '8px', fontWeight: 'bold' }
  }
];

const initialEdges: Edge[] = [
  {
    id: 'api-to-lb',
    source: 'api-gateway-1',
    target: 'load-balancer-1',
    type: 'smoothstep',
    animated: true,
  },
  {
    id: 'lb-to-user',
    source: 'load-balancer-1',
    target: 'service-1',
    type: 'smoothstep',
  },
  {
    id: 'lb-to-order',
    source: 'load-balancer-1',
    target: 'service-2',
    type: 'smoothstep',
  },
  {
    id: 'lb-to-payment',
    source: 'load-balancer-1',
    target: 'service-3',
    type: 'smoothstep',
  },
  {
    id: 'user-to-db',
    source: 'service-1',
    target: 'database-1',
    type: 'smoothstep',
  },
  {
    id: 'order-to-db',
    source: 'service-2',
    target: 'database-1',
    type: 'smoothstep',
  },
  {
    id: 'services-to-cache',
    source: 'service-2',
    target: 'cache-1',
    type: 'smoothstep',
  }
];

const SystemDesignCanvas: React.FC = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [selectedComponent, setSelectedComponent] = useState<ComponentType | null>(null);
  const [isDragging, setIsDragging] = useState(false);

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds: Edge[]) => addEdge({
      ...params,
      type: 'smoothstep',
      animated: Math.random() > 0.5, // Randomly animate some connections
    }, eds)),
    [setEdges]
  );

  const onDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onDrop = useCallback(
    (event: React.DragEvent) => {
      event.preventDefault();

      if (!selectedComponent) return;

      const reactFlowBounds = (event.target as Element).closest('.react-flow')?.getBoundingClientRect();
      if (!reactFlowBounds) return;

      const position = {
        x: event.clientX - reactFlowBounds.left - 75, // Center the node
        y: event.clientY - reactFlowBounds.top - 50,
      };

      const newNode: Node = {
        id: `${selectedComponent.nodeType}-${Date.now()}`,
        position,
        data: { 
          label: `${selectedComponent.icon} ${selectedComponent.label}` 
        },
        style: { 
          background: selectedComponent.color, 
          color: 'white', 
          padding: '12px', 
          borderRadius: '8px', 
          fontWeight: 'bold' 
        }
      };

      setNodes((nds: Node[]) => nds.concat(newNode));
      setSelectedComponent(null);
      setIsDragging(false);
    },
    [selectedComponent, setNodes]
  );

  const onDragStart = useCallback((component: ComponentType) => {
    setSelectedComponent(component);
    setIsDragging(true);
  }, []);

  const deleteNode = useCallback((nodeId: string) => {
    setNodes((nds: Node[]) => nds.filter((n: Node) => n.id !== nodeId));
    setEdges((eds: Edge[]) => eds.filter((e: Edge) => e.source !== nodeId && e.target !== nodeId));
  }, [setNodes, setEdges]);

  const clearCanvas = useCallback(() => {
    setNodes([]);
    setEdges([]);
  }, [setNodes, setEdges]);

  const autoLayout = useCallback(() => {
    // Simple auto-layout logic
    const layoutNodes = nodes.map((node: Node, index: number) => {
      const col = index % 3;
      const row = Math.floor(index / 3);
      return {
        ...node,
        position: {
          x: 100 + col * 250,
          y: 100 + row * 200,
        },
      };
    });
    setNodes(layoutNodes);
  }, [nodes, setNodes]);

  return (
    <div className="system-design-canvas">
      {/* Component Palette */}
      <div className="component-palette">
        <div className="palette-header">
          <h3>Components</h3>
          <div className="palette-actions">
            <button onClick={autoLayout} className="action-btn" title="Auto Layout">
              📐
            </button>
            <button onClick={clearCanvas} className="action-btn danger" title="Clear Canvas">
              🗑️
            </button>
          </div>
        </div>
        
        <div className="component-grid">
          {componentTypes.map((component) => (
            <div
              key={component.id}
              className={`component-item ${isDragging && selectedComponent?.id === component.id ? 'dragging' : ''}`}
              draggable
              onDragStart={() => onDragStart(component)}
              style={{ borderColor: component.color }}
            >
              <div className="component-icon" style={{ backgroundColor: component.color }}>
                {component.icon}
              </div>
              <div className="component-info">
                <div className="component-label">{component.label}</div>
                <div className="component-desc">{component.description}</div>
              </div>
            </div>
          ))}
        </div>

        <div className="palette-footer">
          <p>💡 Drag components to canvas</p>
          <p>🔗 Connect nodes by dragging from handles</p>
        </div>
      </div>

      {/* React Flow Canvas */}
      <div className="canvas-area">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onDrop={onDrop}
          onDragOver={onDragOver}
          nodeTypes={nodeTypes}
          connectionMode={ConnectionMode.Loose}
          fitView
          className="react-flow-canvas"
        >
          <Background 
            variant={BackgroundVariant.Dots} 
            gap={20} 
            size={1}
            color="rgba(16, 185, 129, 0.3)"
          />
          <Controls 
            position="bottom-right"
            showZoom={true}
            showFitView={true}
            showInteractive={true}
          />
        </ReactFlow>
      </div>
    </div>
  );
};

export default SystemDesignCanvas;
