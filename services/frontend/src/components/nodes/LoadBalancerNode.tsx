import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

interface LoadBalancerData {
  label: string;
  description?: string;
  algorithm?: 'Round Robin' | 'Least Connections' | 'IP Hash' | 'Weighted';
  throughput?: string;
  onDelete?: (nodeId: string) => void;
}

const LoadBalancerNode: React.FC<NodeProps<LoadBalancerData>> = ({ 
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
    <div className={`custom-node load-balancer-node ${selected ? 'selected' : ''}`}>
      <Handle type="target" position={Position.Top} />
      
      <div className="node-header">
        <div className="node-icon">⚖️</div>
        <div className="node-title">
          <div className="node-label">{data.label}</div>
          {data.algorithm && (
            <div className="node-tech">{data.algorithm}</div>
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
      
      {data.throughput && (
        <div className="node-metrics">
          <span className="metric">
            Throughput: <strong>{data.throughput}</strong>
          </span>
        </div>
      )}
      
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
};

export default LoadBalancerNode;

