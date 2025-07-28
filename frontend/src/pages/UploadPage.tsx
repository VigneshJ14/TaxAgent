import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { uploadFiles, clearUploads, getUploadStatus } from '../services/api';
import { UploadedFile, UploadStatusResponse } from '../types';
import FileUpload from '../components/FileUpload';
import PersonalInfoForm, { PersonalInfo } from '../components/PersonalInfoForm';

type UploadStep = 'files' | 'personal-info' | 'review';

const UploadPage: React.FC = () => {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState<UploadStep>('files');
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [personalInfo, setPersonalInfo] = useState<PersonalInfo | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string>('');

  // Load existing uploaded files on component mount
  useEffect(() => {
    const loadExistingUploads = async () => {
      try {
        const response: UploadStatusResponse = await getUploadStatus();
        if (response.uploaded_files && response.uploaded_files.length > 0) {
          // Convert backend format to frontend format
          const convertedFiles: UploadedFile[] = response.uploaded_files.map((file) => ({
            original_name: file.filename,
            saved_name: file.filename,
            file_path: `/uploads/${file.filename}`,
            size: file.size
          }));
          setUploadedFiles(convertedFiles);
        }
      } catch (error) {
        console.log('No existing uploads or error loading uploads:', error);
      }
    };

    loadExistingUploads();
  }, []);

  const handleFilesSelected = (files: File[]) => {
    setSelectedFiles(files);
    setError('');
  };

  const handleFileUpload = async (files: File[]) => {
    setUploading(true);
    setError('');

    try {
      const response = await uploadFiles(files);
      setUploadedFiles(response.files);
      setCurrentStep('personal-info');
    } catch (error: any) {
      setError(error.message);
    } finally {
      setUploading(false);
    }
  };

  const handleClearUploads = async () => {
    setUploading(true);
    setError('');

    try {
      await clearUploads();
      setUploadedFiles([]);
      setSelectedFiles([]);
      setCurrentStep('files');
    } catch (error: any) {
      setError(error.message);
    } finally {
      setUploading(false);
    }
  };



  const handlePersonalInfoSubmit = (info: PersonalInfo) => {
    setPersonalInfo(info);
    setCurrentStep('review');
  };

  const handleContinueToProcessing = () => {
    // Store data in session storage for processing page
    sessionStorage.setItem('uploadedFiles', JSON.stringify(uploadedFiles));
    sessionStorage.setItem('personalInfo', JSON.stringify(personalInfo));
    navigate('/processing');
  };

  const handleBackToFiles = () => {
    setCurrentStep('files');
    setPersonalInfo(null);
  };

  const handleBackToPersonalInfo = () => {
    setCurrentStep('personal-info');
  };

  const getStepIndicator = () => {
    const steps = [
      { key: 'files', label: 'Upload Files', icon: '📄' },
      { key: 'personal-info', label: 'Personal Info', icon: '👤' },
      { key: 'review', label: 'Review', icon: '✅' }
    ];

    return (
      <div className="step-indicator">
        {steps.map((step, index) => (
          <div key={step.key} className={`step ${currentStep === step.key ? 'active' : ''}`}>
            <div className="step-icon">{step.icon}</div>
            <span className="step-label">{step.label}</span>
            {index < steps.length - 1 && <div className="step-connector"></div>}
          </div>
        ))}
      </div>
    );
  };

  const renderCurrentStep = () => {
    switch (currentStep) {
      case 'files':
        return (
          <div className="step-content">
            <FileUpload
              onFilesSelected={handleFilesSelected}
              onUpload={handleFileUpload}
              onClearUploads={handleClearUploads}
              uploadedFiles={uploadedFiles}
              uploading={uploading}
              error={error}
            />
            <div className="step-actions">
              <button
                className="back-button"
                onClick={() => navigate('/')}
                disabled={uploading}
              >
                Back to Home
              </button>
            </div>
          </div>
        );

      case 'personal-info':
        return (
          <div className="step-content">
            <PersonalInfoForm
              onInfoSubmit={handlePersonalInfoSubmit}
              onSubmit={() => {}} // Handled in onInfoSubmit
              disabled={false}
            />
            <div className="step-actions">
              <button
                className="back-button"
                onClick={handleBackToFiles}
              >
                Back to Files
              </button>
            </div>
          </div>
        );

      case 'review':
        return (
          <div className="step-content">
            <div className="review-section">
              <h3>📋 Review Your Information</h3>
              
              <div className="review-card">
                <h4>📄 Uploaded Files ({uploadedFiles.length})</h4>
                <ul>
                  {uploadedFiles.map((file, index) => (
                    <li key={index}>
                      {file.original_name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
                    </li>
                  ))}
                </ul>
              </div>

              {personalInfo && (
                <div className="review-card">
                  <h4>👤 Personal Information</h4>
                  <div className="info-grid">
                    <div className="info-item">
                      <span className="label">Name:</span>
                      <span className="value">{personalInfo.name}</span>
                    </div>
                    <div className="info-item">
                      <span className="label">Filing Status:</span>
                      <span className="value">{personalInfo.filing_status}</span>
                    </div>
                    <div className="info-item">
                      <span className="label">Dependents:</span>
                      <span className="value">{personalInfo.dependents}</span>
                    </div>
                    <div className="info-item">
                      <span className="label">Address:</span>
                      <span className="value">
                        {personalInfo.address}, {personalInfo.city}, {personalInfo.state} {personalInfo.zip}
                      </span>
                    </div>
                  </div>
                </div>
              )}

              <div className="review-actions">
                <button
                  className="continue-button"
                  onClick={handleContinueToProcessing}
                >
                  Start Processing Documents
                </button>
                <button
                  className="back-button"
                  onClick={handleBackToPersonalInfo}
                >
                  Edit Personal Info
                </button>
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="upload-page">
      <div className="upload-container">
        <h2>Tax Document Upload</h2>
        <p>Upload ALL your tax forms (W-2, 1099-INT, 1099-NEC, etc.) to get a complete tax return</p>
        {uploadedFiles.length > 0 && (
          <div style={{ 
            background: '#f0fff4', 
            border: '1px solid #48bb78', 
            borderRadius: '8px', 
            padding: '12px', 
            marginBottom: '20px',
            textAlign: 'center'
          }}>
            <span style={{ color: '#2f855a', fontWeight: '600' }}>
              📄 Currently uploaded: {uploadedFiles.length} document{uploadedFiles.length !== 1 ? 's' : ''}
            </span>
          </div>
        )}
        
        {getStepIndicator()}
        
        {renderCurrentStep()}
      </div>
    </div>
  );
};

export default UploadPage; 