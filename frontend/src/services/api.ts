import axios from 'axios';
import { 
  ApiResponse, 
  UploadResponse, 
  UploadStatusResponse,
  TaxData, 
  Form1040Data 
} from '../types';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: 'http://localhost:5000',
  timeout: 30000, // 30 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Health check
export const checkHealth = async (): Promise<ApiResponse> => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    throw new Error('Backend server is not responding');
  }
};

// File upload
export const uploadFiles = async (files: File[]): Promise<UploadResponse> => {
  try {
    const formData = new FormData();
    files.forEach(file => {
      formData.append('files', file);
    });

    const response = await api.post('/api/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error: any) {
    throw new Error(error.response?.data?.error || 'Upload failed');
  }
};

// Get upload status
export const getUploadStatus = async (): Promise<UploadStatusResponse> => {
  try {
    const response = await api.get('/api/upload-status');
    return response.data;
  } catch (error: any) {
    throw new Error(error.response?.data?.error || 'Failed to get upload status');
  }
};

// Clear all uploads
export const clearUploads = async (): Promise<ApiResponse> => {
  try {
    const response = await api.delete('/api/upload/clear');
    return response.data;
  } catch (error: any) {
    throw new Error(error.response?.data?.error || 'Failed to clear uploads');
  }
};

// Process documents
export const processDocuments = async (): Promise<ApiResponse> => {
  try {
    const response = await api.post('/api/process');
    return response.data;
  } catch (error: any) {
    throw new Error(error.response?.data?.error || 'Document processing failed');
  }
};

// Calculate tax
export const calculateTax = async (taxData: Partial<TaxData>): Promise<ApiResponse<TaxData>> => {
  try {
    const response = await api.post('/api/calculate', taxData);
    return response.data;
  } catch (error: any) {
    throw new Error(error.response?.data?.error || 'Tax calculation failed');
  }
};

// Generate Form 1040
export const generateForm1040 = async (formData: Form1040Data): Promise<Blob> => {
  try {
    const response = await api.post('/api/generate-precision-form-1040', formData, {
      responseType: 'blob',
    });
    return response.data;
  } catch (error: any) {
    throw new Error(error.response?.data?.error || 'Form generation failed');
  }
};

// Generate watermarked Form 1040
export const generateWatermarkedForm1040 = async (formData: Form1040Data): Promise<Blob> => {
  try {
    const response = await api.post('/api/generate-watermarked-form-1040', formData, {
      responseType: 'blob',
    });
    return response.data;
  } catch (error: any) {
    throw new Error(error.response?.data?.error || 'Watermarked form generation failed');
  }
};

// Generate robust Form 1040 (PyMuPDF approach)
export const generateRobustForm1040 = async (formData: Form1040Data): Promise<Blob> => {
  try {
    const response = await api.post('/api/generate-robust-form-1040', formData, {
      responseType: 'blob',
    });
    return response.data;
  } catch (error: any) {
    throw new Error(error.response?.data?.error || 'Robust form generation failed');
  }
};

export default api; 