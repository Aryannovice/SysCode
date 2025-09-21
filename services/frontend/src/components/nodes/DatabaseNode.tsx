import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

interface DatabaseData {
  label: string;
  description?: string;
  type?: 'SQL' | 'NoSQL' | 'Graph' | 'Time-Series';
  size?: string;
  onDelete?: (nodeId: string) => void;
}

const DatabaseNode: React.FC<NodeProps<DatabaseData>> = ({ 
  id, 
  data, 
  selected 
}) => {
  const handleDelete = () => {
    if (data.onDelete) {
      data.onDelete(id);
    }
  };

  const getTypeColor = (type?: string) => {
    switch (type) {
      case 'SQL': return '#3B82F6';
      case 'NoSQL': return '#F59E0B';
      case 'Graph': return '#8B5CF6';
      case 'Time-Series': return '#EF4444';
      default: return '#6B7280';
    }
  };

  return (
    <div className={`custom-node database-node ${selected ? 'selected' : ''}`}>
      <Handle type="target" position={Position.Top} />
      
      <div className="node-header">
        <div className="node-icon">💾</div>
        <div className="node-title">
          <div className="node-label">{data.label}</div>
          {data.type && (
            <div 
              className="node-badge"
              style={{ backgroundColor: getTypeColor(data.type) }}
            >
              {data.type}
            </div>
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
      
      {data.size && (
        <div className="node-metrics">
          <span className="metric">
            Size: <strong>{data.size}</strong>
          </span>
        </div>
      )}
      
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
};

export default DatabaseNode;

