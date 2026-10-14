import { useState, useRef, type DragEvent, type ChangeEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import PageHeader from '../components/common/PageHeader';
import './Upload.css';

const ACCEPTED_TYPES = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg'];
const MAX_SIZE = 20 * 1024 * 1024; // 20 MB

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1048576) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1048576).toFixed(1)} MB`;
}

export default function Upload() {
  const navigate = useNavigate();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [error, setError] = useState<string>('');
  const [isDragOver, setIsDragOver] = useState(false);

  function validateAndSetFile(file: File) {
    setError('');
    if (!ACCEPTED_TYPES.includes(file.type)) {
      setError(`Invalid file type "${file.type}". Accepted: PDF, JPG, PNG.`);
      return;
    }
    if (file.size > MAX_SIZE) {
      setError('File too large. Maximum size: 20 MB.');
      return;
    }
    setSelectedFile(file);
    if (file.type.startsWith('image/')) {
      setPreviewUrl(URL.createObjectURL(file));
    } else {
      setPreviewUrl(null);
    }
  }

  function handleDrop(e: DragEvent<HTMLDivElement>) {
    e.preventDefault();
    setIsDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file) validateAndSetFile(file);
  }

  function handleFileInput(e: ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (file) validateAndSetFile(file);
  }

  function handleRemove() {
    setSelectedFile(null);
    setPreviewUrl(null);
    setError('');
    if (fileInputRef.current) fileInputRef.current.value = '';
  }

  function handleStartVerification() {
    if (selectedFile) navigate('/verification');
  }

  return (
    <div className="upload-container">
      <PageHeader title="Upload Certificate" subtitle="Upload a degree certificate to begin verification" />

      {!selectedFile ? (
        <div
          className={`dropzone ${isDragOver ? 'drag-over' : ''}`}
          onDragOver={(e: DragEvent<HTMLDivElement>) => { e.preventDefault(); setIsDragOver(true); }}
          onDragLeave={() => setIsDragOver(false)}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          <div className="dropzone-icon">📁</div>
          <h3>Drag & drop your certificate here</h3>
          <p>or click to browse files</p>
          <p className="format-note">Accepted formats: PDF, JPG, PNG · Max size: 20 MB</p>
          <button className="browse-btn" type="button" onClick={(e) => { e.stopPropagation(); fileInputRef.current?.click(); }}>
            Browse Files
          </button>
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.jpg,.jpeg,.png"
            onChange={handleFileInput}
            style={{ display: 'none' }}
          />
        </div>
      ) : (
        <div className="upload-preview">
          <div className="preview-image-area">
            {previewUrl ? (
              <img src={previewUrl} alt="Certificate preview" />
            ) : (
              <div className="pdf-placeholder">
                <span className="pdf-icon">📄</span>
                <p>PDF Document</p>
              </div>
            )}
          </div>
          <div className="preview-meta">
            <div className="preview-info">
              <span className="file-name">{selectedFile.name}</span>
              <span className="file-details">{selectedFile.type} · {formatBytes(selectedFile.size)}</span>
            </div>
            <div className="preview-actions">
              <button className="btn-outline" onClick={handleRemove}>Remove</button>
              <button className="btn-primary" onClick={handleStartVerification}>Start Verification</button>
            </div>
          </div>
        </div>
      )}

      {error && <div className="upload-error">{error}</div>}

      <div className="prototype-footer">
        <p>STTCSE . CS-202</p>
      </div>
    </div>
  );
}
