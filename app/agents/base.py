from typing import Type, TypeVar
from dotenv import load_dotenv
from pydantic import BaseModel
import anthropic
import os

# Login to claude API
load_dotenv()
API_KEY = os.getenv("ANTHROPIC-API")
client = anthropic.AsyncAnthropic(api_key=API_KEY)

schema = TypeVar("schema", bound=BaseModel)

# Base agent class which agents inherit from
class ClaudeAgent:
  def __init__(
    self,
    agent_name: str,
    system_prompt: str,
    model: str = "claude-haiku-4-5",
  ):
    self.agent_name = agent_name
    self.system_prompt = system_prompt
    self.model = model

  # Calls the messaging API
  async def call(
    self,
    user_content: str,
    output_format: Type[schema] = None,
    tools: list = None,
    max_tokens: int = 1000,
  ):
    # Allows for calls to optionally use tools
    kwargs = {}
    if tools:
      kwargs["tools"] = tools

    # When using pydantic models for output validation, need to call messages.parse instead of create
    if output_format:
      response = await client.messages.parse(
        model=self.model,
        max_tokens=max_tokens,
        system=self.system_prompt,
        messages=[{
          "role": "user",
          "content": user_content
        }],
        output_format=output_format,
        **kwargs,
      )
      return response.parsed_output

    response = await client.messages.create(
      model=self.model,
      max_tokens=max_tokens,
      system=self.system_prompt,
      messages=[{
        "role": "user",
        "content": user_content
      }],
      **kwargs,
    )
    return response.content[0].text

  
      