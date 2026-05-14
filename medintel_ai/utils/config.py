"""
MedIntel AI - Configuration Management
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
EXTRACTED_DIR = DATA_DIR / "extracted_text"
VECTOR_DIR = DATA_DIR / "vector_store"
REPORTS_DIR = DATA_DIR / "reports"
DATABASE_PATH = DATA_DIR / "medintel.db"

# Create directories if they don't exist
for directory in [DATA_DIR, UPLOADS_DIR, EXTRACTED_DIR, VECTOR_DIR, REPORTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.1-70b-versatile")

# Embedding Configuration
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# Chunking Configuration
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 800))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 150))

# Application Settings
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", 50))

# Safety Settings
ENABLE_SAFETY_DISCLAIMERS = os.getenv("ENABLE_SAFETY_DISCLAIMERS", "true").lower() == "true"
EMERGENCY_DETECTION = os.getenv("EMERGENCY_DETECTION", "true").lower() == "true"

# Document Types
DOCUMENT_TYPES = [
    "Prescription",
    "Lab Report",
    "Discharge Summary",
    "Insurance Policy",
    "Claim Document",
    "Hospital Bill",
    "Medical Certificate",
    "Other"
]

# Lab Reference Ranges (India-specific)
LAB_REFERENCE_RANGES = {
    "hemoglobin": {"min": 12.0, "max": 17.5, "unit": "g/dL", "male_min": 13.5, "male_max": 17.5, "female_min": 12.0, "female_max": 15.5},
    "hba1c": {"min": 4.0, "max": 5.6, "unit": "%", "prediabetes": 5.7, "diabetes": 6.5},
    "fasting_glucose": {"min": 70, "max": 100, "unit": "mg/dL", "prediabetes": 126},
    "random_glucose": {"min": 70, "max": 140, "unit": "mg/dL"},
    "total_cholesterol": {"min": 0, "max": 200, "unit": "mg/dL", "borderline": 240},
    "ldl": {"min": 0, "max": 100, "unit": "mg/dL", "borderline": 130},
    "hdl": {"min": 40, "max": 60, "unit": "mg/dL"},
    "triglycerides": {"min": 0, "max": 150, "unit": "mg/dL", "borderline": 200},
    "creatinine": {"min": 0.7, "max": 1.3, "unit": "mg/dL"},
    "urea": {"min": 7, "max": 20, "unit": "mg/dL"},
    "sgpt": {"min": 7, "max": 56, "unit": "U/L"},
    "sgot": {"min": 10, "max": 40, "unit": "U/L"},
    "tsh": {"min": 0.4, "max": 4.0, "unit": "mIU/L"},
    "wbc": {"min": 4000, "max": 11000, "unit": "cells/mcL"},
    "platelets": {"min": 150000, "max": 400000, "unit": "cells/mcL"},
    "rbc": {"min": 4.5, "max": 5.5, "unit": "million/mcL"},
    "bilirubin": {"min": 0.1, "max": 1.2, "unit": "mg/dL"},
    "albumin": {"min": 3.5, "max": 5.0, "unit": "g/dL"},
    "uric_acid": {"min": 3.5, "max": 7.2, "unit": "mg/dL"},
    "vitamin_d": {"min": 30, "max": 100, "unit": "ng/mL"},
    "vitamin_b12": {"min": 200, "max": 900, "unit": "pg/mL"},
}

# Benchmark prices for bill analysis (INR - approximate ranges)
BILL_BENCHMARKS = {
    "mri": {"min": 5000, "max": 15000, "category": "diagnostic"},
    "ct_scan": {"min": 2000, "max": 10000, "category": "diagnostic"},
    "x_ray": {"min": 200, "max": 1500, "category": "diagnostic"},
    "ultrasound": {"min": 500, "max": 3000, "category": "diagnostic"},
    "ecg": {"min": 150, "max": 800, "category": "diagnostic"},
    "echo": {"min": 1000, "max": 4000, "category": "diagnostic"},
    "cbc": {"min": 200, "max": 800, "category": "diagnostic"},
    "blood_test": {"min": 100, "max": 500, "category": "diagnostic"},
    "urine_test": {"min": 100, "max": 400, "category": "diagnostic"},
    "consultation": {"min": 200, "max": 2000, "category": "consultation"},
    "icu_day": {"min": 5000, "max": 25000, "category": "room"},
    "room_general": {"min": 1000, "max": 5000, "category": "room"},
    "room_private": {"min": 3000, "max": 15000, "category": "room"},
    "gloves": {"min": 5, "max": 50, "category": "consumable"},
    "syringe": {"min": 5, "max": 30, "category": "consumable"},
    "iv_set": {"min": 50, "max": 200, "category": "consumable"},
    "catheter": {"min": 100, "max": 500, "category": "consumable"},
    "nursing": {"min": 500, "max": 2000, "category": "nursing"},
}

# Insurance clause types
INSURANCE_CLAUSE_TYPES = [
    "waiting_period",
    "room_rent_cap",
    "copay",
    "sublimit",
    "exclusion",
    "pre_existing_disease",
    "claim_condition",
    "network_hospital",
    "daycare_procedure",
    "maternity",
    "critical_illness",
    "other"
]

# Color scheme
COLORS = {
    "primary": "#0066CC",
    "secondary": "#00A8A8",
    "success": "#28A745",
    "warning": "#FFC107",
    "danger": "#DC3545",
    "info": "#17A2B8",
    "light": "#F8F9FA",
    "dark": "#343A40",
    "gradient_start": "#667eea",
    "gradient_end": "#764ba2",
}
