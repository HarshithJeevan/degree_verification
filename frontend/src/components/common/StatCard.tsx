import React from 'react';
import './common.css';

interface StatCardProps {
  icon: string;
  value: number;
  label: string;
  color: 'blue' | 'green' | 'amber' | 'red';
}

const StatCard: React.FC<StatCardProps> = ({ icon, value, label, color }) => {
  return (
    <div className="stat-card">
      <div className={`stat-icon-wrap icon-${color}`}>
        <span className="stat-icon" role="img" aria-label={label}>{icon}</span>
      </div>
      <div className="stat-content">
        <div className="stat-value">{value}</div>
        <div className="stat-label">{label}</div>
      </div>
    </div>
  );
};

export default StatCard;
