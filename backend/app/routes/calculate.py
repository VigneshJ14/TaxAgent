from flask import Blueprint, request, jsonify, current_app
from app.services.tax_calculator import TaxCalculator
from app.services.document_processor import DocumentProcessor
import os
from typing import Dict, Any

calculate_bp = Blueprint('calculate', __name__)

@calculate_bp.route('/calculate', methods=['POST'])
def calculate_tax():
    """Calculate tax liability based on uploaded documents and personal information"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract personal information
        filing_status = data.get('filing_status', 'single')
        dependents = data.get('dependents', 0)
        age = data.get('age', 0)
        
        # Initialize calculators
        tax_calculator = TaxCalculator()
        document_processor = DocumentProcessor()
        
        # Validate inputs
        validation = tax_calculator.validate_inputs(
            filing_status=filing_status,
            dependents=dependents,
            age=age
        )
        
        if not validation['is_valid']:
            return jsonify({
                'error': 'Invalid input data',
                'validation_errors': validation['errors']
            }), 400
        
        # Process uploaded documents to extract income data
        upload_folder = current_app.config['UPLOAD_FOLDER']
        income_data = {
            'wages': 0,
            'interest_income': 0,
            'nonemployee_compensation': 0,
            'federal_income_tax_withheld': 0
        }
        
        processed_documents = []
        
        if os.path.exists(upload_folder):
            pdf_files = [f for f in os.listdir(upload_folder) if f.endswith('.pdf')]
            
            for filename in pdf_files:
                file_path = os.path.join(upload_folder, filename)
                try:
                    extracted_data = document_processor.process_document(file_path)
                    
                    # Aggregate income data based on document type
                    if extracted_data.document_type.value == 'W-2':
                        income_data['wages'] += extracted_data.data.get('wages', 0)
                        income_data['federal_income_tax_withheld'] += extracted_data.data.get('federal_tax_withheld', 0)
                    
                    elif extracted_data.document_type.value == '1099-INT':
                        income_data['interest_income'] += extracted_data.data.get('interest_income', 0)
                        income_data['federal_income_tax_withheld'] += extracted_data.data.get('federal_tax_withheld', 0)
                    
                    elif extracted_data.document_type.value == '1099-NEC':
                        income_data['nonemployee_compensation'] += extracted_data.data.get('nonemployee_compensation', 0)
                        income_data['federal_income_tax_withheld'] += extracted_data.data.get('federal_tax_withheld', 0)
                    
                    processed_documents.append({
                        'filename': extracted_data.filename,
                        'document_type': extracted_data.document_type.value,
                        'confidence_score': extracted_data.confidence_score,
                        'extracted_data': extracted_data.data
                    })
                    
                except Exception as e:
                    current_app.logger.error(f"Error processing {filename}: {str(e)}")
                    processed_documents.append({
                        'filename': filename,
                        'document_type': 'UNKNOWN',
                        'confidence_score': 0.0,
                        'extracted_data': {},
                        'error': str(e)
                    })
        
        # Calculate tax liability
        tax_result = tax_calculator.calculate_tax(
            filing_status=filing_status,
            wages=income_data['wages'],
            interest_income=income_data['interest_income'],
            nonemployee_compensation=income_data['nonemployee_compensation'],
            federal_income_tax_withheld=income_data['federal_income_tax_withheld'],
            dependents=dependents,
            age=age
        )
        
        # Prepare response
        response_data = {
            'message': 'Tax calculation completed successfully',
            'personal_info': {
                'filing_status': filing_status,
                'dependents': dependents,
                'age': age
            },
            'income_summary': {
                'wages': income_data['wages'],
                'interest_income': income_data['interest_income'],
                'nonemployee_compensation': income_data['nonemployee_compensation'],
                'total_income': tax_result.total_income,
                'federal_income_tax_withheld': income_data['federal_income_tax_withheld']
            },
            'tax_calculation': {
                'adjusted_gross_income': tax_result.adjusted_gross_income,
                'standard_deduction': tax_result.standard_deduction,
                'taxable_income': tax_result.taxable_income,
                'tax_liability': tax_result.tax_liability,
                'total_payments': tax_result.total_payments,
                'refund_or_amount_owed': tax_result.refund_or_amount_owed
            },
            'breakdown': tax_result.breakdown,
            'processed_documents': processed_documents,
            'validation': {
                'warnings': validation['warnings']
            }
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        current_app.logger.error(f"Tax calculation error: {str(e)}")
        return jsonify({'error': f'Tax calculation failed: {str(e)}'}), 500

@calculate_bp.route('/calculate/estimate', methods=['POST'])
def estimate_tax():
    """Provide a quick tax estimate without processing documents"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract basic information
        filing_status = data.get('filing_status', 'single')
        total_income = data.get('total_income', 0)
        federal_income_tax_withheld = data.get('federal_income_tax_withheld', 0)
        dependents = data.get('dependents', 0)
        age = data.get('age', 0)
        
        # Initialize calculator
        tax_calculator = TaxCalculator()
        
        # Validate inputs
        validation = tax_calculator.validate_inputs(
            filing_status=filing_status,
            total_income=total_income,
            federal_income_tax_withheld=federal_income_tax_withheld,
            dependents=dependents,
            age=age
        )
        
        if not validation['is_valid']:
            return jsonify({
                'error': 'Invalid input data',
                'validation_errors': validation['errors']
            }), 400
        
        # Calculate tax liability
        tax_result = tax_calculator.calculate_tax(
            filing_status=filing_status,
            wages=total_income,  # Assume all income is wages for estimate
            interest_income=0,
            nonemployee_compensation=0,
            federal_income_tax_withheld=federal_income_tax_withheld,
            dependents=dependents,
            age=age
        )
        
        return jsonify({
            'message': 'Tax estimate completed',
            'estimate': {
                'total_income': tax_result.total_income,
                'tax_liability': tax_result.tax_liability,
                'federal_income_tax_withheld': tax_result.total_payments,
                'refund_or_amount_owed': tax_result.refund_or_amount_owed,
                'effective_tax_rate': (tax_result.tax_liability / tax_result.total_income * 100) if tax_result.total_income > 0 else 0
            },
            'breakdown': tax_result.breakdown
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Tax estimation error: {str(e)}")
        return jsonify({'error': f'Tax estimation failed: {str(e)}'}), 500 