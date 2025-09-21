import React, { useState, useCallback, useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Box, Html } from '@react-three/drei';
import * as THREE from 'three';

interface Component {
  id: string;
  type: string;
  name: string;
  position: [number, number, number];
  color: string;
  connections: string[];
}

const FlowCanvas: React.FC = () => {
  const [components, setComponents] = useState<Component[]>([
    {
      id: 'lb1',
      type: 'load_balancer',
      name: 'Load Balancer',
      position: [0, 2, 0],
      color: '#4CAF50',
      connections: ['api1', 'api2']
    },
    {
      id: 'api1',
      type: 'api_gateway',
      name: 'API Gateway 1',
      position: [-2, 0, 0],
      color: '#2196F3',
      connections: ['db1', 'cache1']
    },
    {
      id: 'api2',
      type: 'api_gateway',
      name: 'API Gateway 2',
      position: [2, 0, 0],
      color: '#2196F3',
      connections: ['db1', 'cache1']
    },
    {
      id: 'db1',
      type: 'database',
      name: 'Primary DB',
      position: [-2, -2, 0],
      color: '#FF9800',
      connections: []
    },
    {
      id: 'cache1',
      type: 'cache',
      name: 'Redis Cache',
      position: [2, -2, 0],
      color: '#E91E63',
      connections: []
    }
  ]);

  const [selectedComponent, setSelectedComponent] = useState<string | null>(null);

  const handleComponentClick = useCallback((componentId: string) => {
    setSelectedComponent(componentId);
  }, []);

  const addComponent = useCallback((type: string) => {
    const newComponent: Component = {
      id: `comp_${Date.now()}`,
      type,
      name: `New ${type}`,
      position: [Math.random() * 4 - 2, Math.random() * 4 - 2, 0],
      color: getColorForType(type),
      connections: []
    };
    setComponents(prev => [...prev, newComponent]);
  }, []);

  return (
    <div className="flow-canvas">
      <div className="canvas-toolbar">
        <h3>System Architecture</h3>
        <div className="component-palette">
          <button onClick={() => addComponent('database')}>+ Database</button>
          <button onClick={() => addComponent('cache')}>+ Cache</button>
          <button onClick={() => addComponent('load_balancer')}>+ Load Balancer</button>
          <button onClick={() => addComponent('microservice')}>+ Service</button>
        </div>
      </div>

      <div className="canvas-container">
        <Canvas camera={{ position: [0, 0, 10], fov: 50 }}>
          <ambientLight intensity={0.5} />
          <pointLight position={[10, 10, 10]} />
          
          {components.map(component => (
            <ComponentNode
              key={component.id}
              component={component}
              isSelected={selectedComponent === component.id}
              onClick={() => handleComponentClick(component.id)}
            />
          ))}

          {/* Render connections */}
          {components.map(component =>
            component.connections.map(targetId => {
              const target = components.find(c => c.id === targetId);
              return target ? (
                <ConnectionLine
                  key={`${component.id}-${targetId}`}
                  from={component.position}
                  to={target.position}
                />
              ) : null;
            })
          )}

          <OrbitControls enablePan enableZoom enableRotate />
        </Canvas>
      </div>

      {selectedComponent && (
        <ComponentDetails
          component={components.find(c => c.id === selectedComponent)!}
          onClose={() => setSelectedComponent(null)}
        />
      )}
    </div>
  );
};

const ComponentNode: React.FC<{
  component: Component;
  isSelected: boolean;
  onClick: () => void;
}> = ({ component, isSelected, onClick }) => {
  const meshRef = useRef<THREE.Mesh>(null!);
  
  useFrame((state) => {
    if (isSelected && meshRef.current) {
      meshRef.current.scale.setScalar(1 + Math.sin(state.clock.elapsedTime * 3) * 0.1);
    }
  });

  return (
    <group position={component.position}>
      <Box
        ref={meshRef}
        args={[1.5, 1, 0.2]}
        onClick={onClick}
        onPointerOver={() => document.body.style.cursor = 'pointer'}
        onPointerOut={() => document.body.style.cursor = 'auto'}
      >
        <meshStandardMaterial
          color={component.color}
          transparent
          opacity={isSelected ? 0.8 : 0.6}
        />
      </Box>
      <Html>
        <div className="component-label">
          <div className="component-name">{component.name}</div>
          <div className="component-type">{component.type}</div>
        </div>
      </Html>
    </group>
  );
};

const ConnectionLine: React.FC<{
  from: [number, number, number];
  to: [number, number, number];
}> = ({ from, to }) => {
  const points = [new THREE.Vector3(...from), new THREE.Vector3(...to)];
  const geometry = new THREE.BufferGeometry().setFromPoints(points);
  
  return (
    <line>
      <bufferGeometry attach="geometry" {...geometry} />
      <lineBasicMaterial attach="material" color="#666" />
    </line>
  );
};

const ComponentDetails: React.FC<{
  component: Component;
  onClose: () => void;
}> = ({ component, onClose }) => {
  return (
    <div className="component-details">
      <div className="details-header">
        <h4>{component.name}</h4>
        <button onClick={onClose}>×</button>
      </div>
      <div className="details-content">
        <p><strong>Type:</strong> {component.type}</p>
        <p><strong>Connections:</strong> {component.connections.length}</p>
        <div className="component-actions">
          <button>Edit Properties</button>
          <button>View Metrics</button>
          <button>Delete</button>
        </div>
      </div>
    </div>
  );
};

const getColorForType = (type: string): string => {
  const colors = {
    database: '#FF9800',
    cache: '#E91E63',
    load_balancer: '#4CAF50',
    api_gateway: '#2196F3',
    microservice: '#9C27B0',
    message_queue: '#FF5722'
  };
  return colors[type as keyof typeof colors] || '#607D8B';
};

export default FlowCanvas;
