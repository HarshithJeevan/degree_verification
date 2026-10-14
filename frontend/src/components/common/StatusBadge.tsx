import React from 'react';
import './common.css';

interface StatusBadgeProps {
  status: 'verified' | 'requires_review' | 'pending' | 'rejected' | 'match' | 'mismatch' | 'review' | '';      // remove all (| '') afterwards to the end
  size?: 'sm' | 'md';
}

const StatusBadge: React.FC<StatusBadgeProps> = ({ status, size = 'md' }) => {
  const getStatusConfig = () => {
    switch (status) {
      case 'verified':
      case 'match':
        return { label: status === 'verified' ? 'Verified' : 'Match', type: 'success' };
      case 'requires_review':
      case 'review':
        return { label: status === 'requires_review' ? 'Requires Review' : 'Review', type: 'warning' };
      case 'rejected':
      case 'mismatch':
        return { label: status === 'rejected' ? 'Rejected' : 'Mismatch', type: 'danger' };
      case 'pending':
        return { label: 'Pending', type: 'neutral' };
      default:
        return { label: 'Unknown', type: 'neutral' };
    }
  };

  const config = getStatusConfig();

  return (
    <span className={`status-badge badge-${config.type} badge-${size}`}>
      <span className="badge-dot"></span>
      {config.label}
    </span>
  );
};

export default StatusBadge;
