"""
MedIntel AI - OCR Engine
"""
import os
import re
from pathlib import Path
from typing import Optional, List
from PIL import Image
import io

# Check for tesseract availability
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

# Check for pdf2image availability  
try:
    from pdf2image import convert_from_path
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False


def check_ocr_available() -> bool:
    """Check if OCR is available."""
    if not TESSERACT_AVAILABLE:
        return False
    try:
        pytesseract.get_tesseract_version()
        return True
    except Exception:
        return False


def run_ocr_on_image(image_path: str, lang: str = 'eng') -> str:
    """
    Run OCR on an image file.
    
    Args:
        image_path: Path to image file
        lang: OCR language (default: English)
        
    Returns:
        Extracted text from image
    """
    if not TESSERACT_AVAILABLE:
        return "[OCR Error: pytesseract not installed]"
    
    try:
        image = Image.open(image_path)
        # Preprocess image for better OCR
        image = preprocess_image(image)
        text = pytesseract.image_to_string(image, lang=lang)
        return clean_ocr_text(text)
    except Exception as e:
        return f"[OCR Error: {str(e)}]"


def run_ocr_on_image_object(image: Image.Image, lang: str = 'eng') -> str:
    """
    Run OCR on a PIL Image object.
    
    Args:
        image: PIL Image object
        lang: OCR language
        
    Returns:
        Extracted text
    """
    if not TESSERACT_AVAILABLE:
        return "[OCR Error: pytesseract not installed]"
    
    try:
        image = preprocess_image(image)
        text = pytesseract.image_to_string(image, lang=lang)
        return clean_ocr_text(text)
    except Exception as e:
        return f"[OCR Error: {str(e)}]"


def run_ocr_on_pdf(pdf_path: str, lang: str = 'eng') -> str:
    """
    Run OCR on a PDF file by converting to images first.
    
    Args:
        pdf_path: Path to PDF file
        lang: OCR language
        
    Returns:
        Extracted text from all pages
    """
    if not TESSERACT_AVAILABLE:
        return "[OCR Error: pytesseract not installed]"
    
    if not PDF2IMAGE_AVAILABLE:
        return "[OCR Error: pdf2image not installed. Install poppler-utils.]"
    
    try:
        # Convert PDF to images
        images = convert_from_path(pdf_path, dpi=300)
        
        all_text = []
        for i, image in enumerate(images):
            # Preprocess and OCR each page
            processed_image = preprocess_image(image)
            page_text = pytesseract.image_to_string(processed_image, lang=lang)
            all_text.append(f"--- Page {i+1} ---\n{page_text}")
        
        combined_text = "\n\n".join(all_text)
        return clean_ocr_text(combined_text)
    
    except Exception as e:
        return f"[OCR Error: {str(e)}]"


def preprocess_image(image: Image.Image) -> Image.Image:
    """
    Preprocess image for better OCR results.
    
    Args:
        image: PIL Image object
        
    Returns:
        Preprocessed image
    """
    # Convert to RGB if necessary
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Convert to grayscale
    image = image.convert('L')
    
    # Resize if too small
    width, height = image.size
    if width < 1000:
        ratio = 1000 / width
        new_size = (int(width * ratio), int(height * ratio))
        image = image.resize(new_size, Image.Resampling.LANCZOS)
    
    # Increase contrast
    from PIL import ImageEnhance
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)
    
    # Sharpen
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(1.5)
    
    return image


def clean_ocr_text(text: str) -> str:
    """
    Clean and normalize OCR output text.
    
    Args:
        text: Raw OCR text
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    
    # Fix common OCR errors
    replacements = {
        '|': 'I',
        '0': 'O',  # Only in specific contexts
        'l': '1',  # Only in numeric contexts
    }
    
    # Remove non-printable characters
    text = ''.join(char for char in text if char.isprintable() or char in '\n\t')
    
    # Clean up lines
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if line:  # Only keep non-empty lines
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)


def extract_tables_from_image(image_path: str) -> List[List[str]]:
    """
    Attempt to extract table data from image.
    
    Args:
        image_path: Path to image
        
    Returns:
        List of rows (each row is a list of cell values)
    """
    if not TESSERACT_AVAILABLE:
        return []
    
    try:
        image = Image.open(image_path)
        # Use tesseract with TSV output
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        
        # Group by line
        lines = {}
        for i, text in enumerate(data['text']):
            if text.strip():
                line_num = data['line_num'][i]
                if line_num not in lines:
                    lines[line_num] = []
                lines[line_num].append(text)
        
        return [lines[k] for k in sorted(lines.keys())]
    
    except Exception:
        return []


def get_ocr_confidence(image_path: str) -> float:
    """
    Get OCR confidence score for an image.
    
    Args:
        image_path: Path to image
        
    Returns:
        Average confidence score (0-100)
    """
    if not TESSERACT_AVAILABLE:
        return 0.0
    
    try:
        image = Image.open(image_path)
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        
        confidences = [int(c) for c in data['conf'] if int(c) > 0]
        if confidences:
            return sum(confidences) / len(confidences)
        return 0.0
    
    except Exception:
        return 0.0


def detect_document_orientation(image_path: str) -> int:
    """
    Detect document orientation.
    
    Args:
        image_path: Path to image
        
    Returns:
        Rotation angle needed (0, 90, 180, 270)
    """
    if not TESSERACT_AVAILABLE:
        return 0
    
    try:
        image = Image.open(image_path)
        osd = pytesseract.image_to_osd(image)
        
        # Parse rotation from OSD output
        for line in osd.split('\n'):
            if 'Rotate:' in line:
                angle = int(line.split(':')[1].strip())
                return angle
        return 0
    
    except Exception:
        return 0


def auto_rotate_image(image_path: str) -> Image.Image:
    """
    Auto-rotate image based on detected orientation.
    
    Args:
        image_path: Path to image
        
    Returns:
        Correctly oriented image
    """
    image = Image.open(image_path)
    
    rotation = detect_document_orientation(image_path)
    if rotation != 0:
        image = image.rotate(-rotation, expand=True)
    
    return image
