import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

interface ApiGatewayData {
  label: string;
  description?: string;
  routes?: number;
  metrics?: {
    requests?: string;
    latency?: string;
  };
  onDelete?: (nodeId: string) => void;
}

const ApiGatewayNode: React.FC<NodeProps<ApiGatewayData>> = ({ 
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
    <div className={`custom-node api-gateway-node ${selected ? 'selected' : ''}`}>
      <Handle type="target" position={Position.Top} />
      
      <div className="node-header">
        <div className="node-icon">🚪</div>
        <div className="node-title">
          <div className="node-label">{data.label}</div>
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
      
      <div className="node-metrics">
        {data.metrics?.requests && (
          <span className="metric">
            Requests: <strong>{data.metrics.requests}</strong>
          </span>
        )}
        {data.metrics?.latency && (
          <span className="metric">
            Latency: <strong>{data.metrics.latency}</strong>
          </span>
        )}
        {data.routes && (
          <span className="metric">
            Routes: <strong>{data.routes}</strong>
          </span>
        )}
      </div>
      
      <Handle type="source" position={Position.Bottom} />
      <Handle type="source" position={Position.Left} />
      <Handle type="source" position={Position.Right} />
    </div>
  );
};

export default ApiGatewayNode;

