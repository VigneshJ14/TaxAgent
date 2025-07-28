import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from io import BytesIO
from typing import Dict, Any, Tuple, List
import os
from datetime import datetime

class PrecisionFormFiller:
    """Fill Form 1040 with precision alignment using line detection"""
    
    def __init__(self):
        self.font_size = 9
        self.text_color = colors.black
        
    def detect_line_positions(self, blank_form_path: str) -> Dict[str, Tuple[float, float]]:
        """Detect exact line positions for precise text placement"""
        doc = fitz.open(blank_form_path)
        page = doc[0]
        
        # Get all text blocks
        blocks = page.get_text("dict")
        
        # Find horizontal lines and field positions
        field_positions = {}
        line_positions = {}
        
        for block in blocks['blocks']:
            if 'lines' in block:
                for line in block['lines']:
                    for span in line['spans']:
                        text = span['text'].strip()
                        bbox = span['bbox']
                        
                        if text:
                            # Store field label positions
                            text_lower = text.lower()
                            
                            if 'first name' in text_lower:
                                field_positions['first_name'] = {
                                    'label': text,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 8  # Move down to sit on line
                                }
                            elif 'last name' in text_lower:
                                field_positions['last_name'] = {
                                    'label': text,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 8
                                }
                            elif 'social security' in text_lower and 'your' in text_lower:
                                # This is the main SSN field in the top right
                                field_positions['ssn_main'] = {
                                    'label': text,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 8,
                                    'x_offset': 30  # Move right
                                }
                            elif 'address' in text_lower and 'number' in text_lower:
                                field_positions['address'] = {
                                    'label': text,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 16  # Move down more
                                }
                            elif 'city' in text_lower:
                                field_positions['city'] = {
                                    'label': text,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 16  # Move down more
                                }
                            elif 'state' in text_lower and len(text) < 10:
                                field_positions['state'] = {
                                    'label': text,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 12,  # Move down more
                                    'x_offset': -20  # Move left
                                }
                            elif 'zip' in text_lower:
                                field_positions['zip'] = {
                                    'label': text,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 12,  # Move down more
                                    'x_offset': -20  # Move left
                                }
                            elif 'single' in text_lower:
                                # Filing status checkbox - look for the actual checkbox position
                                field_positions['filing_status_single'] = {
                                    'label': text,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 5,
                                    'x_offset': -10  # Move left to center on checkbox
                                }
                            elif 'married' in text_lower and 'filing' in text_lower:
                                # Alternative filing status detection
                                field_positions['filing_status_married'] = {
                                    'label': text,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 5,
                                    'x_offset': -10
                                }
                            elif 'head' in text_lower and 'household' in text_lower:
                                # Alternative filing status detection
                                field_positions['filing_status_head'] = {
                                    'label': text,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 5,
                                    'x_offset': -10
                                }
                            
                            # Look for line numbers (income section)
                            if text.isdigit() and len(text) <= 2:
                                line_num = int(text)
                                if line_num in [1, 2, 8, 9, 11, 15, 16, 20, 21, 29, 30, 31, 32]:
                                    line_positions[f'line_{line_num}'] = {
                                        'number': line_num,
                                        'bbox': bbox,
                                        'line_y': bbox[1] + 5,  # Slightly above line
                                        'x_offset': -80  # Move further left for income values
                                    }
                            
                            # Look for specific line labels and patterns
                            text_lower = text.lower()
                            
                            # Line 1a: Wages, tips, other compensation
                            if any(keyword in text_lower for keyword in ['wages', 'tips', 'compensation']) and '1' in text:
                                line_positions['line_1a'] = {
                                    'number': 1,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 5,
                                    'x_offset': -80
                                }
                            elif 'wages' in text_lower and 'form' in text_lower:
                                line_positions['line_1a'] = {
                                    'number': 1,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 5,
                                    'x_offset': -80
                                }
                            
                            # Line 2b: Taxable interest
                            elif 'taxable' in text_lower and 'interest' in text_lower:
                                line_positions['line_2b'] = {
                                    'number': 2,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 5,
                                    'x_offset': -80
                                }
                            elif 'interest' in text_lower and 'income' in text_lower:
                                line_positions['line_2b'] = {
                                    'number': 2,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 5,
                                    'x_offset': -80
                                }
                            
                            # Line 8: Additional income
                            elif 'additional' in text_lower and 'income' in text_lower:
                                line_positions['line_8'] = {
                                    'number': 8,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 5,
                                    'x_offset': -80
                                }
                            elif 'other' in text_lower and 'income' in text_lower:
                                line_positions['line_8'] = {
                                    'number': 8,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 5,
                                    'x_offset': -80
                                }
                            
                            # Line 9: Total income
                            elif 'total' in text_lower and 'income' in text_lower:
                                line_positions['line_9'] = {
                                    'number': 9,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 5,
                                    'x_offset': -80
                                }
                            
                            # Line 11: Adjusted gross income
                            elif 'adjusted' in text_lower and 'gross' in text_lower:
                                line_positions['line_11'] = {
                                    'number': 11,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 5,
                                    'x_offset': -80
                                }
                            
                            # Line 15: Taxable income
                            elif 'taxable' in text_lower and 'income' in text_lower and '15' in text:
                                line_positions['line_15'] = {
                                    'number': 15,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 5,
                                    'x_offset': -80
                                }
                            
                            # Line 16: Tax
                            elif 'tax' in text_lower and 'liability' in text_lower:
                                line_positions['line_16'] = {
                                    'number': 16,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 5,
                                    'x_offset': -80
                                }
                            elif 'tax' in text_lower and '16' in text:
                                line_positions['line_16'] = {
                                    'number': 16,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 5,
                                    'x_offset': -80
                                }
                            
                            # Line 20: Total tax
                            elif 'total' in text_lower and 'tax' in text_lower:
                                line_positions['line_20'] = {
                                    'number': 20,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 5,
                                    'x_offset': -80
                                }
                            
                            # Line 21: Federal income tax withheld
                            elif 'federal' in text_lower and 'withheld' in text_lower:
                                line_positions['line_21'] = {
                                    'number': 21,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 5,
                                    'x_offset': -80
                                }
                            elif 'withheld' in text_lower and '21' in text:
                                line_positions['line_21'] = {
                                    'number': 21,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 5,
                                    'x_offset': -80
                                }
                            
                            # Line 29: Total payments
                            elif 'total' in text_lower and 'payments' in text_lower:
                                line_positions['line_29'] = {
                                    'number': 29,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 5,
                                    'x_offset': -80
                                }
                            elif 'payments' in text_lower and '29' in text:
                                line_positions['line_29'] = {
                                    'number': 29,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 5,
                                    'x_offset': -80
                                }
                            
                            # Line 30: Amount owed
                            elif 'amount' in text_lower and 'owed' in text_lower:
                                line_positions['line_30'] = {
                                    'number': 30,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 5,
                                    'x_offset': -80
                                }
                            elif 'owed' in text_lower and '30' in text:
                                line_positions['line_30'] = {
                                    'number': 30,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 5,
                                    'x_offset': -80
                                }
                            
                            # Line 31: Overpayment
                            elif 'overpayment' in text_lower:
                                line_positions['line_31'] = {
                                    'number': 31,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 5,
                                    'x_offset': -80
                                }
                            elif 'overpayment' in text_lower and '31' in text:
                                line_positions['line_31'] = {
                                    'number': 31,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 5,
                                    'x_offset': -80
                                }
                            
                            # Line 32: Refund
                            elif 'refund' in text_lower:
                                line_positions['line_32'] = {
                                    'number': 32,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 5,
                                    'x_offset': -80
                                }
                            elif 'refund' in text_lower and '32' in text:
                                line_positions['line_32'] = {
                                    'number': 32,
                                    'bbox': bbox,
                                    'line_y': bbox[1] + 5,
                                    'x_offset': -80
                                }
        
        doc.close()
        
        # Generate coordinates
        coordinates = {}
        
        # Personal information fields
        for field, info in field_positions.items():
            x = info['bbox'][0] + 50  # Move right from label
            if 'x_offset' in info:
                x += info['x_offset']  # Apply offset if specified
            y = info['line_y']
            coordinates[field] = (x, y)
        
        # Income section fields
        for field, info in line_positions.items():
            x = info['bbox'][0] + 100  # Move right from line number
            if 'x_offset' in info:
                x += info['x_offset']  # Apply left offset for income values
            y = info['line_y']
            coordinates[field] = (x, y)
        
        # Add precise coordinates based on analysis and user specifications
        precise_coordinates = {
            # Personal Information (updated based on user specifications)
            'first_name': (50, 90),  # Moved down by 10
            'last_name': (270, 90),  # Moved down by 10
            'ssn_main': (490, 93),  # Your social security number
            'address': (90.0, 143.7340087890625),
            'city': (90.0, 167.7349853515625),
            'state': (370, 170),
            'zip': (430, 168),
            
            # Filing Status (updated based on user specifications)
            'filing_status_single': (103, 208),  # Moved down by 5
            
            # Income Section - Page 1 (updated based on user specifications)
            'line_1a_wages': (500, 435),  # Moved down by 5
            'line_2b_interest': (500, 555),  # Moved down by 5
            'line_8_other_income': (500, 515),  # Moved up by 10
            'line_9_total_income': (500, 650),  # Moved down by 10
            'line_11_agi': (500, 675),  # Moved down by 5
            'line_15_taxable_income': (500, 723),  # Moved down by 3
            
            # Income Section - Page 2 (will be added)
            'line_16_tax': (500, 45),  # Moved up by 5
            'line_20_total_tax': (500, 92),  # Moved up by 8
            'line_21_federal_withheld': (500, 150),  # Line 21 (federal withheld) - Page 2
            'line_29_total_payments': (500, 200),  # Line 29 (total payments) - Page 2
            'line_30_amount_owed': (500, 250),  # Line 30 (amount owed) - Page 2
            'line_31_overpayment': (500, 300),  # Line 31 (overpayment) - Page 2
            'line_32_refund': (500, 350),  # Line 32 (refund) - Page 2
        }
        
        # Override with precise coordinates
        for field, coord in precise_coordinates.items():
            coordinates[field] = coord
            print(f"Using precise coordinate for {field}: {coord}")
        
        return coordinates
    
    def create_precision_filled_form(self, blank_form_path: str, tax_data: Dict[str, Any], output_path: str = None) -> str:
        """
        Create a filled Form 1040 with precision alignment
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"precision_form_1040_{timestamp}.pdf"
        
        # Check if blank form exists
        if not os.path.exists(blank_form_path):
            raise FileNotFoundError(f"Blank Form 1040 not found at {blank_form_path}")
        
        # Detect line positions (only from page 1 for labels)
        coordinates = self.detect_line_positions(blank_form_path)
        
        # Open the PDF with PyMuPDF
        doc = fitz.open(blank_form_path)
        
        # Ensure we have at least two pages for Form 1040
        if len(doc) < 2:
            # If blank-1040.pdf only has one page, we need to add a blank second page
            # This is a simplified approach; a more robust solution might involve creating
            # the second page content from scratch or using a blank two-page template.
            # For now, we'll just duplicate the first page as a placeholder if only one exists.
            # This is a temporary measure for debugging the coordinate system.
            if len(doc) == 1:
                doc.new_page(pno=1, width=doc[0].rect.width, height=doc[0].rect.height)
                print("Added a blank second page to the document for testing.")
            else:
                raise ValueError("Blank Form 1040 has no pages.")

        # Extract data
        personal_info = tax_data.get('personal_info', {})
        tax_calc = tax_data.get('tax_data', {})
        income_summary = tax_data.get('income_summary', {})
        
        # Fill form fields on Page 1
        page1 = doc[0]
        self._fill_form_fields_precision(page1, coordinates, personal_info, tax_calc, income_summary, page_num=1)

        # Fill form fields on Page 2
        page2 = doc[1]
        self._fill_form_fields_precision(page2, coordinates, personal_info, tax_calc, income_summary, page_num=2)
        
        # Save the filled form
        doc.save(output_path)
        doc.close()
        
        return output_path
    
    def _fill_form_fields_precision(self, page, coordinates: Dict[str, Tuple[float, float]], 
                                   personal_info: Dict, tax_calc: Dict, income_summary: Dict, page_num: int):
        """Fill form fields with precision alignment"""
        
        # Personal Information (only on page 1)
        if page_num == 1:
            if 'first_name' in coordinates:
                x, y = coordinates['first_name']
                page.insert_text((x, y), personal_info.get('first_name', 'John'), 
                               fontsize=self.font_size, color=(0, 0, 0))
                print(f"Filling first_name at ({x}, {y}): {personal_info.get('first_name', 'John')}")
            
            if 'last_name' in coordinates:
                x, y = coordinates['last_name']
                page.insert_text((x, y), personal_info.get('last_name', 'Doe'), 
                               fontsize=self.font_size, color=(0, 0, 0))
                print(f"Filling last_name at ({x}, {y}): {personal_info.get('last_name', 'Doe')}")
            
            if 'ssn_main' in coordinates:
                x, y = coordinates['ssn_main']
                page.insert_text((x, y), personal_info.get('ssn', '123-45-6789'), 
                               fontsize=self.font_size, color=(0, 0, 0))
                print(f"Filling ssn_main at ({x}, {y}): {personal_info.get('ssn', '123-45-6789')}")
            
            if 'address' in coordinates:
                x, y = coordinates['address']
                page.insert_text((x, y), personal_info.get('address', '456 Personal Ave'), 
                               fontsize=self.font_size, color=(0, 0, 0))
                print(f"Filling address at ({x}, {y}): {personal_info.get('address', '456 Personal Ave')}")
            
            if 'city' in coordinates:
                x, y = coordinates['city']
                page.insert_text((x, y), personal_info.get('city', 'Hometown'), 
                               fontsize=self.font_size, color=(0, 0, 0))
                print(f"Filling city at ({x}, {y}): {personal_info.get('city', 'Hometown')}")
            
            if 'state' in coordinates:
                x, y = coordinates['state']
                page.insert_text((x, y), personal_info.get('state', 'CA'), 
                               fontsize=self.font_size, color=(0, 0, 0))
                print(f"Filling state at ({x}, {y}): {personal_info.get('state', 'CA')}")
            
            if 'zip' in coordinates:
                x, y = coordinates['zip']
                page.insert_text((x, y), personal_info.get('zip', '67890'), 
                               fontsize=self.font_size, color=(0, 0, 0))
                print(f"Filling zip at ({x}, {y}): {personal_info.get('zip', '67890')}")
            
            # Filing Status checkbox - make it larger
            filing_status = personal_info.get('filing_status', 'single')
            if filing_status == 'single' and 'filing_status_single' in coordinates:
                x, y = coordinates['filing_status_single']
                page.insert_text((x, y), "●", fontsize=14, color=(0, 0, 0))  # Larger dot
                print(f"Filling filing_status_single at ({x}, {y}) with larger dot")
            else:
                # Fallback position for filing status checkbox
                page.insert_text((115.20, 200.10), "●", fontsize=14, color=(0, 0, 0))  # Larger dot
                print(f"Filling filing_status_single at fallback position (115.20, 200.10) with larger dot")
            
            # Income Section - ONLY on page 1
            # Line 1a: Wages, tips, other compensation (from W-2)
            if 'line_1a_wages' in coordinates:
                x, y = coordinates['line_1a_wages']
                value = f"${income_summary.get('wages', 0):,.2f}"
                page.insert_text((x, y), value, fontsize=self.font_size, color=(0, 0, 0))
                print(f"Filling line_1a_wages (wages from W-2) at ({x}, {y}): {value}")
            
            # Line 2b: Taxable interest (from 1099-INT)
            if 'line_2b_interest' in coordinates:
                x, y = coordinates['line_2b_interest']
                value = f"${income_summary.get('interest_income', 0):,.2f}"
                page.insert_text((x, y), value, fontsize=self.font_size, color=(0, 0, 0))
                print(f"Filling line_2b_interest (interest from 1099-INT) at ({x}, {y}): {value}")
            
            # Line 8: Additional income from Schedule 1 (from 1099-NEC)
            if 'line_8_other_income' in coordinates:
                x, y = coordinates['line_8_other_income']
                value = f"${income_summary.get('nonemployee_compensation', 0):,.2f}"
                page.insert_text((x, y), value, fontsize=self.font_size, color=(0, 0, 0))
                print(f"Filling line_8_other_income (other income from 1099-NEC) at ({x}, {y}): {value}")
            
            # Line 9: Total income (sum of all income)
            if 'line_9_total_income' in coordinates:
                x, y = coordinates['line_9_total_income']
                value = f"${income_summary.get('total_income', 0):,.2f}"
                page.insert_text((x, y), value, fontsize=self.font_size, color=(0, 0, 0))
                print(f"Filling line_9_total_income (total income) at ({x}, {y}): {value}")
            
            # Line 11: Adjusted gross income (same as total income for this case)
            if 'line_11_agi' in coordinates:
                x, y = coordinates['line_11_agi']
                value = f"${tax_calc.get('adjusted_gross_income', 0):,.2f}"
                page.insert_text((x, y), value, fontsize=self.font_size, color=(0, 0, 0))
                print(f"Filling line_11_agi (AGI) at ({x}, {y}): {value}")
            
            # Line 15: Taxable income
            if 'line_15_taxable_income' in coordinates:
                x, y = coordinates['line_15_taxable_income']
                value = f"${tax_calc.get('taxable_income', 0):,.2f}"
                page.insert_text((x, y), value, fontsize=self.font_size, color=(0, 0, 0))
                print(f"Filling line_15_taxable_income (taxable income) at ({x}, {y}): {value}")
        
        # Page 2 values - ONLY tax calculations, NO income values
        if page_num == 2:
            # Line 16: Tax
            if 'line_16_tax' in coordinates:
                x, y = coordinates['line_16_tax']
                value = f"${tax_calc.get('tax_liability', 0):,.2f}"
                page.insert_text((x, y), value, fontsize=self.font_size, color=(0, 0, 0))
                print(f"Filling line_16_tax (tax) at ({x}, {y}): {value}")
            
            # Line 20: Total tax
            if 'line_20_total_tax' in coordinates:
                x, y = coordinates['line_20_total_tax']
                value = f"${tax_calc.get('tax_liability', 0):,.2f}"
                page.insert_text((x, y), value, fontsize=self.font_size, color=(0, 0, 0))
                print(f"Filling line_20_total_tax (total tax) at ({x}, {y}): {value}")
            
            # Line 21: Federal income tax withheld (from W-2)
            if 'line_21_federal_withheld' in coordinates:
                x, y = coordinates['line_21_federal_withheld']
                value = f"${tax_calc.get('federal_income_tax_withheld', 0):,.2f}"
                page.insert_text((x, y), value, fontsize=self.font_size, color=(0, 0, 0))
                print(f"Filling line_21_federal_withheld (federal withheld from W-2) at ({x}, {y}): {value}")
            
            # Line 29: Total payments
            if 'line_29_total_payments' in coordinates:
                x, y = coordinates['line_29_total_payments']
                value = f"${tax_calc.get('federal_income_tax_withheld', 0):,.2f}"
                page.insert_text((x, y), value, fontsize=self.font_size, color=(0, 0, 0))
                print(f"Filling line_29_total_payments (total payments) at ({x}, {y}): {value}")
            
            # Refund or amount owed
            refund_amount = tax_calc.get('refund_or_amount_owed', 0)
            if refund_amount > 0:
                if 'line_31_overpayment' in coordinates:
                    x, y = coordinates['line_31_overpayment']
                    value = f"${refund_amount:,.2f}"
                    page.insert_text((x, y), value, fontsize=self.font_size, color=(0, 0, 0))
                    print(f"Filling line_31_overpayment (overpayment) at ({x}, {y}): {value}")
            else:
                if 'line_30_amount_owed' in coordinates:
                    x, y = coordinates['line_30_amount_owed']
                    value = f"${abs(refund_amount):,.2f}"
                    page.insert_text((x, y), value, fontsize=self.font_size, color=(0, 0, 0))
                    print(f"Filling line_30_amount_owed (amount owed) at ({x}, {y}): {value}")
            
            # Line 32: Refund
            if 'line_32_refund' in coordinates:
                x, y = coordinates['line_32_refund']
                value = f"${refund_amount:,.2f}"
                page.insert_text((x, y), value, fontsize=self.font_size, color=(0, 0, 0))
                print(f"Filling line_32_refund (refund) at ({x}, {y}): {value}")

def create_precision_filled_form(blank_form_path: str, tax_data: Dict[str, Any]) -> str:
    """
    Create a filled Form 1040 with precision alignment
    
    Args:
        blank_form_path: Path to the blank Form 1040 PDF
        tax_data: Dictionary containing tax calculation results
        
    Returns:
        Path to the filled Form 1040 PDF
    """
    filler = PrecisionFormFiller()
    return filler.create_precision_filled_form(blank_form_path, tax_data) 