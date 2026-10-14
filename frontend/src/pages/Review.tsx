import { useState } from 'react';
import PageHeader from '../components/common/PageHeader';
import StatusBadge from '../components/common/StatusBadge';
import ConfidenceIndicator from '../components/common/ConfidenceIndicator';
import Modal from '../components/common/Modal';
import { mockCertificateIssues } from '../data/mockCertificates';
import type { CertificateField } from '../types';
import './Review.css';

export default function Review() {
  const cert = mockCertificateIssues;
  const student = cert.studentRecord;
  const flaggedFields = /*cert.fields.filter((f: CertificateField) => f.matchStatus !== 'match')*/"";
  const [showModal, setShowModal] = useState(false);
  const [modalMessage, setModalMessage] = useState('');
  const [editingField, setEditingField] = useState<string | null>(null);
  const [notes, setNotes] = useState('');

  function handleDecision(decision: 'approve' | 'reject' | 'further_review') {
    const labels: Record<string, string> = {
      approve: 'Certificate APPROVED',
      reject: 'Certificate REJECTED',
      further_review: 'Sent for FURTHER REVIEW',
    };
    setModalMessage(`${labels[decision]}. This is a frontend prototype action. Backend integration pending.`);
    setShowModal(true);
  }

  function handleFieldAction(fieldName: string, action: string) {
    setModalMessage(`Field "${fieldName}": action "${action}" recorded. This is a frontend prototype action.`);
    setShowModal(true);
  }

  return (
    <div className="review-container">
      <PageHeader title="Human Review" subtitle="Review flagged certificates and make verification decisions" />

      {/* Certificate Info Header */}
      <div className="review-info-grid">
        <div className="review-info-card">
          <span className="review-info-label">Certificate ID</span>
          <span className="review-info-value mono">{cert.id}</span>
        </div>
        <div className="review-info-card">
          <span className="review-info-label">Student Name</span>
          <span className="review-info-value">{/*student.englishName*/}</span>
        </div>
        <div className="review-info-card">
          <span className="review-info-label">Roll Number</span>
          <span className="review-info-value mono">{/*student.rollNumber*/}</span>
        </div>
        <div className="review-info-card">
          <span className="review-info-label">Overall Confidence</span>
          <span className="review-info-value">{cert.overallConfidence}%</span>
        </div>
      </div>

      {/* Flagged Fields */}
      <h3 className="review-section-title">⚠ Flagged Fields</h3>
      {/*flaggedFields.map((field: CertificateField) => (
        <div key={field.name} className="review-field-card">
          <div className="review-field-header">
            <h4>{field.name}</h4>
            <StatusBadge status={field.matchStatus} />
          </div>
          <div className="review-field-body">
            <div className="review-compare">
              <div className="review-compare-col">
                <span className="review-compare-label">Expected Value</span>
                <div className="review-compare-value expected">{field.expectedValue}</div>
              </div>
              <div className="review-compare-col">
                <span className="review-compare-label">Extracted Value</span>
                <div className="review-compare-value extracted">{field.extractedValue}</div>
              </div>
            </div>
            <div className="review-field-meta">
              <span>Confidence: <ConfidenceIndicator value={field.confidence} showBar size="sm" /></span>
              <span>Match Type: <strong>{field.matchType}</strong></span>
            </div>
            {field.reason && (
              <div className="review-field-reason">
                <span>ℹ</span> {field.reason}
              </div>
            )}
            <div className="review-field-actions">
              <button className="btn-sm btn-outline" onClick={() => handleFieldAction(field.name, 'Accept Extracted')}>Accept Extracted</button>
              <button className="btn-sm btn-success" onClick={() => handleFieldAction(field.name, 'Use Expected')}>Use Expected</button>
              <button className="btn-sm btn-warning" onClick={() => setEditingField(editingField === field.name ? null : field.name)}>Edit Manually</button>
            </div>
            {editingField === field.name && (
              <div className="manual-edit">
                <input type="text" className="manual-input" placeholder="Enter corrected value" />
                <button className="btn-sm btn-primary" onClick={() => { handleFieldAction(field.name, 'Manual Edit'); setEditingField(null); }}>Save</button>
              </div>
            )}
          </div>
        </div>
      ))/*}

      {/* All Fields Reference */}
      <div className="review-all-fields">
        <h3 className="review-section-title">All Fields (Reference)</h3>
        <table className="review-table">
          <thead>
            <tr>
              <th>Field</th>
              <th>Expected</th>
              <th>Extracted</th>
              <th>Status</th>
              <th>Confidence</th>
            </tr>
          </thead>
          <tbody>
            {/*cert.fields.map((field: CertificateField) => (
              <tr key={field.name}>
                <td>{field.name}</td>
                <td className="mono">{field.expectedValue}</td>
                <td className="mono">{field.extractedValue}</td>
                <td><StatusBadge status={field.matchStatus} size="sm" /></td>
                <td><ConfidenceIndicator value={field.confidence} size="sm" /></td>
              </tr>
            ))*/}
          </tbody>
        </table>
      </div>

      {/* Review Decision */}
      <div className="review-decision">
        <h3 className="review-section-title">Review Decision</h3>
        <div className="review-notes">
          <label>Notes (optional)</label>
          <textarea
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            placeholder="Add any review notes or observations…"
          />
        </div>
        <div className="review-decision-buttons">
          <button className="btn-lg btn-success" onClick={() => handleDecision('approve')}>✓ Approve Certificate</button>
          <button className="btn-lg btn-danger" onClick={() => handleDecision('reject')}>✕ Reject Certificate</button>
          <button className="btn-lg btn-warning" onClick={() => handleDecision('further_review')}>⟳ Send for Further Review</button>
        </div>
      </div>

      <div className="prototype-footer">
        <p>STTCSE . CS-202</p>
      </div>

      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="Review Action">
        <p>{modalMessage}</p>
      </Modal>
    </div>
  );
}
