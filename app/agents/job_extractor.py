import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from agents.base import llamaAgent
from schema.job import Job
from tools.pagescrap import get_text

# Job extractor agent
# Extracts information from a job listing and returns a JSON object containing the information
job_extractor = llamaAgent(
  system_prompt=(
    "You extract structured job posting information from a web page. "
    "Fetch the given URL and pull out the job title, company, seniority level, "
    "required skills, preferred skills, responsibilities, and relevant keywords."
  ),
)


def extract_job(url: str) -> Job:
  return job_extractor.call(
    f"Extract the job posting details from this URL: {url}",
    output_format=Job,
    tools={'get_text': get_text,},
  )
