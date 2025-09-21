import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

interface QueueData {
  label: string;
  description?: string;
  type?: 'FIFO' | 'Priority' | 'Pub/Sub' | 'Dead Letter';
  messages?: string;
  onDelete?: (nodeId: string) => void;
}

const QueueNode: React.FC<NodeProps<QueueData>> = ({ 
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
    <div className={`custom-node queue-node ${selected ? 'selected' : ''}`}>
      <Handle type="target" position={Position.Left} />
      
      <div className="node-header">
        <div className="node-icon">📬</div>
        <div className="node-title">
          <div className="node-label">{data.label}</div>
          {data.type && (
            <div className="node-tech">{data.type}</div>
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
      
      {data.messages && (
        <div className="node-metrics">
          <span className="metric">
            Messages: <strong>{data.messages}</strong>
          </span>
        </div>
      )}
      
      <Handle type="source" position={Position.Right} />
    </div>
  );
};

export default QueueNode;
