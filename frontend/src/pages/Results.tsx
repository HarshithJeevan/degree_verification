import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import PageHeader from '../components/common/PageHeader';
import ConfidenceIndicator from '../components/common/ConfidenceIndicator';
import { mockCertificateClean, mockCertificateIssues } from '../data/mockCertificates';
import type { Certificate, CertificateField } from '../types';
import './Results.css';

export default function Results() {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<'verified' | 'flagged'>('flagged');
  const cert: Certificate = activeTab === 'verified' ? mockCertificateClean : mockCertificateIssues;
  const passedFields = /*cert.fields.filter((f: CertificateField) => f.matchStatus === 'match');*/"";
  const flaggedFields = /*cert.fields.filter((f: CertificateField) => f.matchStatus !== 'match');*/"";

  return (
    <div className="results-container">
      <PageHeader title="Verification Result" subtitle={`Certificate ${cert.id}`} />

      {/* Tab Switcher */}
      <div className="result-tabs">
        <button
          className={`tab-btn ${activeTab === 'verified' ? 'active' : ''}`}
          onClick={() => setActiveTab('verified')}
        >
          View Verified Example
        </button>
        <button
          className={`tab-btn ${activeTab === 'flagged' ? 'active' : ''}`}
          onClick={() => setActiveTab('flagged')}
        >
          View Flagged Example
        </button>
      </div>

      {/* Verdict Banner */}
      <div className={`verdict-banner ${cert.status === 'verified' ? 'verdict-pass' : 'verdict-review'}`}>
        <div className="verdict-icon">
          {cert.status === 'verified' ? '✓' : '⚠'}
        </div>
        <h2 className="verdict-title">
          {cert.status === 'verified' ? 'VERIFICATION PASSED' : 'REQUIRES HUMAN REVIEW'}
        </h2>
        <p className="verdict-subtitle">
          {cert.status === 'verified'
            ? 'Certificate appears consistent with the reference student record.'
            : 'Certificate has discrepancies that require manual verification.'}
        </p>
        <div className="verdict-confidence">
          Overall Confidence: <strong>{cert.overallConfidence}%</strong>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="summary-cards">
        <div className="summary-card pass">
          <div className="summary-count">{passedFields.length}</div>
          <div className="summary-label">Fields Passed</div>
        </div>
        <div className={`summary-card ${flaggedFields.length > 0 ? 'fail' : 'pass'}`}>
          <div className="summary-count">{flaggedFields.length}</div>
          <div className="summary-label">Fields Flagged</div>
        </div>
        <div className="summary-card neutral">
          <div className="summary-count">{cert.overallConfidence}%</div>
          <div className="summary-label">Confidence</div>
        </div>
      </div>

      {/* Flagged Issues */}
      {flaggedFields.length > 0 && (
        <div className="flagged-section">
          <h3>Flagged Issues</h3>
          {/*flaggedFields.map((field: CertificateField) => (
            <div key={field.name} className="flagged-item">
              <div className="flagged-field-name">{field.name}</div>
              <div className="flagged-detail">
                <span className="extracted">Extracted: <strong>{field.extractedValue}</strong></span>
                <span className="expected">Expected: <strong>{field.expectedValue}</strong></span>
              </div>
              {field.reason && <div className="flagged-reason">{field.reason}</div>}
            </div>
          ))*/}
        </div>
      )}

      {/* All Field Results */}
      <div className="all-fields-section">
        <h3>Field Results</h3>
        <div className="field-results-list">
          {/*cert.fields.map((field: CertificateField) => (
            <div key={field.name} className={`field-result-row ${field.matchStatus}`}>
              <span className="field-result-icon">
                {field.matchStatus === 'match' ? '✓' : field.matchStatus === 'review' ? '⚠' : '✕'}
              </span>
              <span className="field-result-name">{field.name}</span>
              <span className={`field-result-status ${field.matchStatus}`}>
                {field.matchStatus === 'match' ? 'Match' : field.matchStatus === 'review' ? 'Review' : 'Mismatch'}
              </span>
              <ConfidenceIndicator value={field.confidence} showBar size="sm" />
            </div>
          ))*/}
        </div>
      </div>

      {/* Actions */}
      <div className="results-actions">
        <button className="btn-outline" onClick={() => navigate('/comparison')}>View Detailed Comparison</button>
        {cert.status === 'requires_review' && (
          <button className="btn-warning" onClick={() => navigate('/review')}>Send to Review</button>
        )}
      </div>

      <div className="prototype-footer">
        <p>STTCSE . CS-202</p>
      </div>
    </div>
  );
}
