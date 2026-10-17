import json
from typing import AsyncGenerator
from backend.llm.chat import completion_with_backoff
from backend.tools.dispatch import dispatch_tool
from backend.tools.schemas import TOOL_DEFINITIONS

async def run_agent_loop(
    user_query: str,
    system_prompt: str,
    tools: list = TOOL_DEFINITIONS,
    max_steps: int = 6
) -> AsyncGenerator[dict, None]:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ]

    for step in range(max_steps):
        try:
            response = completion_with_backoff(messages=messages, tools=tools)
        except Exception as err:
            yield {
                "event": "trace",
                "data": {"step": "error", "error": f"LLM Call Failed: {str(err)}"}
            }
            yield {
                "event": "token",
                "data": {"content": f"Sorry, encountered an error communicating with the model: {str(err)}"}
            }
            yield {"event": "done", "data": {"done": True}}
            return

        message = response.choices[0].message
        
        # If model decides to call tools
        if message.tool_calls:
            # Append assistant message with tool calls
            messages.append({
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    } for tc in message.tool_calls
                ]
            })

            for tc in message.tool_calls:
                fn_name = tc.function.name
                try:
                    fn_args = json.loads(tc.function.arguments) if isinstance(tc.function.arguments, str) else tc.function.arguments
                except Exception:
                    fn_args = {}

                # Emit trace step to frontend
                yield {
                    "event": "trace",
                    "data": {
                        "step": "tool_call",
                        "tool": fn_name,
                        "args": fn_args
                    }
                }

                # Execute tool
                result = dispatch_tool(fn_name, fn_args)

                yield {
                    "event": "trace",
                    "data": {
                        "step": "tool_result",
                        "tool": fn_name,
                        "result": result
                    }
                }

                # Append tool response
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": json.dumps(result)
                })

        else:
            # Final text response
            final_content = message.content or ""
            yield {
                "event": "token",
                "data": {"content": final_content}
            }
            yield {"event": "done", "data": {"done": True}}
            return

    yield {
        "event": "token",
        "data": {"content": "Agent reached maximum tool invocation depth."}
    }
    yield {"event": "done", "data": {"done": True}}
