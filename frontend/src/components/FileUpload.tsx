import React, { useState, useRef, useCallback } from 'react';
import { UploadedFile } from '../types';

interface FileUploadProps {
  onFilesSelected: (files: File[]) => void;
  onUpload: (files: File[]) => Promise<void>;
  onClearUploads?: () => Promise<void>;
  uploadedFiles: UploadedFile[];
  uploading: boolean;
  error: string;
}

const FileUpload: React.FC<FileUploadProps> = ({
  onFilesSelected,
  onUpload,
  onClearUploads,
  uploadedFiles,
  uploading,
  error
}) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateFiles = (files: File[]): { valid: File[], invalid: string[] } => {
    const valid: File[] = [];
    const invalid: string[] = [];

    files.forEach(file => {
      // Check file type
      if (!file.type.includes('pdf')) {
        invalid.push(`${file.name} - Only PDF files are allowed`);
        return;
      }

      // Check file size (16MB limit)
      if (file.size > 16 * 1024 * 1024) {
        invalid.push(`${file.name} - File size must be less than 16MB`);
        return;
      }

      // Check for duplicate files
      const isDuplicate = valid.some(f => f.name === file.name);
      if (isDuplicate) {
        invalid.push(`${file.name} - Duplicate file`);
        return;
      }

      valid.push(file);
    });

    return { valid, invalid };
  };

  const handleFileSelect = useCallback((files: FileList | null) => {
    if (!files) return;

    const fileArray = Array.from(files);
    console.log(`Selected ${fileArray.length} files:`, fileArray.map(f => f.name));
    
    const { valid, invalid } = validateFiles(fileArray);

    if (invalid.length > 0) {
      alert('Invalid files:\n' + invalid.join('\n'));
      return;
    }

    setSelectedFiles(valid);
    onFilesSelected(valid);
  }, [onFilesSelected]);

  const handleDrop = useCallback((event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragOver(false);
    
    const files = event.dataTransfer.files;
    handleFileSelect(files);
  }, [handleFileSelect]);

  const handleDragOver = useCallback((event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleFileInputChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    handleFileSelect(event.target.files);
  }, [handleFileSelect]);

  const removeFile = useCallback((index: number) => {
    const newFiles = selectedFiles.filter((_, i) => i !== index);
    setSelectedFiles(newFiles);
    onFilesSelected(newFiles);
  }, [selectedFiles, onFilesSelected]);

  const handleUploadClick = useCallback(async () => {
    if (selectedFiles.length === 0) return;
    await onUpload(selectedFiles);
  }, [selectedFiles, onUpload]);

  return (
    <div className="file-upload">
      <div className="upload-instructions">
        <h3>📄 Upload Your Tax Documents</h3>
        <p><strong>Upload ALL your tax forms:</strong> W-2, 1099-INT, 1099-NEC, etc.</p>
        <p>You can select multiple files at once or upload them one by one</p>
        <p>Supported formats: PDF only | Maximum file size: 16MB per file</p>
      </div>

      <div
        className={`drop-zone ${isDragOver ? 'drag-over' : ''}`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onClick={() => fileInputRef.current?.click()}
      >
        <div className="drop-zone-content">
          {isDragOver ? (
            <div className="drag-over-message">
              <p>📁 Drop files here</p>
            </div>
          ) : (
            <div className="upload-message">
              <div className="upload-icon">📄</div>
              <p>Drag and drop your tax documents here</p>
              <p>or click to browse and select multiple files</p>
              <button 
                type="button" 
                className="browse-button"
                onClick={(e) => {
                  e.stopPropagation();
                  fileInputRef.current?.click();
                }}
              >
                Choose Files
              </button>
            </div>
          )}
        </div>
      </div>

      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept=".pdf"
        onChange={handleFileInputChange}
        className="hidden-file-input"
      />

      {selectedFiles.length > 0 && (
        <div className="selected-files">
          <h4>Selected Files ({selectedFiles.length})</h4>
          <div className="file-list">
            {selectedFiles.map((file, index) => (
              <div key={index} className="file-item">
                <div className="file-info">
                  <span className="file-icon">📄</span>
                  <div className="file-details">
                    <span className="file-name">{file.name}</span>
                    <span className="file-size">
                      {(file.size / 1024 / 1024).toFixed(2)} MB
                    </span>
                  </div>
                </div>
                <button
                  type="button"
                  className="remove-file"
                  onClick={() => removeFile(index)}
                  disabled={uploading}
                >
                  ✕
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {uploadedFiles.length > 0 && (
        <div className="uploaded-files">
          <div className="uploaded-files-header">
            <h4>Successfully Uploaded ({uploadedFiles.length})</h4>
            {onClearUploads && (
              <button
                type="button"
                className="clear-uploads-button"
                onClick={onClearUploads}
                disabled={uploading}
              >
                🗑️ Clear All Uploads
              </button>
            )}
          </div>
          <div className="file-list">
            {uploadedFiles.map((file, index) => (
              <div key={index} className="file-item uploaded">
                <div className="file-info">
                  <span className="file-icon">✅</span>
                  <div className="file-details">
                    <span className="file-name">{file.original_name}</span>
                    <span className="file-size">
                      {(file.size / 1024 / 1024).toFixed(2)} MB
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}



      {error && (
        <div className="error-message">
          <span className="error-icon">❌</span>
          <span>{error}</span>
        </div>
      )}

      <div className="upload-actions">
        <button
          type="button"
          className="upload-button"
          onClick={handleUploadClick}
          disabled={uploading || selectedFiles.length === 0}
        >
          {uploading ? (
            <>
              <span className="spinner"></span>
              Uploading...
            </>
          ) : (
            'Upload Files'
          )}
        </button>
      </div>
    </div>
  );
};

export default FileUpload; 