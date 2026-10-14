import React from 'react';
import './common.css';

interface ConfidenceIndicatorProps {
  value: number;
  showBar?: boolean;
  size?: 'sm' | 'md';
}

const ConfidenceIndicator: React.FC<ConfidenceIndicatorProps> = ({ value, showBar = true, size = 'md' }) => {
  const getColorClass = () => {
    if (value >= 90) return 'color-green';
    if (value >= 75) return 'color-amber';
    return 'color-red';
  };

  const colorClass = getColorClass();

  return (
    <div className={`confidence-indicator size-${size}`}>
      <span className={`confidence-text ${colorClass}`}>{value.toFixed(1)}%</span>
      {showBar && (
        <div className="confidence-bar">
          <div 
            className={`confidence-fill bg-${colorClass}`} 
            style={{ width: `${Math.min(100, Math.max(0, value))}%` }}
          ></div>
        </div>
      )}
    </div>
  );
};

export default ConfidenceIndicator;
