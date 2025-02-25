from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfform
from reportlab.pdfbase.pdfform import TextField
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from datetime import datetime

def generate_pdf(data, output_path):
    # Create the PDF document with AcroForm support
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    # Container for the 'Flowable' objects
    elements = []
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    # Add title
    elements.append(Paragraph("Job Order Details", title_style))
    elements.append(Spacer(1, 12))
    
    # Create form fields
    form = doc.acroForm
    
    # Company Information section with form fields
    company_data = [
        ['Company Information', ''],
        ['Company Name:', TextField(name='company_name', value=data.get('Company Name', ''), width=200, height=20)],
        ['Email:', TextField(name='email', value=data.get('Email', ''), width=200, height=20)],
        ['Address:', TextField(name='address', value=data.get('Address', ''), width=200, height=40)],
        ['Business Info:', TextField(name='business_info', value=data.get('Business Info', ''), width=200, height=20)],
        ['Tax ID:', TextField(name='tax_id', value=data.get('Tax ID', ''), width=200, height=20)]
    ]
    
    company_table = Table(company_data, colWidths=[2*inch, 4*inch])
    company_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(company_table)
    elements.append(Spacer(1, 20))
    
    # Module Information section with form fields
    module_data = [
        ['Module Information', ''],
        ['Plug In Module:', TextField(name='plugin_module', value=data.get('Plug In Module', ''), width=200, height=20)],
        ['Module & User License:', TextField(name='module_license', value=data.get('Module & User License', ''), width=200, height=20)],
        ['VPN Info:', TextField(name='vpn_info', value=data.get('VPN Info', ''), width=200, height=20)]
    ]
    
    module_table = Table(module_data, colWidths=[2*inch, 4*inch])
    module_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(module_table)
    elements.append(Spacer(1, 20))
    
    # Report and Migration Information section with form fields
    report_data = [
        ['Report and Migration Details', ''],
        ['Report Design Template:', TextField(name='report_template', value=data.get('Report Design Template', ''), width=200, height=20)],
        ['Migration Master Data:', TextField(name='migration_master', value=data.get('Migration Master Data', ''), width=200, height=20)],
        ['Migration Outstanding Balance:', TextField(name='migration_balance', value=data.get('Migration Outstanding Balance', ''), width=200, height=20)]
    ]
    
    report_table = Table(report_data, colWidths=[2*inch, 4*inch])
    report_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(report_table)
    elements.append(Spacer(1, 20))
    
    # Status section with form field
    status_data = [
        ['Status Information', ''],
        ['Current Status:', TextField(name='status', value=data.get('Status', ''), width=200, height=20)]
    ]
    
    status_table = Table(status_data, colWidths=[2*inch, 4*inch])
    status_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(status_table)
    
    # Build the PDF document
    doc.build(elements)