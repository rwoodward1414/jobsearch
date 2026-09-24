from agents.base import llamaAgent
from schema.critique import Critique

adversary = llamaAgent(
    system_prompt=(
        "You review resumes and cover letters, looking for AI generated text,"
        "generic filler phrases, keyword stuffing, tone inconsistency, and overuse of buzzwords."
        "Provide feedback on the given text and flag if more edits need to be made."
        ),
    )


def review(draft: str)-> Critique:
    response = adversary.call(draft, output_format=Critique)
    return response
