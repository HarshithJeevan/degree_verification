import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import PageHeader from '../components/common/PageHeader';
import { mockPipelineIssues } from '../data/mockVerification';
import type { VerificationStep } from '../types';
import './Verification.css';

function stepIcon(status: VerificationStep['status']): string {
  switch (status) {
    case 'completed': return '✓';
    case 'warning': return '⚠';
    case 'processing': return '⟳';
    case 'error': return '✕';
    default: return '○';
  }
}

function stepClass(status: VerificationStep['status']): string {
  switch (status) {
    case 'completed': return 'step-completed';
    case 'warning': return 'step-warning';
    case 'processing': return 'step-processing';
    case 'error': return 'step-error';
    default: return 'step-pending';
  }
}

export default function Verification() {
  const navigate = useNavigate();
  const [visibleSteps, setVisibleSteps] = useState(0);
  const pipeline = mockPipelineIssues;

  /*useEffect(() => {
    if (visibleSteps < pipeline.steps.length) {
      const timer = setTimeout(() => setVisibleSteps((v) => v + 1), 250);
      return () => clearTimeout(timer);
    }
  }, [visibleSteps, pipeline.steps.length]);*/

  return (
    <div className="verification-container">
      <PageHeader title="Verification Pipeline" subtitle="Tracking each stage of the certificate verification process" />

      <div className="pipeline-card">
        <div className="pipeline-steps">
          {/*pipeline.steps.map((step: VerificationStep, index: number) => (
            <div
              key={step.id}
              className={`pipeline-step ${stepClass(step.status)} ${index < visibleSteps ? 'visible' : ''}`}
            >
              {index > 0 && <div className="step-connector" />}
              <div className={`step-icon-circle ${stepClass(step.status)}`}>
                <span>{stepIcon(step.status)}</span>
              </div>
              <div className="step-body">
                <div className="step-title">{step.name}</div>
                <div className="step-desc">{step.description}</div>
                {step.detail && <div className="step-detail">{step.detail}</div>}
              </div>
            </div>
          ))*/}
        </div>
      </div>

      {/*visibleSteps >= pipeline.steps.length && (
        <div className="verification-actions">
          <button className="btn-primary" onClick={() => navigate('/results')}>View Detailed Results</button>
          <button className="btn-outline" onClick={() => navigate('/comparison')}>View Comparison</button>
        </div>
      )*/}

      <div className="prototype-footer">
        <p>STTCSE . CS-202</p>
      </div>
    </div>
  );
}
