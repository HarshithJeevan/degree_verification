import { useNavigate } from 'react-router-dom';
import PageHeader from '../components/common/PageHeader';
import StatusBadge from '../components/common/StatusBadge';
import ConfidenceIndicator from '../components/common/ConfidenceIndicator';
import { mockCertificateIssues } from '../data/mockCertificates';
import type { CertificateField, LayoutRegion } from '../types';
import './Comparison.css';

export default function Comparison() {
  const navigate = useNavigate();
  const cert = mockCertificateIssues;
  const student = cert.studentRecord;

  return (
    <div className="comparison-container">
      <PageHeader 
        title="Certificate Comparison" 
        subtitle={`Certificate ${cert.id} · ${/*student.englishName*/""}`}
      />

      {/* Side-by-side comparison */}
      <div className="comparison-grid">
        {/* Left: Uploaded Certificate */}
        <div className="comp-panel">
          <div className="comp-panel-header">📄 Uploaded Certificate</div>
          <div className="certificate-preview">
            <div className="cert-frame">
              <div className="cert-header-text">
                <p className="cert-hindi">भारतीय प्रौद्योगिकी संस्थान गांधीनगर</p>
                <h3>INDIAN INSTITUTE OF TECHNOLOGY GANDHINAGAR</h3>
              </div>
              <div className="cert-title">DEGREE CERTIFICATE</div>
              <div className="cert-body">
                <p>This is to certify that</p>
                <p className="cert-name">{/*student.englishName*/}</p>
                <p className="cert-name-hindi">{/*student.hindiName*/}</p>
                <p>Roll Number: <strong>{/*student.rollNumber*/}</strong></p>
                <p>has successfully completed the requirements for the degree of</p>
                <p className="cert-degree">{/*student.degree*/}</p>
                <p>in <strong>{/*student.branch*/}</strong></p>
                <p className="cert-date">Date: {/*student.dateOfIssue*/}</p>
                <p>CGPA: {/*student.cgpa*/} | Convocation: {/*student.convocationNumber*/}</p>
              </div>
              <div className="cert-watermark">SAMPLE — Mock Data</div>
            </div>
          </div>
        </div>

        {/* Right: Reference Information */}
        <div className="comp-panel">
          <div className="comp-panel-header">📋 Reference Information</div>
          <div className="reference-info">
            <div className="ref-section">
              <h4>Student Record</h4>
              <div className="ref-grid">
                <div className="ref-item">
                  <span className="ref-label">English Name</span>
                  <span className="ref-value">{/*student.englishName*/}</span>
                </div>
                <div className="ref-item">
                  <span className="ref-label">Hindi Name</span>
                  <span className="ref-value">{/*student.hindiName*/}</span>
                </div>
                <div className="ref-item">
                  <span className="ref-label">Roll Number</span>
                  <span className="ref-value mono">{/*student.rollNumber*/}</span>
                </div>
                <div className="ref-item">
                  <span className="ref-label">Degree</span>
                  <span className="ref-value">{/*student.degree*/}</span>
                </div>
                <div className="ref-item">
                  <span className="ref-label">Branch</span>
                  <span className="ref-value">{/*student.branch*/}</span>
                </div>
                <div className="ref-item">
                  <span className="ref-label">Date of Issue</span>
                  <span className="ref-value">{/*student.dateOfIssue*/}</span>
                </div>
                <div className="ref-item">
                  <span className="ref-label">CGPA</span>
                  <span className="ref-value">{/*student.cgpa*/}</span>
                </div>
                <div className="ref-item">
                  <span className="ref-label">Convocation</span>
                  <span className="ref-value">{/*student.convocationNumber*/}</span>
                </div>
              </div>
            </div>
            <div className="ref-section">
              <h4>Verification Summary</h4>
              <div className="ref-summary">
                <span>Status: <StatusBadge status={/*cert.status*/''} /></span>
                <span>Confidence: <strong>{cert.overallConfidence}%</strong></span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Field-level Comparison */}
      <div className="section-card">
        <h3 className="section-title">Field-Level Comparison</h3>
        <div className="fields-list">
          {/*cert.fields.map((field: CertificateField) => (
            <div key={field.name} className={`field-comparison-card ${field.matchStatus}`}>
              <div className="field-comp-header">
                <span className="field-comp-name">{field.name}</span>
                <div className="field-comp-meta">
                  <StatusBadge status={field.matchStatus} size="sm" />
                  <span className="match-type-tag">{field.matchType}</span>
                </div>
              </div>
              <div className="field-comp-values">
                <div className="field-comp-col">
                  <span className="field-comp-label">Expected</span>
                  <span className="field-comp-value expected">{field.expectedValue}</span>
                </div>
                <div className="field-comp-col">
                  <span className="field-comp-label">Extracted</span>
                  <span className={`field-comp-value extracted ${field.matchStatus !== 'match' ? 'flagged' : ''}`}>{field.extractedValue}</span>
                </div>
                <div className="field-comp-col confidence-col">
                  <span className="field-comp-label">Confidence</span>
                  <ConfidenceIndicator value={field.confidence} showBar />
                </div>
              </div>
              {field.reason && (
                <div className="field-comp-reason">
                  <span className="reason-icon">ℹ</span> {field.reason}
                </div>
              )}
            </div>
          ))*/}
        </div>
      </div>

      {/* Layout Verification */}
      {/* <div className="section-card">
        <h3 className="section-title">Layout Verification</h3>
        <p className="section-note">Field positions are compared against the reference certificate template.</p>
        <div className="layout-regions">
          {cert.layoutRegions.map((region: LayoutRegion) => (
            <div key={region.name} className={`layout-region-item ${region.status}`}>
              <span className="region-icon">
                {region.status === 'match' ? '✓' : region.status === 'position_difference' ? '⚠' : '✕'}
              </span>
              <span className="region-name">{region.name}</span>
              <span className={`region-status ${region.status}`}>
                {region.status === 'match' ? 'Match' : region.status === 'position_difference' ? 'Position Difference' : 'Anomaly'}
              </span>
              {region.deviation !== undefined && (
                <span className="region-deviation">{region.deviation}px deviation</span>
              )}
            </div>
          ))}
        </div>
        <p className="section-note" style={{ marginTop: '12px', fontStyle: 'italic' }}>
          Actual layout verification via OpenCV is pending backend implementation.
        </p>
      </div> */}

      {/* Heatmap Placeholder */}
      {/* <div className="heatmap-placeholder">
        <span className="heatmap-icon">🗺️</span>
        <h4>Difference Heatmap</h4>
        <p>Pixel-level difference heatmap requires OpenCV backend integration.</p>
      </div> */}

      {/* Actions */}
      <div className="comparison-actions">
        <button className="btn-primary" onClick={() => navigate('/results')}>View Results</button>
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
