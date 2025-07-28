import React, { useState } from 'react';

export interface PersonalInfo {
  filing_status: 'single' | 'married' | 'head_of_household';
  dependents: number;
  name: string;
  ssn: string;
  address: string;
  city: string;
  state: string;
  zip: string;
}

interface PersonalInfoFormProps {
  onInfoSubmit: (info: PersonalInfo) => void;
  onSubmit: () => void;
  disabled?: boolean;
}

const PersonalInfoForm: React.FC<PersonalInfoFormProps> = ({
  onInfoSubmit,
  onSubmit,
  disabled = false
}) => {
  const [formData, setFormData] = useState<PersonalInfo>({
    filing_status: 'single',
    dependents: 0,
    name: '',
    ssn: '',
    address: '',
    city: '',
    state: '',
    zip: ''
  });

  const [errors, setErrors] = useState<Partial<PersonalInfo>>({});

  const validateForm = (): boolean => {
    const newErrors: Partial<PersonalInfo> = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    }

    if (!formData.ssn.trim()) {
      newErrors.ssn = 'SSN is required';
    } else if (!/^\d{3}-?\d{2}-?\d{4}$/.test(formData.ssn.replace(/-/g, ''))) {
      newErrors.ssn = 'Please enter a valid SSN (XXX-XX-XXXX)';
    }

    if (!formData.address.trim()) {
      newErrors.address = 'Address is required';
    }

    if (!formData.city.trim()) {
      newErrors.city = 'City is required';
    }

    if (!formData.state.trim()) {
      newErrors.state = 'State is required';
    }

    if (!formData.zip.trim()) {
      newErrors.zip = 'ZIP code is required';
    } else if (!/^\d{5}(-\d{4})?$/.test(formData.zip)) {
      newErrors.zip = 'Please enter a valid ZIP code';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleInputChange = (field: keyof PersonalInfo, value: string | number) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));

    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({
        ...prev,
        [field]: undefined
      }));
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (validateForm()) {
      onInfoSubmit(formData);
      onSubmit();
    }
  };

  const formatSSN = (value: string): string => {
    const cleaned = value.replace(/\D/g, '');
    if (cleaned.length <= 3) return cleaned;
    if (cleaned.length <= 5) return `${cleaned.slice(0, 3)}-${cleaned.slice(3)}`;
    return `${cleaned.slice(0, 3)}-${cleaned.slice(3, 5)}-${cleaned.slice(5, 9)}`;
  };

  const handleSSNChange = (value: string) => {
    const formatted = formatSSN(value);
    handleInputChange('ssn', formatted);
  };

  return (
    <div className="personal-info-form">
      <div className="form-header">
        <h3>👤 Personal Information</h3>
        <p>Please provide your personal details for tax filing</p>
      </div>

      <form onSubmit={handleSubmit} className="form">
        <div className="form-section">
          <h4>Filing Information</h4>
          
          <div className="form-group">
            <label htmlFor="filing_status">Filing Status *</label>
            <select
              id="filing_status"
              value={formData.filing_status}
              onChange={(e) => handleInputChange('filing_status', e.target.value as any)}
              disabled={disabled}
              className={errors.filing_status ? 'error' : ''}
            >
              <option value="single">Single</option>
              <option value="married">Married Filing Jointly</option>
              <option value="head_of_household">Head of Household</option>
            </select>
            {errors.filing_status && <span className="error-text">{errors.filing_status}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="dependents">Number of Dependents</label>
            <input
              type="number"
              id="dependents"
              min="0"
              max="10"
              value={formData.dependents}
              onChange={(e) => handleInputChange('dependents', parseInt(e.target.value) || 0)}
              disabled={disabled}
              className={errors.dependents ? 'error' : ''}
            />
            {errors.dependents && <span className="error-text">{errors.dependents}</span>}
          </div>
        </div>

        <div className="form-section">
          <h4>Personal Details</h4>
          
          <div className="form-group">
            <label htmlFor="name">Full Name *</label>
            <input
              type="text"
              id="name"
              value={formData.name}
              onChange={(e) => handleInputChange('name', e.target.value)}
              disabled={disabled}
              className={errors.name ? 'error' : ''}
              placeholder="Enter your full name"
            />
            {errors.name && <span className="error-text">{errors.name}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="ssn">Social Security Number *</label>
            <input
              type="text"
              id="ssn"
              value={formData.ssn}
              onChange={(e) => handleSSNChange(e.target.value)}
              disabled={disabled}
              className={errors.ssn ? 'error' : ''}
              placeholder="XXX-XX-XXXX"
              maxLength={11}
            />
            {errors.ssn && <span className="error-text">{errors.ssn}</span>}
          </div>
        </div>

        <div className="form-section">
          <h4>Address Information</h4>
          
          <div className="form-group">
            <label htmlFor="address">Street Address *</label>
            <input
              type="text"
              id="address"
              value={formData.address}
              onChange={(e) => handleInputChange('address', e.target.value)}
              disabled={disabled}
              className={errors.address ? 'error' : ''}
              placeholder="Enter your street address"
            />
            {errors.address && <span className="error-text">{errors.address}</span>}
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="city">City *</label>
              <input
                type="text"
                id="city"
                value={formData.city}
                onChange={(e) => handleInputChange('city', e.target.value)}
                disabled={disabled}
                className={errors.city ? 'error' : ''}
                placeholder="City"
              />
              {errors.city && <span className="error-text">{errors.city}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="state">State *</label>
              <input
                type="text"
                id="state"
                value={formData.state}
                onChange={(e) => handleInputChange('state', e.target.value)}
                disabled={disabled}
                className={errors.state ? 'error' : ''}
                placeholder="State"
                maxLength={2}
              />
              {errors.state && <span className="error-text">{errors.state}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="zip">ZIP Code *</label>
              <input
                type="text"
                id="zip"
                value={formData.zip}
                onChange={(e) => handleInputChange('zip', e.target.value)}
                disabled={disabled}
                className={errors.zip ? 'error' : ''}
                placeholder="ZIP"
                maxLength={10}
              />
              {errors.zip && <span className="error-text">{errors.zip}</span>}
            </div>
          </div>
        </div>

        <div className="form-actions">
          <button
            type="submit"
            className="submit-button"
            disabled={disabled}
          >
            Continue to Processing
          </button>
        </div>
      </form>
    </div>
  );
};

export default PersonalInfoForm; 