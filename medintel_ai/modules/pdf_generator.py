"""
MedIntel AI - PDF Report Generator
"""
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
import sys

sys.path.append(str(Path(__file__).parent.parent))
from utils.config import REPORTS_DIR

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch, cm
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        PageBreak, Image, HRFlowable
    )
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def generate_pdf_report(summary_text: str, title: str = "MedIntel AI Health Report") -> Optional[str]:
    """
    Generate a PDF report from summary text.
    
    Args:
        summary_text: The summary text to include in the report
        title: Report title
        
    Returns:
        Path to generated PDF or None if failed
    """
    if not REPORTLAB_AVAILABLE:
        return None
    
    # Generate filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"medintel_report_{timestamp}.pdf"
    filepath = REPORTS_DIR / filename
    
    try:
        # Create document
        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#0066CC'),
            alignment=TA_CENTER
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=20,
            textColor=colors.HexColor('#666666'),
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceBefore=20,
            spaceAfter=10,
            textColor=colors.HexColor('#333333')
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            alignment=TA_JUSTIFY,
            leading=14
        )
        
        disclaimer_style = ParagraphStyle(
            'Disclaimer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#888888'),
            alignment=TA_CENTER,
            spaceBefore=20
        )
        
        # Build story
        story = []
        
        # Title
        story.append(Paragraph("🏥 MedIntel AI", title_style))
        story.append(Paragraph(title, subtitle_style))
        story.append(Paragraph(
            f"Generated on {datetime.now().strftime('%d %B %Y at %I:%M %p')}",
            subtitle_style
        ))
        
        # Horizontal line
        story.append(HRFlowable(
            width="100%",
            thickness=1,
            color=colors.HexColor('#0066CC'),
            spaceBefore=10,
            spaceAfter=20
        ))
        
        # Process summary text
        # Convert markdown-like formatting to paragraphs
        lines = summary_text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                story.append(Spacer(1, 6))
                continue
            
            # Handle headings
            if line.startswith('# '):
                story.append(Paragraph(line[2:], heading_style))
            elif line.startswith('## '):
                story.append(Spacer(1, 12))
                story.append(Paragraph(line[3:], heading_style))
            elif line.startswith('### '):
                story.append(Spacer(1, 8))
                story.append(Paragraph(f"<b>{line[4:]}</b>", body_style))
            elif line.startswith('---'):
                story.append(HRFlowable(
                    width="100%",
                    thickness=0.5,
                    color=colors.HexColor('#CCCCCC'),
                    spaceBefore=10,
                    spaceAfter=10
                ))
            elif line.startswith('- ') or line.startswith('* '):
                # Bullet point
                story.append(Paragraph(f"• {line[2:]}", body_style))
            elif line.startswith('|'):
                # Skip table markdown (handled separately if needed)
                continue
            else:
                # Clean up markdown formatting
                line = line.replace('**', '<b>').replace('__', '<b>')
                # Fix unclosed tags
                if line.count('<b>') % 2 != 0:
                    line = line.replace('<b>', '', 1)
                story.append(Paragraph(line, body_style))
        
        # Footer
        story.append(Spacer(1, 30))
        story.append(HRFlowable(
            width="100%",
            thickness=0.5,
            color=colors.HexColor('#CCCCCC'),
            spaceBefore=10,
            spaceAfter=10
        ))
        
        disclaimer = """
        <b>IMPORTANT DISCLAIMER:</b> This report is generated by MedIntel AI for informational purposes only. 
        It does not constitute medical advice, diagnosis, or treatment. Always consult with qualified 
        healthcare professionals for medical decisions. The AI analysis may contain errors or omissions.
        Verify all information with your healthcare providers and insurance company.
        """
        story.append(Paragraph(disclaimer, disclaimer_style))
        
        story.append(Spacer(1, 10))
        story.append(Paragraph(
            "MedIntel AI - Your Medical Memory, Insurance Decoder, and Hospital Bill Watchdog",
            ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, 
                          textColor=colors.HexColor('#0066CC'), alignment=TA_CENTER)
        ))
        
        # Build PDF
        doc.build(story)
        
        return str(filepath)
    
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None


def generate_comprehensive_report(
    documents: list,
    medicines: list,
    lab_values: list,
    insurance_risks: list,
    bill_risks: list
) -> Optional[str]:
    """
    Generate a comprehensive PDF report with all data.
    
    Returns:
        Path to generated PDF
    """
    if not REPORTLAB_AVAILABLE:
        return None
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"medintel_comprehensive_{timestamp}.pdf"
    filepath = REPORTS_DIR / filename
    
    try:
        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50
        )
        
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'Title', fontSize=20, spaceAfter=20, 
            textColor=colors.HexColor('#0066CC'), alignment=TA_CENTER
        )
        story.append(Paragraph("MedIntel AI - Comprehensive Health Report", title_style))
        story.append(Paragraph(
            f"Generated: {datetime.now().strftime('%d %B %Y')}",
            ParagraphStyle('Date', fontSize=10, alignment=TA_CENTER, 
                          textColor=colors.gray, spaceAfter=20)
        ))
        
        # Documents Section
        if documents:
            story.append(Paragraph("Documents Analyzed", styles['Heading2']))
            doc_data = [['Filename', 'Type', 'Upload Date']]
            for d in documents[:20]:
                doc_data.append([
                    d.get('filename', 'Unknown')[:30],
                    d.get('document_type', 'Unknown'),
                    str(d.get('upload_time', ''))[:10]
                ])
            
            table = Table(doc_data, colWidths=[200, 100, 100])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066CC')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ]))
            story.append(table)
            story.append(Spacer(1, 20))
        
        # Medicines Section
        if medicines:
            story.append(Paragraph("Current Medications", styles['Heading2']))
            med_data = [['Medicine', 'Dose', 'Frequency']]
            for m in medicines[:20]:
                med_data.append([
                    m.get('name', 'Unknown'),
                    m.get('dose', ''),
                    m.get('frequency', '')
                ])
            
            table = Table(med_data, colWidths=[180, 80, 140])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#28A745')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
            ]))
            story.append(table)
            story.append(Spacer(1, 20))
        
        # Lab Values Section
        if lab_values:
            story.append(Paragraph("Lab Test Results", styles['Heading2']))
            lab_data = [['Test', 'Value', 'Unit', 'Status']]
            for l in lab_values[:20]:
                status = l.get('status', 'Unknown')
                lab_data.append([
                    l.get('test_name', 'Unknown'),
                    str(l.get('value', '')),
                    l.get('unit', ''),
                    status.upper() if status else 'N/A'
                ])
            
            table = Table(lab_data, colWidths=[150, 80, 80, 90])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#17A2B8')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
            ]))
            story.append(table)
            story.append(Spacer(1, 20))
        
        # Insurance Risks Section
        if insurance_risks:
            story.append(Paragraph("Insurance Policy Findings", styles['Heading2']))
            for risk in insurance_risks[:10]:
                story.append(Paragraph(
                    f"<b>{risk.get('clause_type', 'Unknown')}:</b> {risk.get('simple_meaning', '')}",
                    ParagraphStyle('Risk', fontSize=9, spaceAfter=6)
                ))
            story.append(Spacer(1, 20))
        
        # Bill Risks Section
        if bill_risks:
            story.append(Paragraph("Billing Observations", styles['Heading2']))
            for risk in bill_risks[:10]:
                story.append(Paragraph(
                    f"• <b>{risk.get('item_name', 'Unknown')}:</b> {risk.get('reason', '')}",
                    ParagraphStyle('Bill', fontSize=9, spaceAfter=6)
                ))
        
        # Disclaimer
        story.append(Spacer(1, 30))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.gray))
        story.append(Paragraph(
            "DISCLAIMER: This report is for informational purposes only and does not constitute medical advice.",
            ParagraphStyle('Disclaimer', fontSize=7, textColor=colors.gray, 
                          alignment=TA_CENTER, spaceBefore=10)
        ))
        
        doc.build(story)
        return str(filepath)
    
    except Exception as e:
        print(f"Error generating comprehensive PDF: {e}")
        return None


def check_pdf_available() -> bool:
    """Check if PDF generation is available."""
    return REPORTLAB_AVAILABLE


def get_report_list() -> list:
    """Get list of generated reports."""
    reports = []
    for f in REPORTS_DIR.glob('*.pdf'):
        reports.append({
            'filename': f.name,
            'path': str(f),
            'size': f.stat().st_size,
            'created': datetime.fromtimestamp(f.stat().st_ctime)
        })
    return sorted(reports, key=lambda x: x['created'], reverse=True)


def delete_report(filename: str) -> bool:
    """Delete a report file."""
    filepath = REPORTS_DIR / filename
    if filepath.exists():
        filepath.unlink()
        return True
    return False
