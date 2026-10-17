import time
from backend.llm.client import get_llm_client
from backend.tools.schemas import TOOL_DEFINITIONS

def completion_with_backoff(messages: list, tools: list = None, max_retries: int = 3, temperature: float = 0.2):
    client, model = get_llm_client()
    
    kwargs = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }
    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"

    last_error = None
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(**kwargs)
            return response
        except Exception as e:
            last_error = e
            time.sleep(1.5 * (attempt + 1))

    raise RuntimeError(f"LLM request failed after {max_retries} attempts: {last_error}")
