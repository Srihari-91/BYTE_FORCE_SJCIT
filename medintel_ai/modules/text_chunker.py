"""
MedIntel AI - Text Chunking for Embeddings
"""
from typing import List, Dict
import re
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_text(text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
    """
    Split text into overlapping chunks for embedding.
    
    Args:
        text: Text to chunk
        chunk_size: Maximum chunk size in characters
        overlap: Overlap between chunks
        
    Returns:
        List of text chunks
    """
    if chunk_size is None:
        chunk_size = CHUNK_SIZE
    if overlap is None:
        overlap = CHUNK_OVERLAP
    
    if not text or len(text) < chunk_size:
        return [text] if text else []
    
    # First, try to split by paragraphs/sections
    paragraphs = re.split(r'\n\n+', text)
    
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        
        # If paragraph alone is larger than chunk_size, split it further
        if len(para) > chunk_size:
            # Split by sentences
            sentences = re.split(r'(?<=[.!?])\s+', para)
            for sentence in sentences:
                if len(current_chunk) + len(sentence) + 1 <= chunk_size:
                    current_chunk += (" " if current_chunk else "") + sentence
                else:
                    if current_chunk:
                        chunks.append(current_chunk)
                    # If single sentence is too long, split by words
                    if len(sentence) > chunk_size:
                        words = sentence.split()
                        current_chunk = ""
                        for word in words:
                            if len(current_chunk) + len(word) + 1 <= chunk_size:
                                current_chunk += (" " if current_chunk else "") + word
                            else:
                                if current_chunk:
                                    chunks.append(current_chunk)
                                current_chunk = word
                    else:
                        current_chunk = sentence
        else:
            # Paragraph fits, try to add to current chunk
            if len(current_chunk) + len(para) + 2 <= chunk_size:
                current_chunk += ("\n\n" if current_chunk else "") + para
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = para
    
    # Don't forget the last chunk
    if current_chunk:
        chunks.append(current_chunk)
    
    # Add overlap
    if overlap > 0 and len(chunks) > 1:
        overlapped_chunks = []
        for i, chunk in enumerate(chunks):
            if i > 0:
                # Get last part of previous chunk as overlap
                prev_chunk = chunks[i-1]
                overlap_text = prev_chunk[-overlap:] if len(prev_chunk) > overlap else prev_chunk
                # Find a good break point (space)
                space_idx = overlap_text.find(' ')
                if space_idx > 0:
                    overlap_text = overlap_text[space_idx+1:]
                chunk = overlap_text + " " + chunk
            overlapped_chunks.append(chunk)
        chunks = overlapped_chunks
    
    return chunks


def chunk_text_with_metadata(text: str, document_name: str, document_type: str,
                            chunk_size: int = None, overlap: int = None) -> List[Dict]:
    """
    Chunk text and attach metadata to each chunk.
    
    Args:
        text: Text to chunk
        document_name: Name of source document
        document_type: Type of document
        chunk_size: Maximum chunk size
        overlap: Overlap between chunks
        
    Returns:
        List of chunk dictionaries with metadata
    """
    raw_chunks = chunk_text(text, chunk_size, overlap)
    
    chunks_with_metadata = []
    for i, chunk_text in enumerate(raw_chunks):
        chunk_data = {
            'text': chunk_text,
            'index': i,
            'document_name': document_name,
            'document_type': document_type,
            'chunk_size': len(chunk_text),
            'word_count': len(chunk_text.split()),
        }
        chunks_with_metadata.append(chunk_data)
    
    return chunks_with_metadata


def chunk_by_section(text: str, section_headers: List[str] = None) -> Dict[str, str]:
    """
    Chunk text by sections/headers.
    
    Args:
        text: Text to chunk
        section_headers: List of section header patterns to look for
        
    Returns:
        Dictionary mapping section names to content
    """
    if section_headers is None:
        # Common medical document sections
        section_headers = [
            r'chief complaint',
            r'history of present illness',
            r'past medical history',
            r'medications?',
            r'allergies',
            r'physical examination',
            r'diagnosis',
            r'treatment',
            r'investigations?',
            r'advice',
            r'follow[- ]?up',
            r'discharge summary',
            r'lab results?',
            r'test results?',
        ]
    
    sections = {}
    current_section = "General"
    current_content = []
    
    lines = text.split('\n')
    
    for line in lines:
        line_lower = line.lower().strip()
        
        # Check if line is a section header
        is_header = False
        for header_pattern in section_headers:
            if re.search(header_pattern, line_lower):
                # Save previous section
                if current_content:
                    sections[current_section] = '\n'.join(current_content)
                # Start new section
                current_section = line.strip().rstrip(':')
                current_content = []
                is_header = True
                break
        
        if not is_header and line.strip():
            current_content.append(line)
    
    # Save last section
    if current_content:
        sections[current_section] = '\n'.join(current_content)
    
    return sections


def get_chunk_context(chunks: List[Dict], chunk_index: int, context_size: int = 1) -> str:
    """
    Get surrounding context for a chunk.
    
    Args:
        chunks: List of chunk dictionaries
        chunk_index: Index of target chunk
        context_size: Number of chunks before/after to include
        
    Returns:
        Combined text with context
    """
    start_idx = max(0, chunk_index - context_size)
    end_idx = min(len(chunks), chunk_index + context_size + 1)
    
    context_chunks = chunks[start_idx:end_idx]
    return "\n\n".join([c['text'] for c in context_chunks])


def merge_small_chunks(chunks: List[str], min_size: int = 100) -> List[str]:
    """
    Merge chunks that are too small.
    
    Args:
        chunks: List of text chunks
        min_size: Minimum chunk size
        
    Returns:
        List of merged chunks
    """
    if not chunks:
        return chunks
    
    merged = []
    current = ""
    
    for chunk in chunks:
        if len(chunk) < min_size:
            current += (" " if current else "") + chunk
        else:
            if current:
                if len(current) < min_size:
                    current += " " + chunk
                    merged.append(current)
                    current = ""
                else:
                    merged.append(current)
                    current = ""
                    merged.append(chunk)
            else:
                merged.append(chunk)
    
    if current:
        if merged and len(current) < min_size:
            merged[-1] += " " + current
        else:
            merged.append(current)
    
    return merged


def estimate_token_count(text: str) -> int:
    """
    Estimate token count for a text (rough approximation).
    
    Args:
        text: Text to estimate
        
    Returns:
        Estimated token count
    """
    # Rough estimate: ~4 characters per token for English
    return len(text) // 4


def chunk_for_llm(text: str, max_tokens: int = 3000) -> List[str]:
    """
    Chunk text to fit within LLM context limits.
    
    Args:
        text: Text to chunk
        max_tokens: Maximum tokens per chunk
        
    Returns:
        List of chunks
    """
    # Convert token limit to character limit (rough estimate)
    max_chars = max_tokens * 4
    return chunk_text(text, chunk_size=max_chars, overlap=200)
