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
    tools: Dict = None
  ):
    self.system_prompt = system_prompt
    self.model = model
    self.tools = tools

  # Calls the API
  async def call(
    self,
    content: str,
    format: Type[schema] = None,
  ):
    # Optional tool calling and output formating
    kwargs = {}
    if self.tools:
      kwargs["tools"] = list(self.tools)
    if format:
      kwargs["format"] = format.model_json_schema()

    messages=[
      {
        "role": "system",
        "content": self.system_prompt
      },
      {
        "role": "user",
        "content": content
      }
    ],

    response = await chat(
      model=self.model,
      messages=messages,
      **kwargs,
    )
    if response.message.tool_calls:
      self.tool_calling(messages, response)
    else:
      return response.message.content

  # Handles tool calling
  async def tool_calling(self, messages: Dict, response: Dict):
    messages.append(response.message)
    for tool_call in response.message.tool_calls:
      if tool_call.function.name in self.tools:
        result = self.tools[tool_call.function.name](**tool_call.function.arguments)
        messages.append({'role': 'tool', 'tool_name': tool_call.function.name, 'content': str(result)})

    final_response = await chat(
      model=self.model,
      messages=messages
    )

    return final_response.message.content