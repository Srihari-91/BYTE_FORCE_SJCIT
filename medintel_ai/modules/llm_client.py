"""
MedIntel AI - LLM Client for AI Inference
"""
import json
from typing import Dict, Optional, Any
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.config import (
    LLM_PROVIDER, GROQ_API_KEY, OPENAI_API_KEY, 
    GOOGLE_API_KEY, LLM_MODEL
)
from utils.prompts import SYSTEM_PROMPT
from utils.helpers import safe_json_parse

# Check for API availability
GROQ_AVAILABLE = bool(GROQ_API_KEY)
OPENAI_AVAILABLE = bool(OPENAI_API_KEY)
GOOGLE_AVAILABLE = bool(GOOGLE_API_KEY)


def get_available_providers() -> list:
    """Get list of available LLM providers."""
    providers = []
    if GROQ_AVAILABLE:
        providers.append("groq")
    if OPENAI_AVAILABLE:
        providers.append("openai")
    if GOOGLE_AVAILABLE:
        providers.append("google")
    return providers


def call_groq(prompt: str, system_prompt: str = None, temperature: float = 0.3) -> str:
    """
    Call Groq API with Llama model.
    
    Args:
        prompt: User prompt
        system_prompt: System prompt
        temperature: Sampling temperature
        
    Returns:
        Model response text
    """
    if not GROQ_AVAILABLE:
        return "[Error: Groq API key not configured]"
    
    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=4096
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"[Groq Error: {str(e)}]"


def call_openai(prompt: str, system_prompt: str = None, temperature: float = 0.3) -> str:
    """
    Call OpenAI API.
    
    Args:
        prompt: User prompt
        system_prompt: System prompt
        temperature: Sampling temperature
        
    Returns:
        Model response text
    """
    if not OPENAI_AVAILABLE:
        return "[Error: OpenAI API key not configured]"
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=temperature,
            max_tokens=4096
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"[OpenAI Error: {str(e)}]"


def call_google(prompt: str, system_prompt: str = None, temperature: float = 0.3) -> str:
    """
    Call Google Gemini API.
    
    Args:
        prompt: User prompt
        system_prompt: System prompt
        temperature: Sampling temperature
        
    Returns:
        Model response text
    """
    if not GOOGLE_AVAILABLE:
        return "[Error: Google API key not configured]"
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=GOOGLE_API_KEY)
        
        model = genai.GenerativeModel('gemini-pro')
        
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=4096
            )
        )
        
        return response.text
    
    except Exception as e:
        return f"[Google Error: {str(e)}]"


def call_llm(prompt: str, system_prompt: str = None, 
             provider: str = None, temperature: float = 0.3) -> str:
    """
    Call LLM using configured or specified provider.
    
    Args:
        prompt: User prompt
        system_prompt: System prompt (defaults to MedIntel system prompt)
        provider: LLM provider to use
        temperature: Sampling temperature
        
    Returns:
        Model response text
    """
    if system_prompt is None:
        system_prompt = SYSTEM_PROMPT
    
    if provider is None:
        provider = LLM_PROVIDER
    
    # Try specified provider
    if provider == "groq" and GROQ_AVAILABLE:
        response = call_groq(prompt, system_prompt, temperature)
        if not response.startswith("[Groq Error"):
            return response
    
    if provider == "openai" and OPENAI_AVAILABLE:
        response = call_openai(prompt, system_prompt, temperature)
        if not response.startswith("[OpenAI Error"):
            return response
    
    if provider == "google" and GOOGLE_AVAILABLE:
        response = call_google(prompt, system_prompt, temperature)
        if not response.startswith("[Google Error"):
            return response
    
    # Fallback to any available provider
    if GROQ_AVAILABLE:
        return call_groq(prompt, system_prompt, temperature)
    if OPENAI_AVAILABLE:
        return call_openai(prompt, system_prompt, temperature)
    if GOOGLE_AVAILABLE:
        return call_google(prompt, system_prompt, temperature)
    
    return "[Error: No LLM API configured. Please add API keys to .env file.]"


def call_llm_json(prompt: str, system_prompt: str = None) -> Optional[Dict]:
    """
    Call LLM and parse JSON response.
    
    Args:
        prompt: User prompt (should request JSON output)
        system_prompt: System prompt
        
    Returns:
        Parsed JSON dictionary or None if parsing fails
    """
    response = call_llm(prompt, system_prompt, temperature=0.1)
    
    if response.startswith("[Error") or response.startswith("[Groq Error") or \
       response.startswith("[OpenAI Error") or response.startswith("[Google Error"):
        return None
    
    # Try to parse JSON from response
    parsed = safe_json_parse(response)
    
    if parsed is None:
        # Try to extract JSON from markdown code blocks
        import re
        json_match = re.search(r'```(?:json)?\s*(\{[\s\S]*?\})\s*```', response)
        if json_match:
            parsed = safe_json_parse(json_match.group(1))
    
    return parsed


def check_llm_available() -> bool:
    """Check if any LLM provider is available."""
    return GROQ_AVAILABLE or OPENAI_AVAILABLE or GOOGLE_AVAILABLE


def get_llm_status() -> Dict[str, bool]:
    """Get status of all LLM providers."""
    return {
        'groq': GROQ_AVAILABLE,
        'openai': OPENAI_AVAILABLE,
        'google': GOOGLE_AVAILABLE,
        'any_available': check_llm_available()
    }


def estimate_cost(prompt: str, response: str, provider: str = "groq") -> float:
    """
    Estimate API cost for a request.
    
    Args:
        prompt: Input prompt
        response: Output response
        provider: API provider
        
    Returns:
        Estimated cost in USD
    """
    # Rough token estimates
    input_tokens = len(prompt) // 4
    output_tokens = len(response) // 4
    
    # Approximate costs per 1M tokens
    costs = {
        'groq': {'input': 0.05, 'output': 0.10},  # Groq is very cheap
        'openai': {'input': 0.15, 'output': 0.60},  # GPT-4o-mini
        'google': {'input': 0.075, 'output': 0.30},  # Gemini Pro
    }
    
    if provider not in costs:
        return 0.0
    
    cost = (input_tokens * costs[provider]['input'] / 1_000_000 + 
            output_tokens * costs[provider]['output'] / 1_000_000)
    
    return cost
