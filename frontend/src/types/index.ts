// API Response Types
export interface ApiResponse<T = any> {
  message: string;
  status?: string;
  data?: T;
  error?: string;
}

// File Upload Types
export interface UploadedFile {
  original_name: string;
  saved_name: string;
  file_path: string;
  size: number;
}

export interface UploadResponse {
  message: string;
  files: UploadedFile[];
  count: number;
}

export interface UploadStatusResponse {
  uploaded_files: {
    filename: string;
    size: number;
    uploaded_at: number;
    modified_at: number;
  }[];
  count: number;
  upload_folder: string;
}

// Document Processing Types
export interface TaxDocument {
  id: string;
  type: 'W-2' | '1099-INT' | '1099-NEC';
  filename: string;
  extracted_data: any;
  confidence_score: number;
  processed: boolean;
}

// Tax Calculation Types
export interface TaxData {
  filing_status: 'single' | 'married' | 'head_of_household';
  dependents: number;
  age?: number;
  total_wages: number;
  total_interest: number;
  total_nonemployee_compensation: number;
  federal_income_tax_withheld: number;
  standard_deduction: number;
  taxable_income: number;
  tax_liability: number;
  refund_or_amount_owed: number;
}

// Form 1040 Types
export interface Form1040Data {
  personal_info: {
    first_name: string;
    last_name: string;
    ssn: string;
    address: string;
    city: string;
    state: string;
    zip: string;
    filing_status: string;
    dependents: number;
    age?: number;
  };
  tax_data: {
    total_income: number;
    adjusted_gross_income: number;
    taxable_income: number;
    federal_tax: number;
    total_tax_withheld: number;
    refund_or_amount_owed: number;
    standard_deduction: number;
  };
  income_summary: {
    wages: number;
    interest_income: number;
    nonemployee_compensation: number;
    total_income: number;
  };
}

// User Interface Types
export interface UploadProgress {
  file: File;
  progress: number;
  status: 'uploading' | 'completed' | 'error';
  error?: string;
}

export interface ProcessingStatus {
  stage: 'uploading' | 'processing' | 'calculating' | 'generating' | 'complete';
  progress: number;
  message: string;
} 