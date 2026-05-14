"""
MedIntel AI - RAG (Retrieval Augmented Generation) Engine
"""
from typing import Dict, List, Tuple, Optional
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from modules.vector_store import search_similar_chunks, check_vector_store_available
from modules.llm_client import call_llm, check_llm_available
from utils.prompts import RAG_QA_PROMPT, SYSTEM_PROMPT
from utils.helpers import calculate_confidence, truncate_text
from utils.safety import check_for_emergency, get_emergency_response, add_safety_note


def retrieve_context(query: str, top_k: int = 5) -> Tuple[str, List[Dict], List[float]]:
    """
    Retrieve relevant context for a query.
    
    Args:
        query: User query
        top_k: Number of chunks to retrieve
        
    Returns:
        Tuple of (combined_context, source_chunks, scores)
    """
    if not check_vector_store_available():
        return "", [], []
    
    # Search for similar chunks
    results = search_similar_chunks(query, top_k)
    
    if not results:
        return "", [], []
    
    # Extract context and metadata
    context_parts = []
    source_chunks = []
    scores = []
    
    for chunk, score in results:
        context_parts.append(chunk['text'])
        source_chunks.append({
            'text': chunk['text'],
            'document_name': chunk.get('document_name', 'Unknown'),
            'document_type': chunk.get('document_type', 'Unknown'),
            'score': score
        })
        scores.append(score)
    
    combined_context = "\n\n---\n\n".join(context_parts)
    
    return combined_context, source_chunks, scores


def generate_rag_answer(query: str, context: str, sources: List[Dict]) -> str:
    """
    Generate answer using RAG.
    
    Args:
        query: User query
        context: Retrieved context
        sources: Source information
        
    Returns:
        Generated answer
    """
    if not check_llm_available():
        return "[Error: No LLM API configured. Please add API keys to .env file.]"
    
    if not context:
        return """**Answer:** I could not find relevant information in the uploaded documents to answer your question.

**Evidence:** No matching content found.

**Source:** N/A

**Confidence:** Low

**Suggested Next Step:** Please upload relevant documents or rephrase your question.

**Safety Note:** For medical questions, always consult with a qualified healthcare provider."""
    
    # Format the prompt
    prompt = RAG_QA_PROMPT.format(
        context=context,
        question=query
    )
    
    # Call LLM
    response = call_llm(prompt, SYSTEM_PROMPT)
    
    return response


def answer_question(query: str, top_k: int = 5) -> Dict:
    """
    Complete RAG pipeline to answer a question.
    
    Args:
        query: User query
        top_k: Number of chunks to retrieve
        
    Returns:
        Dictionary with answer, sources, confidence, etc.
    """
    result = {
        'query': query,
        'answer': '',
        'sources': [],
        'confidence': 'Low',
        'context_used': '',
        'is_emergency': False,
        'error': None
    }
    
    # Check for emergency keywords
    if check_for_emergency(query):
        result['is_emergency'] = True
        result['answer'] = get_emergency_response()
        result['confidence'] = 'High'
        return result
    
    # Check if services are available
    if not check_vector_store_available():
        result['error'] = "Vector store not available. Please check installation."
        result['answer'] = "[Error: Vector search not available]"
        return result
    
    if not check_llm_available():
        result['error'] = "LLM not available. Please configure API keys in .env file."
        result['answer'] = "[Error: No LLM API configured]"
        return result
    
    # Retrieve context
    context, sources, scores = retrieve_context(query, top_k)
    result['context_used'] = context
    result['sources'] = sources
    
    # Calculate confidence
    result['confidence'] = calculate_confidence(scores)
    
    # Generate answer
    answer = generate_rag_answer(query, context, sources)
    result['answer'] = answer
    
    return result


def get_suggested_questions(document_type: str = None) -> List[str]:
    """
    Get suggested questions based on document type.
    
    Args:
        document_type: Type of document
        
    Returns:
        List of suggested questions
    """
    general_questions = [
        "What documents have I uploaded?",
        "Summarize my health records.",
        "What are the key findings in my documents?"
    ]
    
    type_specific = {
        'Prescription': [
            "What medicines were prescribed to me?",
            "What are the dosages of my medications?",
            "How should I take my medicines?",
            "Are there any special instructions?"
        ],
        'Lab Report': [
            "What were my lab test results?",
            "Are any of my values abnormal?",
            "What does my HbA1c level indicate?",
            "How are my cholesterol levels?"
        ],
        'Discharge Summary': [
            "What was I diagnosed with?",
            "What treatment did I receive?",
            "What are my follow-up instructions?",
            "What medicines should I continue?"
        ],
        'Insurance Policy': [
            "What is my coverage amount?",
            "What are the waiting periods?",
            "What conditions are excluded?",
            "Is there a room rent cap?"
        ],
        'Hospital Bill': [
            "What is the total bill amount?",
            "What are the major charges?",
            "Are there any unusual charges?",
            "What diagnostic tests were billed?"
        ]
    }
    
    if document_type and document_type in type_specific:
        return type_specific[document_type] + general_questions[:2]
    
    return general_questions


def search_medical_memory(query: str) -> List[Dict]:
    """
    Search medical memory for relevant information.
    
    Args:
        query: Search query
        
    Returns:
        List of relevant chunks with metadata
    """
    results = search_similar_chunks(query, top_k=10)
    
    formatted_results = []
    for chunk, score in results:
        formatted_results.append({
            'content': truncate_text(chunk['text'], 300),
            'full_text': chunk['text'],
            'document': chunk.get('document_name', 'Unknown'),
            'type': chunk.get('document_type', 'Unknown'),
            'relevance': f"{score*100:.1f}%"
        })
    
    return formatted_results


def get_document_summary(document_name: str) -> str:
    """
    Get AI summary of a specific document.
    
    Args:
        document_name: Name of the document
        
    Returns:
        Summary text
    """
    # Search for all chunks from this document
    query = f"Summary of {document_name}"
    results = search_similar_chunks(query, top_k=20)
    
    # Filter for this document
    doc_chunks = [
        chunk for chunk, score in results 
        if chunk.get('document_name') == document_name
    ]
    
    if not doc_chunks:
        return f"No content found for document: {document_name}"
    
    # Combine chunks for summary
    content = "\n\n".join([c['text'] for c in doc_chunks[:10]])
    
    prompt = f"""Provide a brief summary of this medical document:

{content}

Summarize:
1. Document type
2. Key information
3. Important dates
4. Key findings or recommendations"""
    
    return call_llm(prompt)


def check_rag_ready() -> Dict:
    """Check if RAG system is ready."""
    from modules.vector_store import get_index_stats
    
    stats = get_index_stats()
    
    return {
        'vector_store_available': check_vector_store_available(),
        'llm_available': check_llm_available(),
        'total_chunks': stats.get('total_chunks', 0),
        'ready': check_vector_store_available() and check_llm_available() and stats.get('total_chunks', 0) > 0
    }
