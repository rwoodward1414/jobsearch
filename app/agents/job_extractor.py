import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from base import ClaudeAgent
from schema.job import Job

# Web fetch tool from Anthropic API
WEB_FETCH_TOOL = {
  "type": "web_fetch_20260209",
  "name": "web_fetch",
}

# Job extractor agent
# Extracts information from a job listing and returns a JSON object containing the information
job_extractor = ClaudeAgent(
  agent_name="job-extractor",
  system_prompt=(
    "You extract structured job posting information from a web page. "
    "Fetch the given URL and pull out the job title, company, seniority level, "
    "required skills, preferred skills, responsibilities, and relevant keywords."
  ),
  # Sonnet used over haiku as haiku can not use web fetch tool
  model="claude-sonnet-5",
)


async def extract_job(url: str) -> Job:
  return await job_extractor.call(
    f"Extract the job posting details from this URL: {url}",
    output_format=Job,
    tools=[WEB_FETCH_TOOL],
  )
