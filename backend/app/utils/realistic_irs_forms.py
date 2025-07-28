from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from typing import Dict, Any
import os
from datetime import datetime

class RealisticIRSFormGenerator:
    """Generates truly realistic IRS forms that match actual IRS layouts"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_irs_styles()
    
    def setup_irs_styles(self):
        """Setup styles to match actual IRS forms"""
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
            name='IRSFormSmall',
            parent=self.styles['Normal'],
            fontSize=7,
            spaceAfter=2
        ))
    
    def generate_realistic_w2(self, data: Dict[str, Any], output_path: str = None) -> str:
        """Generate a realistic W-2 form that matches the actual IRS W-2 layout"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"realistic_irs_forms/realistic_w2_{timestamp}.pdf"
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Create PDF document
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        story = []
        
        # W-2 Header with proper IRS styling
        story.append(Paragraph("Form W-2 Wage and Tax Statement", self.styles['IRSFormTitle']))
        story.append(Paragraph("2024", self.styles['IRSFormField']))
        story.append(Paragraph("Copy A—For Social Security Administration", self.styles['IRSFormSmall']))
        story.append(Spacer(1, 12))
        
        # Top section with SSN and EIN (matching real W-2 layout)
        top_section_data = [
            ['a Employee\'s social security number', data.get('employee_ssn', '123-45-6789')],
            ['b Employer identification number (EIN)', data.get('employer_ein', '11-1111111')],
            ['c Employer\'s name, address, and ZIP code', f"{data.get('employer_name', 'FAKE COMPANY INC')}<br/>123 Business St, Anytown, CA 12345"],
            ['d Control number', ''],
            ['e Employee\'s first name and initial', data.get('employee_name', 'John Doe').split()[0] + ' ' + (data.get('employee_name', 'John Doe').split()[1] if len(data.get('employee_name', 'John Doe').split()) > 1 else '')],
            ['f Employee\'s address and ZIP code', f"{data.get('employee_address', '456 Personal Ave')}<br/>Hometown, CA 67890"]
        ]
        
        top_section_table = Table(top_section_data, colWidths=[2.5*inch, 3.5*inch])
        top_section_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey)
        ]))
        story.append(top_section_table)
        story.append(Spacer(1, 12))
        
        # W-2 Boxes (matching real W-2 layout with proper box numbers)
        story.append(Paragraph("W-2 Information", self.styles['Heading2']))
        
        # Create a more realistic W-2 layout with proper box structure
        w2_boxes_data = [
            ['Box 1', 'Wages, tips, other compensation', f"${data.get('wages', 50000):,.2f}"],
            ['Box 2', 'Federal income tax withheld', f"${data.get('federal_tax_withheld', 8000):,.2f}"],
            ['Box 3', 'Social security wages', f"${data.get('social_security_wages', 50000):,.2f}"],
            ['Box 4', 'Social security tax withheld', f"${data.get('social_security_tax', 3100):,.2f}"],
            ['Box 5', 'Medicare wages and tips', f"${data.get('medicare_wages', 50000):,.2f}"],
            ['Box 6', 'Medicare tax withheld', f"${data.get('medicare_tax', 725):,.2f}"],
            ['Box 7', 'Social security tips', '$0.00'],
            ['Box 8', 'Allocated tips', '$0.00'],
            ['Box 9', '', ''],
            ['Box 10', 'Dependent care benefits', '$0.00'],
            ['Box 11', 'Nonqualified plans', '$0.00'],
            ['Box 12a', 'Code', ''],
            ['Box 12b', 'Code', ''],
            ['Box 12c', 'Code', ''],
            ['Box 12d', 'Code', ''],
            ['Box 13', 'Statutory employee', '☐'],
            ['Box 14', 'Other', ''],
            ['Box 15', 'State', data.get('state', 'CA')],
            ['Box 16', 'State wages, tips, etc.', f"${data.get('state_wages', 50000):,.2f}"],
            ['Box 17', 'State income tax', f"${data.get('state_tax', 2000):,.2f}"],
            ['Box 18', 'Local wages, tips, etc.', '$0.00'],
            ['Box 19', 'Local income tax', '$0.00'],
            ['Box 20', 'Locality name', data.get('state', 'CA')]
        ]
        
        w2_boxes_table = Table(w2_boxes_data, colWidths=[0.8*inch, 3.2*inch, 1.5*inch])
        w2_boxes_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('BACKGROUND', (1, 0), (1, -1), colors.lightgrey)
        ]))
        story.append(w2_boxes_table)
        
        # Footer with IRS information
        story.append(Spacer(1, 12))
        story.append(Paragraph("Department of the Treasury—Internal Revenue Service", self.styles['IRSFormSmall']))
        story.append(Paragraph("For Privacy Act and Paperwork Reduction Act Notice, see the separate instructions.", self.styles['IRSFormSmall']))
        story.append(Paragraph("Cat. No. 10134D", self.styles['IRSFormSmall']))
        
        # Build PDF
        doc.build(story)
        return output_path
    
    def generate_realistic_1099_int(self, data: Dict[str, Any], output_path: str = None) -> str:
        """Generate a realistic 1099-INT form that matches the actual IRS 1099-INT layout"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"realistic_irs_forms/realistic_1099_int_{timestamp}.pdf"
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Create PDF document
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        story = []
        
        # 1099-INT Header with proper IRS styling
        story.append(Paragraph("Form 1099-INT Interest Income", self.styles['IRSFormTitle']))
        story.append(Paragraph("2024", self.styles['IRSFormField']))
        story.append(Paragraph("Copy B—For Recipient", self.styles['IRSFormSmall']))
        story.append(Spacer(1, 12))
        
        # Payer and Recipient Information (matching real 1099-INT layout)
        info_section_data = [
            ['PAYER\'S name, street address, city or town, state or province, country, and ZIP or foreign postal code', 
             f"{data.get('payer_name', 'E BANK')}<br/>789 Bank St, Financial City, NY 10001"],
            ['PAYER\'S TIN', data.get('payer_tin', '22-2222222')],
            ['RECIPIENT\'S name, street address, city or town, state or province, country, and ZIP or foreign postal code',
             f"{data.get('recipient_name', 'John Doe')}<br/>456 Personal Ave, Hometown, CA 67890"],
            ['RECIPIENT\'S TIN', data.get('recipient_ssn', '123-45-6789')],
            ['Account number (see instructions)', data.get('account_number', 'F')]
        ]
        
        info_section_table = Table(info_section_data, colWidths=[3*inch, 3*inch])
        info_section_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey)
        ]))
        story.append(info_section_table)
        story.append(Spacer(1, 12))
        
        # 1099-INT Boxes (matching real 1099-INT layout)
        story.append(Paragraph("1099-INT Information", self.styles['Heading2']))
        
        int_boxes_data = [
            ['Box 1', 'Interest income', f"${data.get('interest_income', 300):,.2f}"],
            ['Box 2', 'Early withdrawal penalty', '$0.00'],
            ['Box 3', 'Interest on U.S. Savings bonds', '$0.00'],
            ['Box 4', 'Federal income tax withheld', f"${data.get('federal_tax_withheld', 0):,.2f}"],
            ['Box 5', 'Investment expenses', '$0.00'],
            ['Box 6', 'Foreign tax paid', '$0.00'],
            ['Box 7', 'Foreign country or U.S. possession', ''],
            ['Box 8', 'Tax-exempt interest', '$0.00'],
            ['Box 9', 'Specified private activity bond interest', '$0.00'],
            ['Box 10', 'Market discount', '$0.00'],
            ['Box 11', 'Bond premium on tax-exempt bond', '$0.00'],
            ['Box 12', 'Bond premium on taxable bond', '$0.00'],
            ['Box 13', 'Bond premium on U.S. obligation', '$0.00'],
            ['Box 14', 'Tax-exempt OID', '$0.00'],
            ['Box 15', 'Taxable OID', '$0.00']
        ]
        
        int_boxes_table = Table(int_boxes_data, colWidths=[0.8*inch, 3.2*inch, 1.5*inch])
        int_boxes_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('BACKGROUND', (1, 0), (1, -1), colors.lightgrey)
        ]))
        story.append(int_boxes_table)
        
        # Footer with IRS information
        story.append(Spacer(1, 12))
        story.append(Paragraph("Department of the Treasury—Internal Revenue Service", self.styles['IRSFormSmall']))
        story.append(Paragraph("For Privacy Act and Paperwork Reduction Act Notice, see the separate instructions.", self.styles['IRSFormSmall']))
        story.append(Paragraph("Cat. No. 10134D", self.styles['IRSFormSmall']))
        
        # Build PDF
        doc.build(story)
        return output_path
    
    def generate_realistic_1099_nec(self, data: Dict[str, Any], output_path: str = None) -> str:
        """Generate a realistic 1099-NEC form that matches the actual IRS 1099-NEC layout"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"realistic_irs_forms/realistic_1099_nec_{timestamp}.pdf"
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Create PDF document
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        story = []
        
        # 1099-NEC Header with proper IRS styling
        story.append(Paragraph("Form 1099-NEC Nonemployee Compensation", self.styles['IRSFormTitle']))
        story.append(Paragraph("2024", self.styles['IRSFormField']))
        story.append(Paragraph("Copy B—For Recipient", self.styles['IRSFormSmall']))
        story.append(Spacer(1, 12))
        
        # Payer and Recipient Information (matching real 1099-NEC layout)
        info_section_data = [
            ['PAYER\'S name, street address, city or town, state or province, country, and ZIP or foreign postal code', 
             f"{data.get('payer_name', 'E FREELANCE CORP')}<br/>321 Freelance Blvd, Contract City, TX 75001"],
            ['PAYER\'S TIN', data.get('payer_tin', '33-3333333')],
            ['RECIPIENT\'S name, street address, city or town, state or province, country, and ZIP or foreign postal code',
             f"{data.get('recipient_name', 'John Doe')}<br/>456 Personal Ave, Hometown, CA 67890"],
            ['RECIPIENT\'S TIN', data.get('recipient_ssn', '123-45-6789')],
            ['Account number (see instructions)', data.get('account_number', 'F')]
        ]
        
        info_section_table = Table(info_section_data, colWidths=[3*inch, 3*inch])
        info_section_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey)
        ]))
        story.append(info_section_table)
        story.append(Spacer(1, 12))
        
        # 1099-NEC Boxes (matching real 1099-NEC layout)
        story.append(Paragraph("1099-NEC Information", self.styles['Heading2']))
        
        nec_boxes_data = [
            ['Box 1', 'Nonemployee compensation', f"${data.get('nonemployee_compensation', 10000):,.2f}"],
            ['Box 2', 'Federal income tax withheld', f"${data.get('federal_tax_withheld', 1000):,.2f}"],
            ['Box 3', 'State/Payer\'s state no.', data.get('state', 'CA')],
            ['Box 4', 'State income tax withheld', f"${data.get('state_tax_withheld', 0):,.2f}"],
            ['Box 5', 'State/Payer\'s state no.', ''],
            ['Box 6', 'State income tax withheld', '$0.00'],
            ['Box 7', 'State income', f"${data.get('state_income', 10000):,.2f}"]
        ]
        
        nec_boxes_table = Table(nec_boxes_data, colWidths=[0.8*inch, 3.2*inch, 1.5*inch])
        nec_boxes_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('BACKGROUND', (1, 0), (1, -1), colors.lightgrey)
        ]))
        story.append(nec_boxes_table)
        
        # Footer with IRS information
        story.append(Spacer(1, 12))
        story.append(Paragraph("Department of the Treasury—Internal Revenue Service", self.styles['IRSFormSmall']))
        story.append(Paragraph("For Privacy Act and Paperwork Reduction Act Notice, see the separate instructions.", self.styles['IRSFormSmall']))
        story.append(Paragraph("Cat. No. 10134D", self.styles['IRSFormSmall']))
        
        # Build PDF
        doc.build(story)
        return output_path

def create_realistic_irs_forms():
    """Create truly realistic IRS forms for testing"""
    generator = RealisticIRSFormGenerator()
    
    # W-2 data
    w2_data = {
        'employer_name': 'FAKE COMPANY INC',
        'employer_ein': '11-1111111',
        'employee_name': 'John Doe',
        'employee_ssn': '123-45-6789',
        'employee_address': '456 Personal Ave',
        'wages': 50000,
        'federal_tax_withheld': 8000,
        'social_security_wages': 50000,
        'social_security_tax': 3100,
        'medicare_wages': 50000,
        'medicare_tax': 725,
        'state_wages': 50000,
        'state_tax': 2000,
        'state': 'CA'
    }
    
    # 1099-INT data
    int_data = {
        'payer_name': 'E BANK',
        'payer_tin': '22-2222222',
        'recipient_name': 'John Doe',
        'recipient_ssn': '123-45-6789',
        'account_number': 'F',
        'interest_income': 300,
        'federal_tax_withheld': 0
    }
    
    # 1099-NEC data
    nec_data = {
        'payer_name': 'E FREELANCE CORP',
        'payer_tin': '33-3333333',
        'recipient_name': 'John Doe',
        'recipient_ssn': '123-45-6789',
        'account_number': 'F',
        'nonemployee_compensation': 10000,
        'federal_tax_withheld': 1000,
        'state_income': 10000,
        'state': 'CA'
    }
    
    # Generate realistic forms
    w2_path = generator.generate_realistic_w2(w2_data)
    int_path = generator.generate_realistic_1099_int(int_data)
    nec_path = generator.generate_realistic_1099_nec(nec_data)
    
    print(f"✅ Generated realistic IRS forms:")
    print(f"   W-2: {w2_path}")
    print(f"   1099-INT: {int_path}")
    print(f"   1099-NEC: {nec_path}")
    
    return [w2_path, int_path, nec_path]

if __name__ == "__main__":
    create_realistic_irs_forms() 