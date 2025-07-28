import React from 'react';
import { useNavigate } from 'react-router-dom';
import { checkHealth } from '../services/api';

const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const [serverStatus, setServerStatus] = React.useState<string>('checking');

  React.useEffect(() => {
    const checkServerHealth = async () => {
      try {
        await checkHealth();
        setServerStatus('connected');
      } catch (error) {
        setServerStatus('disconnected');
      }
    };
    
    checkServerHealth();
  }, []);

  return (
    <div className="home-page">
      <div className="hero-section">
        <h1>Welcome to AI Tax Return Agent</h1>
        <p className="subtitle">
          Automate your tax return preparation with AI-powered document processing
        </p>
        
        <div className="status-indicator">
          <span className={`status ${serverStatus}`}>
            Backend Status: {serverStatus === 'connected' ? '🟢 Connected' : 
                           serverStatus === 'disconnected' ? '🔴 Disconnected' : '🟡 Checking...'}
          </span>
        </div>
      </div>

      <div className="features-section">
        <h2>What We Can Do</h2>
        <div className="features-grid">
          <div className="feature-card">
            <h3>📄 Document Upload</h3>
            <p>Upload your W-2, 1099-INT, and 1099-NEC forms</p>
          </div>
          <div className="feature-card">
            <h3>🤖 AI Processing</h3>
            <p>Intelligent data extraction using rule-based parsing</p>
          </div>
          <div className="feature-card">
            <h3>🧮 Tax Calculation</h3>
            <p>Automatic tax liability calculation for 2024</p>
          </div>
          <div className="feature-card">
            <h3>📋 Form Generation</h3>
            <p>Generate completed Form 1040 ready for filing</p>
          </div>
        </div>
      </div>

      <div className="cta-section">
        <button 
          className="cta-button"
          onClick={() => navigate('/upload')}
          disabled={serverStatus !== 'connected'}
        >
          Start Your Tax Return
        </button>
        <p className="disclaimer">
          This is a prototype for educational purposes only. 
          Not intended for actual tax filing.
        </p>
      </div>
    </div>
  );
};

export default HomePage; 