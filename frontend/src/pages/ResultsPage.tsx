import React from 'react';
import { useNavigate } from 'react-router-dom';
import { generateForm1040 } from '../services/api';

const ResultsPage: React.FC = () => {
  const navigate = useNavigate();
  const [downloading, setDownloading] = React.useState(false);
  const [taxResults, setTaxResults] = React.useState<any>(null);
  const [error, setError] = React.useState<string>('');

  React.useEffect(() => {
    // Get tax results from session storage
    const taxResultsStr = sessionStorage.getItem('taxResults');
    if (taxResultsStr) {
      try {
        const results = JSON.parse(taxResultsStr);
        setTaxResults(results);
      } catch (err) {
        setError('Failed to load tax results');
      }
    } else {
      setError('No tax results found. Please start over.');
    }
  }, []);

  const handleDownloadForm = async () => {
    if (!taxResults) return;
    
    setDownloading(true);
    try {
      // Get personal info from session storage (user input)
      const personalInfoStr = sessionStorage.getItem('personalInfo');
      let userPersonalInfo = {
        first_name: '',
        last_name: '',
        ssn: '',
        address: '',
        city: '',
        state: '',
        zip: '',
        filing_status: 'single',
        dependents: 0,
        age: 30
      };
      
      if (personalInfoStr) {
        try {
          const parsedInfo = JSON.parse(personalInfoStr);
          // Parse the full name into first and last name
          const fullName = parsedInfo.name || '';
          const nameParts = fullName.trim().split(' ');
          userPersonalInfo = {
            first_name: nameParts[0] || '',
            last_name: nameParts.slice(1).join(' ') || '',
            ssn: parsedInfo.ssn || '',
            address: parsedInfo.address || '',
            city: parsedInfo.city || '',
            state: parsedInfo.state || '',
            zip: parsedInfo.zip || '',
            filing_status: parsedInfo.filing_status || 'single',
            dependents: parsedInfo.dependents || 0,
            age: 30 // Default age since not collected in form
          };
        } catch (err) {
          console.warn('Failed to parse personal info from session storage');
        }
      }
      
      // Validate that we have the required personal info
      if (!userPersonalInfo.first_name || !userPersonalInfo.last_name || !userPersonalInfo.ssn) {
        alert('Missing required personal information. Please go back and fill in your name and SSN.');
        setDownloading(false);
        return;
      }
      
      // Check for conflicts between personal info and uploaded documents
      const conflicts = [];
      if (taxResults.extracted_data) {
        for (const doc of taxResults.extracted_data) {
          if (doc.document_type === 'W-2' && doc.data.employee_name) {
            const docName = doc.data.employee_name.trim();
            const userFullName = `${userPersonalInfo.first_name} ${userPersonalInfo.last_name}`.trim();
            if (docName && userFullName && docName !== userFullName) {
              conflicts.push(`Name mismatch: Document shows "${docName}" but personal info shows "${userFullName}"`);
            }
          }
          if (doc.data.employee_ssn && doc.data.employee_ssn !== userPersonalInfo.ssn) {
            conflicts.push(`SSN mismatch: Document shows "${doc.data.employee_ssn}" but personal info shows "${userPersonalInfo.ssn}"`);
          }
        }
      }
      
      // Show warning if conflicts exist, but continue with personal info
      if (conflicts.length > 0) {
        const warningMessage = `⚠️ WARNING: Conflicts detected between uploaded documents and personal information:\n\n${conflicts.join('\n')}\n\nUsing personal information provided.`;
        // eslint-disable-next-line no-restricted-globals
        if (!window.confirm(warningMessage + '\n\nContinue with personal information?')) {
          setDownloading(false);
          return;
        }
      }
      
      // Use real form data from API results with user's personal info
      const formData = {
        filing_status: userPersonalInfo.filing_status,
        dependents: userPersonalInfo.dependents,
        personal_info: {
          first_name: userPersonalInfo.first_name,
          last_name: userPersonalInfo.last_name,
          ssn: userPersonalInfo.ssn,
          address: userPersonalInfo.address,
          city: userPersonalInfo.city,
          state: userPersonalInfo.state,
          zip: userPersonalInfo.zip,
          filing_status: userPersonalInfo.filing_status,
          dependents: userPersonalInfo.dependents,
          age: userPersonalInfo.age
        },
        tax_data: {
          total_income: taxResults.income_summary?.total_income || 0,
          adjusted_gross_income: taxResults.tax_calculation?.adjusted_gross_income || 0,
          taxable_income: taxResults.tax_calculation?.taxable_income || 0,
          federal_tax: taxResults.tax_calculation?.tax_liability || 0,
          total_tax_withheld: taxResults.income_summary?.federal_income_tax_withheld || 0,
          refund_or_amount_owed: taxResults.tax_calculation?.refund_or_amount_owed || 0,
          standard_deduction: taxResults.tax_calculation?.standard_deduction || 14600
        },
        income_summary: {
          wages: taxResults.income_summary?.wages || 0,
          interest_income: taxResults.income_summary?.interest_income || 0,
          nonemployee_compensation: taxResults.income_summary?.nonemployee_compensation || 0,
          total_income: taxResults.income_summary?.total_income || 0
        }
      };

      const blob = await generateForm1040(formData);
      
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'Form1040_2024.pdf';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error: any) {
      alert('Error downloading form: ' + error.message);
    } finally {
      setDownloading(false);
    }
  };

  if (error) {
    return (
      <div className="results-page">
        <div className="results-container">
          <div className="error-message">
            ❌ {error}
            <button 
              className="retry-button"
              onClick={() => navigate('/upload')}
            >
              Start Over
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!taxResults) {
    return (
      <div className="results-page">
        <div className="results-container">
          <div className="loading">Loading tax results...</div>
        </div>
      </div>
    );
  }

  // Extract data from API response
  const incomeSummary = taxResults.income_summary || {};
  const taxCalculation = taxResults.tax_calculation || {};
  const personalInfo = taxResults.personal_info || {};

  return (
    <div className="results-page">
      <div className="results-container">
        <h2>Your Tax Return Results</h2>
        
        <div className="summary-card">
          <h3>Tax Summary</h3>
          <div className="summary-grid">
            <div className="summary-item">
              <span className="label">Filing Status:</span>
              <span className="value">{personalInfo.filing_status}</span>
            </div>
            <div className="summary-item">
              <span className="label">Total Wages:</span>
              <span className="value">${incomeSummary.wages?.toLocaleString() || '0'}</span>
            </div>
            <div className="summary-item">
              <span className="label">Interest Income:</span>
              <span className="value">${incomeSummary.interest_income?.toLocaleString() || '0'}</span>
            </div>
            <div className="summary-item">
              <span className="label">Nonemployee Compensation:</span>
              <span className="value">${incomeSummary.nonemployee_compensation?.toLocaleString() || '0'}</span>
            </div>
            <div className="summary-item">
              <span className="label">Standard Deduction:</span>
              <span className="value">${taxCalculation.standard_deduction?.toLocaleString() || '0'}</span>
            </div>
            <div className="summary-item">
              <span className="label">Taxable Income:</span>
              <span className="value">${taxCalculation.taxable_income?.toLocaleString() || '0'}</span>
            </div>
            <div className="summary-item">
              <span className="label">Tax Liability:</span>
              <span className="value">${taxCalculation.tax_liability?.toLocaleString() || '0'}</span>
            </div>
            <div className="summary-item">
              <span className="label">Federal Tax Withheld:</span>
              <span className="value">${incomeSummary.federal_income_tax_withheld?.toLocaleString() || '0'}</span>
            </div>
            <div className="summary-item highlight">
              <span className="label">Refund/Amount Owed:</span>
              <span className={`value ${taxCalculation.refund_or_amount_owed > 0 ? 'refund' : 'owed'}`}>
                {taxCalculation.refund_or_amount_owed > 0 ? 'Refund: $' : 'Owed: $'}
                {Math.abs(taxCalculation.refund_or_amount_owed || 0).toLocaleString()}
              </span>
            </div>
          </div>
        </div>

        <div className="actions-section">
          <button 
            className="download-button"
            onClick={handleDownloadForm}
            disabled={downloading}
          >
            {downloading ? 'Generating PDF...' : '📄 Download Form 1040'}
          </button>
          
          <button 
            className="new-return-button"
            onClick={() => navigate('/upload')}
          >
            Start New Tax Return
          </button>
          
          <button 
            className="home-button"
            onClick={() => navigate('/')}
          >
            Back to Home
          </button>
        </div>

        <div className="disclaimer">
          <h4>Important Disclaimer</h4>
          <p>
            This is a prototype for educational purposes only. The calculations and generated forms 
            are not intended for actual tax filing. Please consult with a qualified tax professional 
            or use official IRS software for your actual tax return.
          </p>
        </div>
      </div>
    </div>
  );
};

export default ResultsPage; 