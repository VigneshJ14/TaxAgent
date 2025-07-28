from flask import Blueprint, request, jsonify, current_app, send_file
from app.services.robust_form_filler import create_robust_filled_form
from app.services.precision_form_filler import create_precision_filled_form
from app.services.tax_calculator import TaxCalculator
from app.services.document_processor import DocumentProcessor
import os
import tempfile
from typing import Dict, Any

generate_bp = Blueprint('generate', __name__)

@generate_bp.route('/generate-form-1040', methods=['POST'])
def generate_form_1040():
    """Generate a proper Form 1040 with calculated values using precision approach"""
    try:
        data = request.get_json()
        personal_info = data.get('personal_info', {})
        tax_data = data.get('tax_data', {})
        income_summary = data.get('income_summary', {})  # Added income_summary
        
        # Prepare data for form generation
        form_data = {
            'personal_info': personal_info,
            'tax_data': tax_data,
            'income_summary': income_summary  # Added income_summary
        }
        
        # Path to the blank Form 1040
        blank_form_path = "realistic_irs_forms/blank-1040.pdf"
        
        if not os.path.exists(blank_form_path):
            return jsonify({'error': 'Blank Form 1040 not found'}), 404
        
        # Use the precision approach by default (best alignment)
        pdf_path = create_precision_filled_form(blank_form_path, form_data)
        
        filing_status = personal_info.get('filing_status', 'single')
        dependents = personal_info.get('dependents', 0)
        
        return send_file(
            pdf_path, 
            as_attachment=True, 
            download_name=f"Form1040_{filing_status}_{dependents}dependents.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        current_app.logger.error(f"Form 1040 generation error: {str(e)}")
        return jsonify({'error': f'Form 1040 generation failed: {str(e)}'}), 500

@generate_bp.route('/generate-robust-form-1040', methods=['POST'])
def generate_robust_form_1040_endpoint():
    """Generate a Form 1040 using the robust form filler approach"""
    try:
        data = request.get_json()
        personal_info = data.get('personal_info', {})
        tax_data = data.get('tax_data', {})
        income_summary = data.get('income_summary', {})  # Added income_summary
        
        # Prepare data for form generation
        form_data = {
            'personal_info': personal_info,
            'tax_data': tax_data,
            'income_summary': income_summary  # Added income_summary
        }
        
        # Path to the blank Form 1040
        blank_form_path = "realistic_irs_forms/blank-1040.pdf"
        
        if not os.path.exists(blank_form_path):
            return jsonify({'error': 'Blank Form 1040 not found'}), 404
        
        # Use the robust approach
        pdf_path = create_robust_filled_form(blank_form_path, form_data)
        
        filing_status = personal_info.get('filing_status', 'single')
        dependents = personal_info.get('dependents', 0)
        
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"Robust_Form1040_{filing_status}_{dependents}dependents.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        current_app.logger.error(f"Robust form generation error: {str(e)}")
        return jsonify({'error': f'Robust form generation failed: {str(e)}'}), 500

@generate_bp.route('/generate-precision-form-1040', methods=['POST'])
def generate_precision_form_1040_endpoint():
    """Generate a Form 1040 using the precision form filler approach"""
    try:
        data = request.get_json()
        personal_info = data.get('personal_info', {})
        tax_data = data.get('tax_data', {})
        income_summary = data.get('income_summary', {})  # Added income_summary
        
        # Prepare data for form generation
        form_data = {
            'personal_info': personal_info,
            'tax_data': tax_data,
            'income_summary': income_summary  # Added income_summary
        }
        
        # Path to the blank Form 1040
        blank_form_path = "realistic_irs_forms/blank-1040.pdf"
        
        if not os.path.exists(blank_form_path):
            return jsonify({'error': 'Blank Form 1040 not found'}), 404
        
        # Use the precision approach
        pdf_path = create_precision_filled_form(blank_form_path, form_data)
        
        filing_status = personal_info.get('filing_status', 'single')
        dependents = personal_info.get('dependents', 0)
        
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"Precision_Form1040_{filing_status}_{dependents}dependents.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        current_app.logger.error(f"Precision form generation error: {str(e)}")
        return jsonify({'error': f'Precision form generation failed: {str(e)}'}), 500 