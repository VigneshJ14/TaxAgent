import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from io import BytesIO
from typing import Dict, Any, Tuple
import os
from datetime import datetime

class RobustFormFiller:
    """Fill Form 1040 using PyMuPDF for better PDF preservation"""
    
    def __init__(self):
        self.font_size = 9
        self.text_color = colors.black
        
    def get_form_coordinates(self) -> Dict[str, Tuple[float, float]]:
        """Get the coordinates for form fields on Form 1040"""
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
    
    def create_filled_form(self, blank_form_path: str, tax_data: Dict[str, Any], output_path: str = None) -> str:
        """
        Create a filled Form 1040 using PyMuPDF for better PDF preservation
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"robust_form_1040_{timestamp}.pdf"
        
        # Check if blank form exists
        if not os.path.exists(blank_form_path):
            raise FileNotFoundError(f"Blank Form 1040 not found at {blank_form_path}")
        
        # Open the PDF with PyMuPDF
        doc = fitz.open(blank_form_path)
        page = doc[0]
        
        # Extract data
        personal_info = tax_data.get('personal_info', {})
        tax_calc = tax_data.get('tax_data', {})
        income_summary = tax_data.get('income_summary', {})
        
        # Get coordinates
        coordinates = self.get_form_coordinates()
        
        # Add fallback coordinates for missing lines based on typical Form 1040 layout
        fallback_coordinates = {
            'line_1a_wages': (510.98, 636.91),      # Wages
            'line_2b_interest': (510.98, 648.91),   # Interest
            'line_16_tax': (510.98, 737.0),         # Tax
            'line_21_federal_withheld': (510.98, 636.91),  # Federal withheld
            'line_29_total_payments': (510.98, 648.91),    # Total payments
            'line_30_amount_owed': (510.98, 595.0),        # Amount owed
            'line_31_overpayment': (510.98, 595.0),        # Overpayment
        }
        
        # Add fallback coordinates only if not already detected
        for field, coord in fallback_coordinates.items():
            if field not in coordinates:
                coordinates[field] = coord
                print(f"Added fallback coordinate for {field}: {coord}")
        
        # Fill form fields using PyMuPDF
        self._fill_form_fields_pymupdf(page, coordinates, personal_info, tax_calc, income_summary)
        
        # Save the filled form
        doc.save(output_path)
        doc.close()
        
        return output_path
    
    def _fill_form_fields_pymupdf(self, page, coordinates: Dict[str, Tuple[float, float]], 
                                 personal_info: Dict, tax_calc: Dict, income_summary: Dict):
        """Fill form fields using PyMuPDF"""
        
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
        
        # Debug: Print all available coordinates
        print(f"\n🔍 Available coordinates: {list(coordinates.keys())}")
        print(f"📊 Income summary: {income_summary}")
        print(f"📊 Tax calc: {tax_calc}")

def create_robust_filled_form(blank_form_path: str, tax_data: Dict[str, Any]) -> str:
    """
    Create a filled Form 1040 using PyMuPDF for better PDF preservation
    
    Args:
        blank_form_path: Path to the blank Form 1040 PDF
        tax_data: Dictionary containing tax calculation results
        
    Returns:
        Path to the filled Form 1040 PDF
    """
    filler = RobustFormFiller()
    return filler.create_filled_form(blank_form_path, tax_data) 