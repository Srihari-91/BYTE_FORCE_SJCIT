"""
MedIntel AI - SQLite Database Operations
"""
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import json
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.config import DATABASE_PATH

def get_connection():
    """Get database connection."""
    conn = sqlite3.connect(str(DATABASE_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database tables."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Documents table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doc_id TEXT UNIQUE,
        filename TEXT NOT NULL,
        document_type TEXT,
        file_path TEXT,
        extracted_text_path TEXT,
        upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        text_length INTEGER,
        ocr_used BOOLEAN DEFAULT FALSE,
        processing_status TEXT DEFAULT 'pending'
    )
    """)
    
    # Chunks table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chunks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER,
        chunk_text TEXT,
        chunk_index INTEGER,
        embedding_id TEXT,
        FOREIGN KEY (document_id) REFERENCES documents(id)
    )
    """)
    
    # Extracted entities table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS extracted_entities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER,
        entity_type TEXT,
        entity_name TEXT,
        entity_value TEXT,
        metadata TEXT,
        source_snippet TEXT,
        extraction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (document_id) REFERENCES documents(id)
    )
    """)
    
    # Lab values table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lab_values (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER,
        test_name TEXT,
        normalized_name TEXT,
        value REAL,
        unit TEXT,
        reference_range TEXT,
        status TEXT,
        report_date DATE,
        source_snippet TEXT,
        FOREIGN KEY (document_id) REFERENCES documents(id)
    )
    """)
    
    # Insurance risks table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS insurance_risks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER,
        clause_type TEXT,
        clause_text TEXT,
        simple_meaning TEXT,
        financial_risk TEXT,
        severity TEXT,
        question_to_ask TEXT,
        FOREIGN KEY (document_id) REFERENCES documents(id)
    )
    """)
    
    # Bill risks table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bill_risks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER,
        item_name TEXT,
        amount REAL,
        risk_type TEXT,
        reason TEXT,
        severity TEXT,
        suggested_question TEXT,
        FOREIGN KEY (document_id) REFERENCES documents(id)
    )
    """)
    
    # Bill items table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bill_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER,
        item_name TEXT,
        category TEXT,
        quantity INTEGER,
        unit_price REAL,
        total_amount REAL,
        date TEXT,
        source_snippet TEXT,
        FOREIGN KEY (document_id) REFERENCES documents(id)
    )
    """)
    
    # Chat history table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT,
        sources TEXT,
        confidence TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Medicines table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER,
        name TEXT,
        dose TEXT,
        frequency TEXT,
        duration TEXT,
        instructions TEXT,
        source_snippet TEXT,
        FOREIGN KEY (document_id) REFERENCES documents(id)
    )
    """)
    
    conn.commit()
    conn.close()

# Document operations
def insert_document(doc_id: str, filename: str, document_type: str, 
                   file_path: str, extracted_text_path: str, 
                   text_length: int, ocr_used: bool) -> int:
    """Insert a new document record."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO documents (doc_id, filename, document_type, file_path, 
                          extracted_text_path, text_length, ocr_used, processing_status)
    VALUES (?, ?, ?, ?, ?, ?, ?, 'processed')
    """, (doc_id, filename, document_type, file_path, extracted_text_path, 
          text_length, ocr_used))
    doc_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return doc_id

def get_all_documents() -> List[Dict]:
    """Get all documents."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM documents ORDER BY upload_time DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_document_by_id(doc_id: int) -> Optional[Dict]:
    """Get document by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def delete_document(doc_id: int):
    """Delete document and related data."""
    conn = get_connection()
    cursor = conn.cursor()
    # Delete related data
    cursor.execute("DELETE FROM chunks WHERE document_id = ?", (doc_id,))
    cursor.execute("DELETE FROM extracted_entities WHERE document_id = ?", (doc_id,))
    cursor.execute("DELETE FROM lab_values WHERE document_id = ?", (doc_id,))
    cursor.execute("DELETE FROM insurance_risks WHERE document_id = ?", (doc_id,))
    cursor.execute("DELETE FROM bill_risks WHERE document_id = ?", (doc_id,))
    cursor.execute("DELETE FROM bill_items WHERE document_id = ?", (doc_id,))
    cursor.execute("DELETE FROM medicines WHERE document_id = ?", (doc_id,))
    cursor.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
    conn.commit()
    conn.close()

# Chunk operations
def insert_chunks(document_id: int, chunks: List[Dict]):
    """Insert document chunks."""
    conn = get_connection()
    cursor = conn.cursor()
    for i, chunk in enumerate(chunks):
        cursor.execute("""
        INSERT INTO chunks (document_id, chunk_text, chunk_index, embedding_id)
        VALUES (?, ?, ?, ?)
        """, (document_id, chunk['text'], i, chunk.get('embedding_id')))
    conn.commit()
    conn.close()

# Entity operations
def insert_entity(document_id: int, entity_type: str, entity_name: str,
                 entity_value: str, metadata: Dict = None, source_snippet: str = None):
    """Insert extracted entity."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO extracted_entities (document_id, entity_type, entity_name, 
                                   entity_value, metadata, source_snippet)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (document_id, entity_type, entity_name, entity_value, 
          json.dumps(metadata) if metadata else None, source_snippet))
    conn.commit()
    conn.close()

def get_entities_by_type(entity_type: str) -> List[Dict]:
    """Get all entities of a specific type."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT e.*, d.filename FROM extracted_entities e
    JOIN documents d ON e.document_id = d.id
    WHERE e.entity_type = ?
    ORDER BY e.extraction_time DESC
    """, (entity_type,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Lab values operations
def insert_lab_value(document_id: int, test_name: str, normalized_name: str,
                    value: float, unit: str, reference_range: str, 
                    status: str, report_date: str, source_snippet: str):
    """Insert lab value."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO lab_values (document_id, test_name, normalized_name, value, 
                           unit, reference_range, status, report_date, source_snippet)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (document_id, test_name, normalized_name, value, unit, 
          reference_range, status, report_date, source_snippet))
    conn.commit()
    conn.close()

def get_all_lab_values() -> List[Dict]:
    """Get all lab values."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT l.*, d.filename FROM lab_values l
    JOIN documents d ON l.document_id = d.id
    ORDER BY l.report_date DESC, l.test_name
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_lab_values_by_test(test_name: str) -> List[Dict]:
    """Get lab values for a specific test."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM lab_values 
    WHERE normalized_name = ?
    ORDER BY report_date
    """, (test_name,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Insurance risks operations
def insert_insurance_risk(document_id: int, clause_type: str, clause_text: str,
                         simple_meaning: str, financial_risk: str, 
                         severity: str, question_to_ask: str):
    """Insert insurance risk."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO insurance_risks (document_id, clause_type, clause_text, 
                                simple_meaning, financial_risk, severity, question_to_ask)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (document_id, clause_type, clause_text, simple_meaning, 
          financial_risk, severity, question_to_ask))
    conn.commit()
    conn.close()

def get_all_insurance_risks() -> List[Dict]:
    """Get all insurance risks."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT i.*, d.filename FROM insurance_risks i
    JOIN documents d ON i.document_id = d.id
    ORDER BY 
        CASE i.severity 
            WHEN 'High' THEN 1 
            WHEN 'Medium' THEN 2 
            ELSE 3 
        END
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Bill operations
def insert_bill_item(document_id: int, item_name: str, category: str,
                    quantity: int, unit_price: float, total_amount: float,
                    date: str, source_snippet: str):
    """Insert bill item."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO bill_items (document_id, item_name, category, quantity, 
                           unit_price, total_amount, date, source_snippet)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (document_id, item_name, category, quantity, unit_price, 
          total_amount, date, source_snippet))
    conn.commit()
    conn.close()

def insert_bill_risk(document_id: int, item_name: str, amount: float,
                    risk_type: str, reason: str, severity: str, 
                    suggested_question: str):
    """Insert bill risk."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO bill_risks (document_id, item_name, amount, risk_type, 
                           reason, severity, suggested_question)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (document_id, item_name, amount, risk_type, reason, 
          severity, suggested_question))
    conn.commit()
    conn.close()

def get_all_bill_risks() -> List[Dict]:
    """Get all bill risks."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT b.*, d.filename FROM bill_risks b
    JOIN documents d ON b.document_id = d.id
    ORDER BY 
        CASE b.severity 
            WHEN 'High' THEN 1 
            WHEN 'Medium' THEN 2 
            ELSE 3 
        END
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_all_bill_items() -> List[Dict]:
    """Get all bill items."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT b.*, d.filename FROM bill_items b
    JOIN documents d ON b.document_id = d.id
    ORDER BY b.document_id, b.id
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Medicines operations
def insert_medicine(document_id: int, name: str, dose: str, frequency: str,
                   duration: str, instructions: str, source_snippet: str):
    """Insert medicine."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO medicines (document_id, name, dose, frequency, duration, 
                          instructions, source_snippet)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (document_id, name, dose, frequency, duration, instructions, source_snippet))
    conn.commit()
    conn.close()

def get_all_medicines() -> List[Dict]:
    """Get all medicines."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT m.*, d.filename FROM medicines m
    JOIN documents d ON m.document_id = d.id
    ORDER BY m.name
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Chat history operations
def insert_chat(question: str, answer: str, sources: str, confidence: str):
    """Insert chat record."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO chat_history (question, answer, sources, confidence)
    VALUES (?, ?, ?, ?)
    """, (question, answer, sources, confidence))
    conn.commit()
    conn.close()

def get_chat_history(limit: int = 50) -> List[Dict]:
    """Get recent chat history."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM chat_history 
    ORDER BY timestamp DESC 
    LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Statistics
def get_statistics() -> Dict:
    """Get database statistics."""
    conn = get_connection()
    cursor = conn.cursor()
    
    stats = {}
    cursor.execute("SELECT COUNT(*) FROM documents")
    stats['total_documents'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM extracted_entities")
    stats['total_entities'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM lab_values")
    stats['total_lab_values'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM insurance_risks")
    stats['total_insurance_risks'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM bill_risks")
    stats['total_bill_risks'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM medicines")
    stats['total_medicines'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM chat_history")
    stats['total_chats'] = cursor.fetchone()[0]
    
    conn.close()
    return stats

# Initialize database on import
init_database()
