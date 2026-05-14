"""
MedIntel AI - Document Loader and Text Extraction
"""
import os
import re
from pathlib import Path
from typing import Dict, Optional, Tuple
from datetime import datetime
import shutil

# PDF extraction libraries
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

from PIL import Image
import sys
sys.path.append(str(Path(__file__).parent.parent))

from utils.config import UPLOADS_DIR, EXTRACTED_DIR, DOCUMENT_TYPES
from utils.helpers import generate_document_id, get_file_extension, sanitize_filename
from modules.ocr_engine import run_ocr_on_pdf, run_ocr_on_image, check_ocr_available


def save_uploaded_file(uploaded_file) -> Tuple[str, str]:
    """
    Save uploaded file to uploads directory.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        Tuple of (file_path, doc_id)
    """
    # Generate unique document ID
    doc_id = generate_document_id(uploaded_file.name, str(datetime.now()))
    
    # Sanitize filename
    safe_name = sanitize_filename(uploaded_file.name)
    filename = f"{doc_id}_{safe_name}"
    file_path = UPLOADS_DIR / filename
    
    # Save file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return str(file_path), doc_id


def extract_text_from_pdf_pymupdf(file_path: str) -> str:
    """
    Extract text from PDF using PyMuPDF.
    
    Args:
        file_path: Path to PDF file
        
    Returns:
        Extracted text
    """
    if not PYMUPDF_AVAILABLE:
        return ""
    
    try:
        doc = fitz.open(file_path)
        text_parts = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            if text.strip():
                text_parts.append(f"--- Page {page_num + 1} ---\n{text}")
        
        doc.close()
        return "\n\n".join(text_parts)
    
    except Exception as e:
        return f"[PyMuPDF Error: {str(e)}]"


def extract_text_from_pdf_pdfplumber(file_path: str) -> str:
    """
    Extract text from PDF using pdfplumber.
    
    Args:
        file_path: Path to PDF file
        
    Returns:
        Extracted text
    """
    if not PDFPLUMBER_AVAILABLE:
        return ""
    
    try:
        text_parts = []
        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    text_parts.append(f"--- Page {i + 1} ---\n{text}")
                
                # Also try to extract tables
                tables = page.extract_tables()
                for table in tables:
                    if table:
                        table_text = "\n".join([" | ".join([str(cell) if cell else "" for cell in row]) for row in table])
                        text_parts.append(f"[Table]\n{table_text}")
        
        return "\n\n".join(text_parts)
    
    except Exception as e:
        return f"[pdfplumber Error: {str(e)}]"


def extract_text_from_pdf(file_path: str) -> Tuple[str, bool]:
    """
    Extract text from PDF using available methods.
    Falls back to OCR if text extraction yields poor results.
    
    Args:
        file_path: Path to PDF file
        
    Returns:
        Tuple of (extracted_text, ocr_used)
    """
    text = ""
    ocr_used = False
    
    # Try PyMuPDF first
    if PYMUPDF_AVAILABLE:
        text = extract_text_from_pdf_pymupdf(file_path)
    
    # If PyMuPDF failed or returned little text, try pdfplumber
    if len(text.strip()) < 100 and PDFPLUMBER_AVAILABLE:
        pdfplumber_text = extract_text_from_pdf_pdfplumber(file_path)
        if len(pdfplumber_text) > len(text):
            text = pdfplumber_text
    
    # If still insufficient text, use OCR
    if len(text.strip()) < 100:
        if check_ocr_available():
            ocr_text = run_ocr_on_pdf(file_path)
            if not ocr_text.startswith("[OCR Error"):
                text = ocr_text
                ocr_used = True
    
    return text, ocr_used


def extract_text_from_image(file_path: str) -> Tuple[str, bool]:
    """
    Extract text from image using OCR.
    
    Args:
        file_path: Path to image file
        
    Returns:
        Tuple of (extracted_text, ocr_used)
    """
    if not check_ocr_available():
        return "[OCR not available. Please install tesseract-ocr.]", False
    
    text = run_ocr_on_image(file_path)
    return text, True


def extract_text(file_path: str) -> Tuple[str, bool]:
    """
    Extract text from any supported file type.
    
    Args:
        file_path: Path to file
        
    Returns:
        Tuple of (extracted_text, ocr_used)
    """
    extension = get_file_extension(file_path)
    
    if extension == 'pdf':
        return extract_text_from_pdf(file_path)
    elif extension in ['png', 'jpg', 'jpeg', 'tiff', 'bmp']:
        return extract_text_from_image(file_path)
    else:
        return f"[Unsupported file type: {extension}]", False


def detect_document_type(text: str) -> str:
    """
    Detect document type based on content.
    
    Args:
        text: Extracted text from document
        
    Returns:
        Detected document type
    """
    text_lower = text.lower()
    
    # Prescription indicators
    prescription_keywords = ['rx', 'prescription', 'medicine', 'tablet', 'capsule', 
                           'syrup', 'dose', 'mg', 'ml', 'twice daily', 'once daily',
                           'after food', 'before food', 'sos', 'prn']
    
    # Lab report indicators
    lab_keywords = ['laboratory', 'lab report', 'test result', 'hemoglobin', 'hba1c',
                   'cholesterol', 'glucose', 'creatinine', 'reference range', 'normal range',
                   'blood test', 'urine test', 'cbc', 'complete blood count']
    
    # Discharge summary indicators
    discharge_keywords = ['discharge summary', 'admission', 'discharge', 'diagnosis',
                         'chief complaint', 'history of present illness', 'hospital stay',
                         'treatment given', 'advice on discharge']
    
    # Insurance policy indicators
    insurance_keywords = ['insurance', 'policy', 'sum insured', 'premium', 'coverage',
                         'exclusion', 'waiting period', 'claim', 'copay', 'deductible',
                         'network hospital', 'cashless', 'reimbursement']
    
    # Hospital bill indicators
    bill_keywords = ['bill', 'invoice', 'charges', 'amount', 'total', 'payment',
                    'room rent', 'nursing charges', 'medicine charges', 'consultation fee',
                    'gst', 'tax', 'receipt', 'advance', 'balance']
    
    # Claim document indicators
    claim_keywords = ['claim form', 'claim number', 'claim id', 'tpa', 'pre-authorization',
                     'settlement', 'approved', 'rejected', 'pending']
    
    # Count keyword matches
    scores = {
        'Prescription': sum(1 for kw in prescription_keywords if kw in text_lower),
        'Lab Report': sum(1 for kw in lab_keywords if kw in text_lower),
        'Discharge Summary': sum(1 for kw in discharge_keywords if kw in text_lower),
        'Insurance Policy': sum(1 for kw in insurance_keywords if kw in text_lower),
        'Hospital Bill': sum(1 for kw in bill_keywords if kw in text_lower),
        'Claim Document': sum(1 for kw in claim_keywords if kw in text_lower),
    }
    
    # Return type with highest score
    max_score = max(scores.values())
    if max_score > 2:
        return max(scores, key=scores.get)
    
    return 'Other'


def save_extracted_text(doc_id: str, text: str) -> str:
    """
    Save extracted text to file.
    
    Args:
        doc_id: Document ID
        text: Extracted text
        
    Returns:
        Path to saved text file
    """
    text_path = EXTRACTED_DIR / f"{doc_id}.txt"
    with open(text_path, 'w', encoding='utf-8') as f:
        f.write(text)
    return str(text_path)


def load_extracted_text(text_path: str) -> str:
    """
    Load previously extracted text.
    
    Args:
        text_path: Path to text file
        
    Returns:
        Extracted text
    """
    try:
        with open(text_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return ""


def get_document_metadata(file_path: str, text: str) -> Dict:
    """
    Extract metadata from document.
    
    Args:
        file_path: Path to document
        text: Extracted text
        
    Returns:
        Document metadata
    """
    path = Path(file_path)
    
    metadata = {
        'filename': path.name,
        'file_size': path.stat().st_size if path.exists() else 0,
        'file_type': get_file_extension(str(path)),
        'text_length': len(text),
        'word_count': len(text.split()),
        'line_count': len(text.split('\n')),
        'document_type': detect_document_type(text),
        'extraction_time': datetime.now().isoformat()
    }
    
    # Try to extract dates from text
    date_patterns = [
        r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',
        r'\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4}',
    ]
    
    dates_found = []
    for pattern in date_patterns:
        dates_found.extend(re.findall(pattern, text, re.IGNORECASE))
    
    metadata['dates_found'] = dates_found[:5]  # Keep first 5 dates
    
    return metadata


def process_document(uploaded_file) -> Dict:
    """
    Complete document processing pipeline.
    
    Args:
        uploaded_file: Streamlit uploaded file
        
    Returns:
        Processing result with all extracted data
    """
    result = {
        'success': False,
        'doc_id': None,
        'file_path': None,
        'text_path': None,
        'text': '',
        'ocr_used': False,
        'document_type': 'Other',
        'metadata': {},
        'error': None
    }
    
    try:
        # Save uploaded file
        file_path, doc_id = save_uploaded_file(uploaded_file)
        result['file_path'] = file_path
        result['doc_id'] = doc_id
        
        # Extract text
        text, ocr_used = extract_text(file_path)
        result['text'] = text
        result['ocr_used'] = ocr_used
        
        # Check if extraction was successful
        if text.startswith('[') and 'Error' in text:
            result['error'] = text
            return result
        
        # Detect document type
        doc_type = detect_document_type(text)
        result['document_type'] = doc_type
        
        # Save extracted text
        text_path = save_extracted_text(doc_id, text)
        result['text_path'] = text_path
        
        # Get metadata
        metadata = get_document_metadata(file_path, text)
        result['metadata'] = metadata
        
        result['success'] = True
        
    except Exception as e:
        result['error'] = str(e)
    
    return result
