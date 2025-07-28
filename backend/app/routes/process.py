from flask import Blueprint, request, jsonify, current_app
import os
from app.services.document_processor import DocumentProcessor, ExtractedData
from typing import List, Dict, Any

process_bp = Blueprint('process', __name__)

@process_bp.route('/process', methods=['POST'])
def process_documents():
    """Process all uploaded documents and extract tax data"""
    try:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        processor = DocumentProcessor()
        
        if not os.path.exists(upload_folder):
            return jsonify({'error': 'Upload folder not found'}), 404
        
        # Get all PDF files from upload folder
        pdf_files = []
        for filename in os.listdir(upload_folder):
            if filename.endswith('.pdf'):
                file_path = os.path.join(upload_folder, filename)
                pdf_files.append(file_path)
        
        if not pdf_files:
            return jsonify({'error': 'No PDF files found to process'}), 400
        
        # Process each document
        processed_documents = []
        total_confidence = 0
        
        for file_path in pdf_files:
            try:
                extracted_data = processor.process_document(file_path)
                validation_result = processor.validate_extracted_data(extracted_data)
                
                processed_doc = {
                    'filename': extracted_data.filename,
                    'document_type': extracted_data.document_type.value,
                    'confidence_score': extracted_data.confidence_score,
                    'extracted_data': extracted_data.data,
                    'validation': validation_result,
                    'raw_text_length': len(extracted_data.raw_text)
                }
                
                processed_documents.append(processed_doc)
                total_confidence += extracted_data.confidence_score
                
            except Exception as e:
                current_app.logger.error(f"Error processing {file_path}: {str(e)}")
                processed_documents.append({
                    'filename': os.path.basename(file_path),
                    'document_type': 'UNKNOWN',
                    'confidence_score': 0.0,
                    'extracted_data': {},
                    'validation': {
                        'is_valid': False,
                        'errors': [f'Processing error: {str(e)}'],
                        'warnings': [],
                        'suggestions': []
                    },
                    'raw_text_length': 0
                })
        
        # Calculate overall statistics
        avg_confidence = total_confidence / len(processed_documents) if processed_documents else 0
        valid_documents = [doc for doc in processed_documents if doc['validation']['is_valid']]
        
        # Group by document type
        document_summary = {}
        for doc in processed_documents:
            doc_type = doc['document_type']
            if doc_type not in document_summary:
                document_summary[doc_type] = []
            document_summary[doc_type].append(doc)
        
        return jsonify({
            'message': 'Document processing completed',
            'total_documents': len(processed_documents),
            'valid_documents': len(valid_documents),
            'average_confidence': round(avg_confidence, 3),
            'document_summary': document_summary,
            'processed_documents': processed_documents
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Document processing error: {str(e)}")
        return jsonify({'error': f'Document processing failed: {str(e)}'}), 500

@process_bp.route('/process/<filename>', methods=['POST'])
def process_single_document(filename):
    """Process a single document by filename"""
    try:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        file_path = os.path.join(upload_folder, filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        processor = DocumentProcessor()
        extracted_data = processor.process_document(file_path)
        validation_result = processor.validate_extracted_data(extracted_data)
        
        processed_doc = {
            'filename': extracted_data.filename,
            'document_type': extracted_data.document_type.value,
            'confidence_score': extracted_data.confidence_score,
            'extracted_data': extracted_data.data,
            'validation': validation_result,
            'raw_text_length': len(extracted_data.raw_text)
        }
        
        return jsonify({
            'message': 'Document processed successfully',
            'processed_document': processed_doc
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Single document processing error: {str(e)}")
        return jsonify({'error': f'Document processing failed: {str(e)}'}), 500

@process_bp.route('/process/status', methods=['GET'])
def get_processing_status():
    """Get processing status and statistics"""
    try:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        
        if not os.path.exists(upload_folder):
            return jsonify({'error': 'Upload folder not found'}), 404
        
        # Count PDF files
        pdf_files = [f for f in os.listdir(upload_folder) if f.endswith('.pdf')]
        
        return jsonify({
            'status': 'ready',
            'uploaded_files': len(pdf_files),
            'can_process': len(pdf_files) > 0
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Processing status error: {str(e)}")
        return jsonify({'error': f'Failed to get processing status: {str(e)}'}), 500 