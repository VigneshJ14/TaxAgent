from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import os

def create_sample_w2():
    """Create a sample W-2 form PDF"""
    filename = "sample_w2_2024.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=20,
        alignment=1  # Center alignment
    )
    story.append(Paragraph("Form W-2 Wage and Tax Statement 2024", title_style))
    story.append(Spacer(1, 20))
    
    # Employer Information
    employer_data = [
        ['a Employer identification number (EIN)', '12-3456789'],
        ['b Employer\'s name, address, and ZIP code', 'ACME CORPORATION<br/>123 Business St<br/>Anytown, CA 90210'],
        ['c Employer\'s name, address, and ZIP code', 'ACME CORPORATION<br/>123 Business St<br/>Anytown, CA 90210']
    ]
    
    employer_table = Table(employer_data, colWidths=[3*inch, 4*inch])
    employer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(employer_table)
    story.append(Spacer(1, 20))
    
    # Employee Information
    employee_data = [
        ['d Employee\'s first name and initial', 'John'],
        ['e Employee\'s name and address', 'John Doe<br/>123 Main St<br/>Anytown, CA 90210'],
        ['f Employee\'s SSN', '123-45-6789']
    ]
    
    employee_table = Table(employee_data, colWidths=[3*inch, 4*inch])
    employee_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(employee_table)
    story.append(Spacer(1, 20))
    
    # Wage Information
    wage_data = [
        ['1 Wages, tips, other compensation', '$75,000.00'],
        ['2 Federal income tax withheld', '$12,000.00'],
        ['3 Social security wages', '$75,000.00'],
        ['4 Social security tax withheld', '$4,650.00'],
        ['5 Medicare wages and tips', '$75,000.00'],
        ['6 Medicare tax withheld', '$1,087.50'],
        ['7 Social security tips', '$0.00'],
        ['8 Allocated tips', '$0.00'],
        ['9', ''],
        ['10 Dependent care benefits', '$0.00'],
        ['11 Nonqualified plan distributions', '$0.00'],
        ['12a See instructions for box 12', 'D $5,000.00'],
        ['12b', ''],
        ['12c', ''],
        ['12d', ''],
        ['13 Statutory employee', ''],
        ['14 Other', ''],
        ['15 State', 'CA'],
        ['16 State wages, tips, etc.', '$75,000.00'],
        ['17 State income tax', '$3,000.00'],
        ['18 Local wages, tips, etc.', '$75,000.00'],
        ['19 Local income tax', '$1,500.00'],
        ['20 Locality name', 'Anytown']
    ]
    
    wage_table = Table(wage_data, colWidths=[3*inch, 2*inch])
    wage_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(wage_table)
    
    doc.build(story)
    return filename

def create_sample_1099_int():
    """Create a sample 1099-INT form PDF"""
    filename = "sample_1099_int_2024.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=20,
        alignment=1
    )
    story.append(Paragraph("Form 1099-INT Interest Income 2024", title_style))
    story.append(Spacer(1, 20))
    
    # Payer Information
    payer_data = [
        ['1 Payer\'s name, street address, city, state, ZIP code, and telephone no.', 'BANK OF AMERICA<br/>123 Banking Ave<br/>Charlotte, NC 28202<br/>(800) 432-1000'],
        ['2 Payer\'s TIN', '12-3456789'],
        ['3 Recipient\'s TIN', '123-45-6789'],
        ['4 Recipient\'s name', 'John Doe'],
        ['5 Recipient\'s address', '123 Main St<br/>Anytown, CA 90210'],
        ['6 Account number', '1234567890'],
        ['7 CUSIP number', ''],
        ['8 Foreign country code', ''],
        ['9 Foreign country name', ''],
        ['10 Foreign country code', ''],
        ['11 Foreign country name', ''],
        ['12 Foreign country code', ''],
        ['13 Foreign country name', ''],
        ['14 Foreign country code', ''],
        ['15 Foreign country name', '']
    ]
    
    payer_table = Table(payer_data, colWidths=[4*inch, 3*inch])
    payer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(payer_table)
    story.append(Spacer(1, 20))
    
    # Interest Information
    interest_data = [
        ['1 Interest income', '$500.00'],
        ['2 Early withdrawal penalty', '$0.00'],
        ['3 Interest on U.S. Savings Bonds and Treasury obligations', '$0.00'],
        ['4 Federal income tax withheld', '$0.00'],
        ['5 Investment expenses', '$0.00'],
        ['6 Foreign tax paid', '$0.00'],
        ['7 Foreign country or U.S. possession', ''],
        ['8 Tax-exempt interest', '$0.00'],
        ['9 Specified private activity bond interest', '$0.00'],
        ['10 Market discount', '$0.00'],
        ['11 Bond premium on tax-exempt bond', '$0.00'],
        ['12 Bond premium on taxable bond', '$0.00'],
        ['13 Bond premium on U.S. obligations', '$0.00'],
        ['14 Bond premium on tax-exempt obligations', '$0.00'],
        ['15 Bond premium on taxable obligations', '$0.00'],
        ['16 Bond premium on U.S. obligations', '$0.00'],
        ['17 Bond premium on tax-exempt obligations', '$0.00'],
        ['18 Bond premium on taxable obligations', '$0.00']
    ]
    
    interest_table = Table(interest_data, colWidths=[4*inch, 2*inch])
    interest_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(interest_table)
    
    doc.build(story)
    return filename

def create_sample_1099_nec():
    """Create a sample 1099-NEC form PDF"""
    filename = "sample_1099_nec_2024.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=20,
        alignment=1
    )
    story.append(Paragraph("Form 1099-NEC Nonemployee Compensation 2024", title_style))
    story.append(Spacer(1, 20))
    
    # Payer Information
    payer_data = [
        ['1 Payer\'s name, street address, city, state, ZIP code, and telephone no.', 'FREELANCE CORP<br/>456 Contract St<br/>Business City, NY 10001<br/>(555) 123-4567'],
        ['2 Payer\'s TIN', '98-7654321'],
        ['3 Recipient\'s TIN', '123-45-6789'],
        ['4 Recipient\'s name', 'John Doe'],
        ['5 Recipient\'s address', '123 Main St<br/>Anytown, CA 90210'],
        ['6 Account number', 'CONTRACT-2024-001']
    ]
    
    payer_table = Table(payer_data, colWidths=[4*inch, 3*inch])
    payer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(payer_table)
    story.append(Spacer(1, 20))
    
    # Compensation Information
    comp_data = [
        ['1 Nonemployee compensation', '$15,000.00'],
        ['2 Federal income tax withheld', '$1,500.00'],
        ['3', ''],
        ['4', ''],
        ['5', ''],
        ['6', ''],
        ['7', '']
    ]
    
    comp_table = Table(comp_data, colWidths=[4*inch, 2*inch])
    comp_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(comp_table)
    
    doc.build(story)
    return filename

def create_all_sample_documents():
    """Create all sample documents"""
    print("Creating sample tax documents...")
    
    # Create uploads directory if it doesn't exist
    uploads_dir = "uploads"
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    
    # Create sample documents
    w2_file = create_sample_w2()
    int_file = create_sample_1099_int()
    nec_file = create_sample_1099_nec()
    
    # Move files to uploads directory
    import shutil
    shutil.move(w2_file, os.path.join(uploads_dir, w2_file))
    shutil.move(int_file, os.path.join(uploads_dir, int_file))
    shutil.move(nec_file, os.path.join(uploads_dir, nec_file))
    
    print(f"✅ Created sample documents in {uploads_dir}/:")
    print(f"  - {w2_file}")
    print(f"  - {int_file}")
    print(f"  - {nec_file}")
    print("\nYou can now use these files to test the upload functionality!")

if __name__ == "__main__":
    create_all_sample_documents() 