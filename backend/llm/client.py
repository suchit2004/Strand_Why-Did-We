from openai import OpenAI
from backend.config import settings

def get_llm_client():
    provider = settings.LLM_PROVIDER.lower()
    
    if provider == "groq":
        return OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=settings.GROQ_API_KEY or "dummy_key_to_init"
        ), settings.GROQ_MODEL
        
    elif provider == "ollama":
        return OpenAI(
            base_url=settings.OLLAMA_BASE_URL,
            api_key="ollama"
        ), settings.OLLAMA_MODEL
        
    elif provider == "openai":
        return OpenAI(
            api_key=settings.OPENAI_API_KEY or "dummy_key_to_init"
        ), settings.OPENAI_MODEL
        
    else:
        # Default fallback to groq
        return OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=settings.GROQ_API_KEY or "dummy_key_to_init"
        ), settings.GROQ_MODEL
