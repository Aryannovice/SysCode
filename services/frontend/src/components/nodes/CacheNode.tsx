import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

interface CacheData {
  label: string;
  description?: string;
  type?: 'In-Memory' | 'Distributed' | 'CDN';
  hitRate?: string;
  onDelete?: (nodeId: string) => void;
}

const CacheNode: React.FC<NodeProps<CacheData>> = ({ 
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
    <div className={`custom-node cache-node ${selected ? 'selected' : ''}`}>
      <Handle type="target" position={Position.Top} />
      
      <div className="node-header">
        <div className="node-icon">⚡</div>
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
      
      {data.hitRate && (
        <div className="node-metrics">
          <span className="metric">
            Hit Rate: <strong>{data.hitRate}</strong>
          </span>
        </div>
      )}
      
      <Handle type="source" position={Position.Bottom} />
      <Handle type="source" position={Position.Left} />
      <Handle type="source" position={Position.Right} />
    </div>
  );
};

export default CacheNode;

