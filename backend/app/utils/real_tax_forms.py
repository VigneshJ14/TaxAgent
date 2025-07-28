from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from typing import Dict, Any
import os
from datetime import datetime

class RealTaxFormGenerator:
    """Generates real-looking IRS tax forms"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom styles for IRS forms"""
        self.styles.add(ParagraphStyle(
            name='IRSFormTitle',
            parent=self.styles['Heading1'],
            fontSize=12,
            fontName='Helvetica-Bold',
            spaceAfter=6,
            alignment=1  # Center
        ))
        
        self.styles.add(ParagraphStyle(
            name='IRSFormField',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=3
        ))
        
        self.styles.add(ParagraphStyle(
            name='IRSFormLabel',
            parent=self.styles['Normal'],
            fontSize=8,
            fontName='Helvetica-Bold'
        ))
    
    def generate_real_w2(self, data: Dict[str, Any], output_path: str = None) -> str:
        """Generate a real-looking W-2 form"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"real_tax_forms/real_w2_{timestamp}.pdf"
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Create PDF document
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        story = []
        
        # W-2 Header
        story.append(Paragraph("Form W-2 Wage and Tax Statement", self.styles['IRSFormTitle']))
        story.append(Paragraph("2024", self.styles['IRSFormField']))
        story.append(Spacer(1, 12))
        
        # Employer Information
        story.append(Paragraph("Employer Information", self.styles['Heading2']))
        employer_data = [
            ['Employer Name:', data.get('employer_name', 'FAKE COMPANY INC')],
            ['Employer EIN:', data.get('employer_ein', '11-1111111')],
            ['Employer Address:', '123 Business St, Anytown, CA 12345']
        ]
        
        employer_table = Table(employer_data, colWidths=[2*inch, 3.5*inch])
        employer_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(employer_table)
        story.append(Spacer(1, 12))
        
        # Employee Information
        story.append(Paragraph("Employee Information", self.styles['Heading2']))
        employee_data = [
            ['Employee Name:', data.get('employee_name', 'John Doe')],
            ['Employee SSN:', data.get('employee_ssn', '123-45-6789')],
            ['Employee Address:', '456 Personal Ave, Hometown, CA 67890']
        ]
        
        employee_table = Table(employee_data, colWidths=[2*inch, 3.5*inch])
        employee_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(employee_table)
        story.append(Spacer(1, 12))
        
        # W-2 Boxes (simplified version of actual W-2 layout)
        story.append(Paragraph("W-2 Information", self.styles['Heading2']))
        
        w2_boxes = [
            ['Box 1 - Wages, tips, other compensation', f"${data.get('wages', 50000):,.2f}"],
            ['Box 2 - Federal income tax withheld', f"${data.get('federal_tax_withheld', 8000):,.2f}"],
            ['Box 3 - Social Security wages', f"${data.get('social_security_wages', 50000):,.2f}"],
            ['Box 4 - Social Security tax withheld', f"${data.get('social_security_tax', 3100):,.2f}"],
            ['Box 5 - Medicare wages and tips', f"${data.get('medicare_wages', 50000):,.2f}"],
            ['Box 6 - Medicare tax withheld', f"${data.get('medicare_tax', 725):,.2f}"],
            ['Box 16 - State wages, tips, etc.', f"${data.get('state_wages', 50000):,.2f}"],
            ['Box 17 - State income tax', f"${data.get('state_tax', 2000):,.2f}"],
            ['Box 20 - Locality name', 'CA'],
        ]
        
        w2_table = Table(w2_boxes, colWidths=[3*inch, 2.5*inch])
        w2_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey)
        ]))
        story.append(w2_table)
        
        # Build PDF
        doc.build(story)
        return output_path
    
    def generate_real_1099_int(self, data: Dict[str, Any], output_path: str = None) -> str:
        """Generate a real-looking 1099-INT form"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"real_tax_forms/real_1099_int_{timestamp}.pdf"
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Create PDF document
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        story = []
        
        # 1099-INT Header
        story.append(Paragraph("Form 1099-INT Interest Income", self.styles['IRSFormTitle']))
        story.append(Paragraph("2024", self.styles['IRSFormField']))
        story.append(Spacer(1, 12))
        
        # Payer Information
        story.append(Paragraph("Payer Information", self.styles['Heading2']))
        payer_data = [
            ['Payer Name:', data.get('payer_name', 'E BANK')],
            ['Payer TIN:', data.get('payer_tin', '22-2222222')],
            ['Payer Address:', '789 Bank St, Financial City, NY 10001']
        ]
        
        payer_table = Table(payer_data, colWidths=[2*inch, 3.5*inch])
        payer_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(payer_table)
        story.append(Spacer(1, 12))
        
        # Recipient Information
        story.append(Paragraph("Recipient Information", self.styles['Heading2']))
        recipient_data = [
            ['Recipient Name:', data.get('recipient_name', 'John Doe')],
            ['Recipient SSN:', data.get('recipient_ssn', '123-45-6789')],
            ['Recipient Address:', '456 Personal Ave, Hometown, CA 67890']
        ]
        
        recipient_table = Table(recipient_data, colWidths=[2*inch, 3.5*inch])
        recipient_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(recipient_table)
        story.append(Spacer(1, 12))
        
        # 1099-INT Boxes
        story.append(Paragraph("1099-INT Information", self.styles['Heading2']))
        
        int_boxes = [
            ['Box 1 - Interest income', f"${data.get('interest_income', 300):,.2f}"],
            ['Box 2 - Early withdrawal penalty', f"${data.get('early_withdrawal_penalty', 0):,.2f}"],
            ['Box 3 - Interest on U.S. Savings bonds', f"${data.get('savings_bonds_interest', 0):,.2f}"],
            ['Box 4 - Federal income tax withheld', f"${data.get('federal_tax_withheld', 0):,.2f}"],
            ['Box 8 - Tax-exempt interest', f"${data.get('tax_exempt_interest', 0):,.2f}"],
            ['Box 10 - Market discount', f"${data.get('market_discount', 0):,.2f}"],
            ['Box 11 - Foreign tax paid', f"${data.get('foreign_tax_paid', 0):,.2f}"],
            ['Box 12 - Foreign country or U.S. possession', ''],
            ['Box 13 - Investment expenses', f"${data.get('investment_expenses', 0):,.2f}"],
        ]
        
        int_table = Table(int_boxes, colWidths=[3*inch, 2.5*inch])
        int_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey)
        ]))
        story.append(int_table)
        
        # Build PDF
        doc.build(story)
        return output_path
    
    def generate_real_1099_nec(self, data: Dict[str, Any], output_path: str = None) -> str:
        """Generate a real-looking 1099-NEC form"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"real_tax_forms/real_1099_nec_{timestamp}.pdf"
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Create PDF document
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        story = []
        
        # 1099-NEC Header
        story.append(Paragraph("Form 1099-NEC Nonemployee Compensation", self.styles['IRSFormTitle']))
        story.append(Paragraph("2024", self.styles['IRSFormField']))
        story.append(Spacer(1, 12))
        
        # Payer Information
        story.append(Paragraph("Payer Information", self.styles['Heading2']))
        payer_data = [
            ['Payer Name:', data.get('payer_name', 'E FREELANCE CORP')],
            ['Payer TIN:', data.get('payer_tin', '33-3333333')],
            ['Payer Address:', '321 Freelance Blvd, Contract City, TX 75001']
        ]
        
        payer_table = Table(payer_data, colWidths=[2*inch, 3.5*inch])
        payer_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(payer_table)
        story.append(Spacer(1, 12))
        
        # Recipient Information
        story.append(Paragraph("Recipient Information", self.styles['Heading2']))
        recipient_data = [
            ['Recipient Name:', data.get('recipient_name', 'John Doe')],
            ['Recipient SSN:', data.get('recipient_ssn', '123-45-6789')],
            ['Recipient Address:', '456 Personal Ave, Hometown, CA 67890']
        ]
        
        recipient_table = Table(recipient_data, colWidths=[2*inch, 3.5*inch])
        recipient_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(recipient_table)
        story.append(Spacer(1, 12))
        
        # 1099-NEC Boxes
        story.append(Paragraph("1099-NEC Information", self.styles['Heading2']))
        
        nec_boxes = [
            ['Box 1 - Nonemployee compensation', f"${data.get('nonemployee_compensation', 10000):,.2f}"],
            ['Box 4 - Federal income tax withheld', f"${data.get('federal_tax_withheld', 1000):,.2f}"],
            ['Box 5 - State tax withheld', f"${data.get('state_tax_withheld', 0):,.2f}"],
            ['Box 6 - State/Payer\'s state no.', 'CA'],
            ['Box 7 - State income', f"${data.get('state_income', 10000):,.2f}"],
        ]
        
        nec_table = Table(nec_boxes, colWidths=[3*inch, 2.5*inch])
        nec_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey)
        ]))
        story.append(nec_table)
        
        # Build PDF
        doc.build(story)
        return output_path

def create_real_tax_forms():
    """Create real-looking tax forms for testing"""
    generator = RealTaxFormGenerator()
    
    # W-2 data
    w2_data = {
        'employer_name': 'FAKE COMPANY INC',
        'employer_ein': '11-1111111',
        'employee_name': 'John Doe',
        'employee_ssn': '123-45-6789',
        'wages': 50000,
        'federal_tax_withheld': 8000,
        'social_security_wages': 50000,
        'social_security_tax': 3100,
        'medicare_wages': 50000,
        'medicare_tax': 725,
        'state_wages': 50000,
        'state_tax': 2000
    }
    
    # 1099-INT data
    int_data = {
        'payer_name': 'E BANK',
        'payer_tin': '22-2222222',
        'recipient_name': 'John Doe',
        'recipient_ssn': '123-45-6789',
        'interest_income': 300,
        'federal_tax_withheld': 0
    }
    
    # 1099-NEC data
    nec_data = {
        'payer_name': 'E FREELANCE CORP',
        'payer_tin': '33-3333333',
        'recipient_name': 'John Doe',
        'recipient_ssn': '123-45-6789',
        'nonemployee_compensation': 10000,
        'federal_tax_withheld': 1000,
        'state_income': 10000
    }
    
    # Generate forms
    w2_path = generator.generate_real_w2(w2_data)
    int_path = generator.generate_real_1099_int(int_data)
    nec_path = generator.generate_real_1099_nec(nec_data)
    
    print(f"✅ Generated real tax forms:")
    print(f"   W-2: {w2_path}")
    print(f"   1099-INT: {int_path}")
    print(f"   1099-NEC: {nec_path}")
    
    return [w2_path, int_path, nec_path]

if __name__ == "__main__":
    create_real_tax_forms() 