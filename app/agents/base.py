from typing import Type, TypeVar, Dict
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
from ollama import chat, ResponseError
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
    model: str = "llama3.2:1b",
  ):
    self.system_prompt = system_prompt
    self.model = model

  # Calls the API
  def call(
    self,
    content: str,
    output_format: Type[schema] = None,
    tools: Dict = None
  ):
    kwargs = {}
    if output_format:
      kwargs["format"] = output_format.model_json_schema()

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
        try:
          response = chat(
            model=self.model,
            messages=messages,
            tools=list(tools)
          )
        except ResponseError as e:
          raise RuntimeError(f"Ollama chat request failed: {e}") from e

        messages.append(response.message)
        if not response.message.tool_calls:
          break

        for tool_call in response.message.tool_calls:
          if tool_call.function.name in tools:
            result = tools[tool_call.function.name](**tool_call.function.arguments)
            messages.append({'role': 'tool', 'tool_name': tool_call.function.name, 'content': str(result)})

    # Output formating, if needed, is applied on the final call, once tool calling is done
    try:
      response = chat(
        model=self.model,
        messages=messages,
        **kwargs,
      )
    except ResponseError as e:
      raise RuntimeError(f"Ollama chat request failed: {e}") from e

    if output_format:
      try:
        return output_format.model_validate_json(response.message.content)
      except ValidationError as e:
        raise RuntimeError(
          f"Model response did not match {output_format.__name__} schema: {response.message.content}"
        ) from e
    return response.message.content