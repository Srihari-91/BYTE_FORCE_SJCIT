"""
MedIntel AI - Helper Utilities
"""
import re
import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
import hashlib

def clean_text(text: str) -> str:
    """Clean and normalize text."""
    if not text:
        return ""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep medical notation
    text = re.sub(r'[^\w\s\.\,\:\;\-\(\)\[\]\/\%\+\=\<\>\@\#\&\*]', '', text)
    return text.strip()

def extract_numbers(text: str) -> List[float]:
    """Extract numeric values from text."""
    numbers = re.findall(r'[-+]?\d*\.?\d+', text)
    return [float(n) for n in numbers if n]

def parse_date(date_str: str) -> Optional[datetime]:
    """Parse date string in various formats."""
    formats = [
        "%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d",
        "%d %b %Y", "%d %B %Y", "%b %d, %Y",
        "%d/%m/%y", "%d-%m-%y"
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    return None

def safe_json_parse(json_str: str) -> Optional[Dict]:
    """Safely parse JSON string."""
    try:
        # Try to find JSON in the string
        json_match = re.search(r'\{[\s\S]*\}', json_str)
        if json_match:
            return json.loads(json_match.group())
        return None
    except json.JSONDecodeError:
        return None

def calculate_confidence(scores: List[float]) -> str:
    """Calculate confidence level from retrieval scores."""
    if not scores:
        return "Low"
    avg_score = sum(scores) / len(scores)
    if avg_score > 0.7:
        return "High"
    elif avg_score > 0.4:
        return "Medium"
    return "Low"

def normalize_lab_name(name: str) -> str:
    """Normalize lab test names for comparison."""
    name = name.lower().strip()
    # Common normalizations
    normalizations = {
        "hb": "hemoglobin",
        "hgb": "hemoglobin",
        "haemoglobin": "hemoglobin",
        "hba1c": "hba1c",
        "glycated hemoglobin": "hba1c",
        "glycosylated hemoglobin": "hba1c",
        "fbs": "fasting_glucose",
        "fasting blood sugar": "fasting_glucose",
        "fasting glucose": "fasting_glucose",
        "rbs": "random_glucose",
        "random blood sugar": "random_glucose",
        "ppbs": "postprandial_glucose",
        "tc": "total_cholesterol",
        "total cholesterol": "total_cholesterol",
        "ldl cholesterol": "ldl",
        "ldl-c": "ldl",
        "hdl cholesterol": "hdl",
        "hdl-c": "hdl",
        "tg": "triglycerides",
        "triglyceride": "triglycerides",
        "creat": "creatinine",
        "serum creatinine": "creatinine",
        "blood urea": "urea",
        "bun": "urea",
        "alt": "sgpt",
        "alanine aminotransferase": "sgpt",
        "ast": "sgot",
        "aspartate aminotransferase": "sgot",
        "thyroid stimulating hormone": "tsh",
        "white blood cells": "wbc",
        "leucocytes": "wbc",
        "wbc count": "wbc",
        "platelet count": "platelets",
        "plt": "platelets",
        "red blood cells": "rbc",
        "erythrocytes": "rbc",
        "total bilirubin": "bilirubin",
        "serum albumin": "albumin",
        "vit d": "vitamin_d",
        "vitamin d3": "vitamin_d",
        "25-hydroxy vitamin d": "vitamin_d",
        "vit b12": "vitamin_b12",
        "cobalamin": "vitamin_b12",
    }
    
    for key, value in normalizations.items():
        if key in name:
            return value
    return name.replace(" ", "_")

def normalize_bill_item(name: str) -> str:
    """Normalize bill item names for comparison."""
    name = name.lower().strip()
    normalizations = {
        "magnetic resonance imaging": "mri",
        "computed tomography": "ct_scan",
        "ct scan": "ct_scan",
        "x-ray": "x_ray",
        "xray": "x_ray",
        "electrocardiogram": "ecg",
        "echocardiogram": "echo",
        "2d echo": "echo",
        "complete blood count": "cbc",
        "intensive care unit": "icu_day",
        "icu charges": "icu_day",
        "general ward": "room_general",
        "private room": "room_private",
        "single room": "room_private",
        "consultation fee": "consultation",
        "doctor fee": "consultation",
        "surgical gloves": "gloves",
        "disposable syringe": "syringe",
        "iv infusion set": "iv_set",
        "foley catheter": "catheter",
        "urinary catheter": "catheter",
        "nursing charges": "nursing",
    }
    
    for key, value in normalizations.items():
        if key in name:
            return value
    return name.replace(" ", "_")

def generate_document_id(filename: str, content: str) -> str:
    """Generate unique document ID."""
    hash_input = f"{filename}_{content[:100]}_{datetime.now().isoformat()}"
    return hashlib.md5(hash_input.encode()).hexdigest()[:12]

def format_currency(amount: Union[int, float, str]) -> str:
    """Format amount as Indian currency."""
    try:
        amount = float(str(amount).replace(",", "").replace("₹", "").strip())
        return f"₹{amount:,.2f}"
    except (ValueError, TypeError):
        return str(amount)

def extract_amount(text: str) -> Optional[float]:
    """Extract monetary amount from text."""
    # Remove currency symbols and extract number
    text = text.replace("₹", "").replace("Rs", "").replace("Rs.", "").replace(",", "")
    numbers = re.findall(r'[-+]?\d*\.?\d+', text)
    if numbers:
        return float(numbers[0])
    return None

def truncate_text(text: str, max_length: int = 200) -> str:
    """Truncate text with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def get_file_extension(filename: str) -> str:
    """Get file extension in lowercase."""
    return filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''

def is_valid_file_type(filename: str) -> bool:
    """Check if file type is supported."""
    valid_extensions = {'pdf', 'png', 'jpg', 'jpeg', 'tiff', 'bmp'}
    return get_file_extension(filename) in valid_extensions

def format_date(date_obj: datetime) -> str:
    """Format datetime for display."""
    return date_obj.strftime("%d %b %Y, %I:%M %p")

def get_time_ago(date_obj: datetime) -> str:
    """Get human-readable time ago string."""
    now = datetime.now()
    diff = now - date_obj
    
    if diff.days > 365:
        years = diff.days // 365
        return f"{years} year{'s' if years > 1 else ''} ago"
    elif diff.days > 30:
        months = diff.days // 30
        return f"{months} month{'s' if months > 1 else ''} ago"
    elif diff.days > 0:
        return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return "Just now"

def chunk_list(lst: List, chunk_size: int) -> List[List]:
    """Split a list into chunks."""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """Merge two dictionaries recursively."""
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result

def extract_email(text: str) -> Optional[str]:
    """Extract email address from text."""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(email_pattern, text)
    return match.group() if match else None

def extract_phone(text: str) -> Optional[str]:
    """Extract phone number from text."""
    phone_pattern = r'(?:\+91[\-\s]?)?[6-9]\d{9}'
    match = re.search(phone_pattern, text)
    return match.group() if match else None

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage."""
    # Remove or replace unsafe characters
    safe_name = re.sub(r'[^\w\s\-\.]', '', filename)
    safe_name = re.sub(r'\s+', '_', safe_name)
    return safe_name[:100]  # Limit length

def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """Calculate percentage change between two values."""
    if old_value == 0:
        return 0
    return ((new_value - old_value) / old_value) * 100
