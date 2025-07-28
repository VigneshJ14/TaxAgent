from flask import Blueprint, request, jsonify, current_app
import os
from werkzeug.utils import secure_filename
import uuid
import mimetypes
import hashlib
import tempfile
import shutil
from datetime import datetime, timedelta

upload_bp = Blueprint('upload', __name__)

ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
SESSION_TIMEOUT = 3600  # 1 hour

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_file(file):
    """Validate file type, size, and content with enhanced security"""
    errors = []
    
    # Check filename
    if not file.filename:
        errors.append("No filename provided")
        return errors
    
    # Check file extension
    if not allowed_file(file.filename):
        errors.append(f"Invalid file type: {file.filename}. Only PDF files are allowed.")
        return errors
    
    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)  # Reset file pointer
    
    if file_size > MAX_FILE_SIZE:
        errors.append(f"File too large: {file.filename}. Maximum size is 16MB.")
        return errors
    
    # Check MIME type
    mime_type, _ = mimetypes.guess_type(file.filename)
    if mime_type != 'application/pdf':
        errors.append(f"Invalid MIME type: {file.filename}. Expected PDF file.")
        return errors
    
    # Additional security: Check for potential malicious content
    file_content = file.read()
    file.seek(0)  # Reset for later use
    
    # Check for executable content in PDF (basic check)
    if b'%PDF' not in file_content[:1024]:
        errors.append(f"Invalid PDF format: {file.filename}")
        return errors
    
    return errors

def generate_file_hash(file_content):
    """Generate SHA-256 hash of file content for duplicate detection"""
    return hashlib.sha256(file_content).hexdigest()

def cleanup_old_files():
    """Clean up files older than session timeout"""
    try:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        current_time = datetime.now()
        
        for filename in os.listdir(upload_folder):
            file_path = os.path.join(upload_folder, filename)
            if os.path.isfile(file_path):
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                if current_time - file_time > timedelta(seconds=SESSION_TIMEOUT):
                    os.remove(file_path)
                    print(f"Cleaned up old file: {filename}")
    except Exception as e:
        print(f"Error during cleanup: {e}")

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload endpoint with enhanced security"""
    try:
        # Clean up old files first
        cleanup_old_files()
        
        # Check if files are present in request
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        
        if not files or files[0].filename == '':
            return jsonify({'error': 'No files selected'}), 400
        
        uploaded_files = []
        file_hashes = set()  # Track file hashes to prevent duplicates
        
        for file in files:
            # Validate file with enhanced security
            validation_errors = validate_file(file)
            if validation_errors:
                return jsonify({'error': validation_errors[0]}), 400
            
            # Read file content for hash generation
            file_content = file.read()
            file_hash = generate_file_hash(file_content)
            
            # Check for duplicate content
            if file_hash in file_hashes:
                return jsonify({'error': f'Duplicate file content detected: {file.filename}'}), 400
            
            file_hashes.add(file_hash)
            
            # Generate unique filename with timestamp
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_filename = f"{timestamp}_{uuid.uuid4()}_{filename}"
            
            # Save file to upload folder
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            
            # Write file content with error handling
            try:
                with open(file_path, 'wb') as f:
                    f.write(file_content)
            except Exception as e:
                return jsonify({'error': f'Failed to save file: {filename}. Error: {str(e)}'}), 500
            
            # Verify file was saved correctly
            if not os.path.exists(file_path):
                return jsonify({'error': f'Failed to save file: {filename}'}), 500
            
            file_size = os.path.getsize(file_path)
            if file_size != len(file_content):
                # Clean up corrupted file
                os.remove(file_path)
                return jsonify({'error': f'File corruption detected: {filename}'}), 500
            
            uploaded_files.append({
                'filename': unique_filename,
                'original_name': filename,
                'size': file_size,
                'hash': file_hash,
                'upload_time': datetime.now().isoformat()
            })
        
        # Store upload info in session for cleanup
        # if 'uploaded_files' not in session: # Removed session usage
        #     session['uploaded_files'] = []
        # session['uploaded_files'].extend([f['filename'] for f in uploaded_files])
        
        return jsonify({
            'message': f'Successfully uploaded {len(uploaded_files)} files',
            'files': uploaded_files
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Upload error: {str(e)}")
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@upload_bp.route('/upload-status', methods=['GET'])
def upload_status():
    """Get upload status and file information"""
    try:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        files = []
        
        if os.path.exists(upload_folder):
            for filename in os.listdir(upload_folder):
                if filename.endswith('.pdf'):
                    file_path = os.path.join(upload_folder, filename)
                    try:
                        file_stat = os.stat(file_path)
                        files.append({
                            'filename': filename,
                            'size': file_stat.st_size,
                            'uploaded_at': file_stat.st_ctime,
                            'modified_at': file_stat.st_mtime
                        })
                    except OSError as e:
                        current_app.logger.warning(f"Could not stat file {filename}: {e}")
                        continue
        
        return jsonify({
            'uploaded_files': files,
            'count': len(files),
            'upload_folder': upload_folder
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Upload status error: {str(e)}")
        return jsonify({'error': f'Failed to get upload status: {str(e)}'}), 500

@upload_bp.route('/upload/<filename>', methods=['DELETE'])
def delete_file(filename):
    """Delete a specific uploaded file"""
    try:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        file_path = os.path.join(upload_folder, filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        # Security check: ensure file is in upload folder
        if not os.path.abspath(file_path).startswith(os.path.abspath(upload_folder)):
            return jsonify({'error': 'Invalid file path'}), 400
        
        os.remove(file_path)
        
        return jsonify({
            'message': 'File deleted successfully',
            'filename': filename
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Delete file error: {str(e)}")
        return jsonify({'error': f'Failed to delete file: {str(e)}'}), 500

@upload_bp.route('/upload/clear', methods=['DELETE'])
def clear_uploads():
    """Clear all uploaded files with session cleanup"""
    try:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        
        # Clear session tracking
        # if 'uploaded_files' in session: # Removed session usage
        #     session.pop('uploaded_files')
        
        # Remove all files in upload folder
        cleared_count = 0
        for filename in os.listdir(upload_folder):
            file_path = os.path.join(upload_folder, filename)
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                    cleared_count += 1
                except Exception as e:
                    current_app.logger.error(f"Failed to delete {filename}: {e}")
        
        return jsonify({
            'message': f'Successfully cleared {cleared_count} uploaded files',
            'cleared_count': cleared_count
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Clear uploads error: {str(e)}")
        return jsonify({'error': f'Failed to clear uploads: {str(e)}'}), 500

@upload_bp.route('/upload/cleanup-session', methods=['POST'])
def cleanup_session():
    """Clean up session and associated files"""
    try:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        cleared_count = 0
        
        # Clear files associated with current session
        # if 'uploaded_files' in session: # Removed session usage
        #     for filename in session['uploaded_files']:
        #         file_path = os.path.join(upload_folder, filename)
        #         if os.path.exists(file_path):
        #             try:
        #                 os.remove(file_path)
        #                 cleared_count += 1
        #             except Exception as e:
        #                 current_app.logger.error(f"Failed to delete {filename}: {e}")
            
        # session.pop('uploaded_files') # Removed session usage
        
        # Also clean up old files
        cleanup_old_files()
        
        return jsonify({
            'message': f'Session cleaned up. Removed {cleared_count} files.',
            'cleared_count': cleared_count
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Session cleanup error: {str(e)}")
        return jsonify({'error': f'Session cleanup failed: {str(e)}'}), 500 