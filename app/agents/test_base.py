import asyncio

from base import ClaudeAgent
from job_extractor import extract_job
from schema.test import Test

async def main():
  agent = ClaudeAgent(
    agent_name="name-extractor",
    system_prompt="Extract the person's first and last name from the given text.",
  )
  result = await agent.call(
    "Hi, my name is Ada Lovelace and I'm reaching out about the job posting.",
    output_format=Test,
  )
  print(result)
  assert result.first_name == "Ada"
  assert result.last_name == "Lovelace"


if __name__ == "__main__":
  asyncio.run(main())
