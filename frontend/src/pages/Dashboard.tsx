import { useNavigate } from 'react-router-dom';
import PageHeader from '../components/common/PageHeader';
import StatCard from '../components/common/StatCard';
import StatusBadge from '../components/common/StatusBadge';
import { mockDashboardStats, mockRecentVerifications } from '../data/mockDashboard';
import type { RecentVerification } from '../data/mockDashboard';
import './Dashboard.css';

export default function Dashboard() {
  const navigate = useNavigate();

  return (
    <div className="dashboard-container">
      <PageHeader title="Dashboard" subtitle="Certificate Verification & Review Portal" />
      
      {/* Upload CTA Banner */}
      <div className="upload-cta-banner">
        <div className="cta-content">
          <h2>Verify a Certificate</h2>
          <p>Upload a new certificate document to begin the automated verification pipeline.</p>
        </div>
        <button className="upload-btn" onClick={() => navigate('/upload')}>
          Upload Certificate
        </button>
      </div>

      {/* Stats Grid */}
      <div className="stats-grid">
        <StatCard icon="📋" value={mockDashboardStats.totalCertificates} label="Total Certificates" color="blue" />
        <StatCard icon="✓" value={mockDashboardStats.verified} label="Verified" color="green" />
        <StatCard icon="⚠" value={mockDashboardStats.requiresReview} label="Requires Review" color="amber" />
        <StatCard icon="⏳" value={mockDashboardStats.pending} label="Pending" color="red" />
      </div>

      {/* Recent Verifications Table */}
      <div className="recent-verifications-card">
        <h3>Recent Verifications</h3>
        <div className="table-responsive">
          <table className="recent-table">
            <thead>
              <tr>
                <th>Certificate ID</th>
                <th>Student Name</th>
                <th>Roll Number</th>
                <th>Degree</th>
                <th>Status</th>
                <th>Confidence</th>
                <th>Date</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {mockRecentVerifications.map((item: RecentVerification) => (
                <tr key={item.id}>
                  <td className="mono">{item.id}</td>
                  <td>{item.studentName}</td>
                  <td className="mono">{item.rollNumber}</td>
                  <td>{item.degree}</td>
                  <td><StatusBadge status={item.status} /></td>
                  <td>{item.confidence > 0 ? `${item.confidence}%` : '—'}</td>
                  <td>{new Date(item.date).toLocaleDateString()}</td>
                  <td>
                    <button className="action-link" onClick={() => navigate('/comparison')}>
                      View
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="prototype-footer">
        <p>STTCSE . CS-202</p>
      </div>
    </div>
  );
}
