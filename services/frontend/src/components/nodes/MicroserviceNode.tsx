import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

interface MicroserviceData {
  label: string;
  description?: string;
  technology?: string;
  instances?: number;
  onDelete?: (nodeId: string) => void;
}

const MicroserviceNode: React.FC<NodeProps<MicroserviceData>> = ({ 
  id, 
  data, 
  selected 
}) => {
  const handleDelete = () => {
    if (data.onDelete) {
      data.onDelete(id);
    }
  };

  return (
    <div className={`custom-node microservice-node ${selected ? 'selected' : ''}`}>
      <Handle type="target" position={Position.Top} />
      
      <div className="node-header">
        <div className="node-icon">🔧</div>
        <div className="node-title">
          <div className="node-label">{data.label}</div>
          {data.technology && (
            <div className="node-tech">{data.technology}</div>
          )}
        </div>
        {selected && (
          <button className="delete-btn" onClick={handleDelete} title="Delete">
            ✕
          </button>
        )}
      </div>
      
      {data.description && (
        <div className="node-description">{data.description}</div>
      )}
      
      {data.instances && (
        <div className="node-metrics">
          <span className="metric">
            Instances: <strong>{data.instances}</strong>
          </span>
        </div>
      )}
      
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
};

export default MicroserviceNode;

