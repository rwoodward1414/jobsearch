from typing import Type, TypeVar, Dict
from dotenv import load_dotenv
from pydantic import BaseModel
from ollama import chat
#import os

# Login to claude API
#load_dotenv()
#API_KEY = os.getenv("ANTHROPIC-API")
#client = anthropic.AsyncAnthropic(api_key=API_KEY)

schema = TypeVar("schema", bound=BaseModel)

# Base agent class which agents inherit from
class llamaAgent:
  def __init__(
    self,
    system_prompt: str,
    model: str = "llama3.1",
  ):
    self.system_prompt = system_prompt
    self.model = model

  # Calls the API
  async def call(
    self,
    content: str,
    format: Type[schema] = None,
    tools: Dict = None
  ):
    kwargs = {}
    if format:
      kwargs["format"] = format

    messages = [
      {
        "role": "system",
        "content": self.system_prompt
      },
      {
        "role": "user",
        "content": content
      }
    ]

    # Optional tool calling
    if tools:
      # Loop calling tools until the model stops requesting them
      while True:
        response = await chat(
          model=self.model,
          messages=messages,
          tools=list(tools)
        )
        messages.append(response.message)

        if not response.message.tool_calls:
          break

        for tool_call in response.message.tool_calls:
          if tool_call.function.name in tools:
            result = tools[tool_call.function.name](**tool_call.function.arguments)
            messages.append({'role': 'tool', 'tool_name': tool_call.function.name, 'content': str(result)})

    # Output formating, if needed, is applied on the final call, once tool calling is done
    response = await chat(
      model=self.model,
      messages=messages,
      **kwargs,        
    )

    return response.message.content