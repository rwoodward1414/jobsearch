from abc import ABC, abstractmethod

from agents.base import llamaAgent
from schema.job import Job
from schema.resume import Resume

# Shared draft + revise-on-feedback loop. Subclasses define write() and, if
# the output should be structured, output_format.
class BaseWriter(ABC):
  system_prompt: str = ""
  output_format = None

  def __init__(self, model: str = "llama3.2:1b"):
    self.agent = llamaAgent(system_prompt=self.system_prompt, model=model)
    self.draft = None

  @abstractmethod
  def write(self, *args, **kwargs):
    ...

  def revise(self, feedback: str):
    if self.draft is None:
      raise RuntimeError("write() must be called before revise()")

    draft_text = self.draft.model_dump_json() if self.output_format else self.draft

    self.draft = self.agent.call(
      f"Here is the current draft:\n{draft_text}\n\n"
      f"Feedback to address:\n{feedback}\n\n"
      "Revise the draft to address the feedback.",
      output_format=self.output_format,
    )
    return self.draft

  def get_draft(self):
    return self.draft

  def get_draft_text(self):
    draft_text = self.draft.model_dump_json() if self.output_format else self.draft
    return draft_text


class ResumeWriter(BaseWriter):
  system_prompt = (
    "You write resumes tailored to a specific job posting, using the "
    "candidate's master resume as a base. Return the resume as structured data matching "
    "the given schema. When given feedback on a draft, revise it to address "
    "the feedback while keeping everything else unchanged."
  )
  output_format = Resume

  def write(self, job: Job, background: Resume) -> Resume:
    self.draft = self.agent.call(
      f"Job information:\n{job.model_dump_json()}\n\n"
      f"Master resume:\n{background.model_dump_json()}",
      output_format=self.output_format,
    )
    return self.draft


class CoverLetterWriter(BaseWriter):
  system_prompt = (
    "You write cover letters tailored to a specific job posting, based on "
    "the candidate's resume and cover letter samples. When given feedback on a draft, revise it "
    "to address the feedback while keeping everything else unchanged."
  )

  def write(self, job: Job, background: Resume, samples: str) -> str:
    self.draft = self.agent.call(
      f"Job information:\n{job.model_dump_json()}\n\n"
      f"Resume:\n{background.model_dump_json()}\n\n"
      f"Cover letter samples:\n{samples}"
    )
    return self.draft
