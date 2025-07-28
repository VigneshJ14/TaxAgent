import React from 'react';
import { useNavigate } from 'react-router-dom';
import { processDocuments, calculateTax } from '../services/api';

const ProcessingPage: React.FC = () => {
  const navigate = useNavigate();
  const [processingStage, setProcessingStage] = React.useState<string>('starting');
  const [progress, setProgress] = React.useState<number>(0);
  const [message, setMessage] = React.useState<string>('Initializing...');
  const [error, setError] = React.useState<string>('');

  React.useEffect(() => {
    const processDocumentsAsync = async () => {
      try {
        // Get data from session storage
        const personalInfoStr = sessionStorage.getItem('personalInfo');
        if (!personalInfoStr) {
          throw new Error('Personal information not found');
        }
        
        const personalInfo = JSON.parse(personalInfoStr);
        
        // Stage 1: Process documents
        setProcessingStage('processing');
        setMessage('Extracting data from documents...');
        setProgress(30);
        
        const processResult = await processDocuments();
        console.log('Document processing result:', processResult);
        
        // Stage 2: Calculate tax
        setProcessingStage('calculating');
        setMessage('Calculating tax liability...');
        setProgress(60);
        
        const taxResult = await calculateTax({
          filing_status: personalInfo.filing_status,
          dependents: personalInfo.dependents,
          age: personalInfo.age || 30
        });
        console.log('Tax calculation result:', taxResult);
        
        // Stage 3: Complete
        setProcessingStage('complete');
        setMessage('Processing complete!');
        setProgress(100);
        
        // Store results in session storage for ResultsPage
        sessionStorage.setItem('taxResults', JSON.stringify(taxResult));
        
        // Navigate to results after processing
        setTimeout(() => {
          navigate('/results');
        }, 1000);

      } catch (error: any) {
        console.error('Processing error:', error);
        setError(error.message);
        setProcessingStage('error');
      }
    };

    processDocumentsAsync();
  }, [navigate]);

  return (
    <div className="processing-page">
      <div className="processing-container">
        <h2>Processing Your Documents</h2>
        
        <div className="progress-container">
          <div className="progress-bar">
            <div 
              className="progress-fill"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <p className="progress-text">{progress}% Complete</p>
        </div>

        <div className="stage-indicator">
          <h3>Current Stage: {processingStage}</h3>
          <p className="stage-message">{message}</p>
        </div>

        {error && (
          <div className="error-message">
            ❌ Error: {error}
            <button 
              className="retry-button"
              onClick={() => window.location.reload()}
            >
              Retry
            </button>
          </div>
        )}

        <div className="processing-info">
          <h4>What's happening:</h4>
          <ul>
            <li>📄 Analyzing uploaded PDF documents</li>
            <li>🤖 Extracting tax data using rule-based parsing</li>
            <li>🧮 Calculating tax liability for 2024</li>
            <li>📋 Generating completed Form 1040</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ProcessingPage; 