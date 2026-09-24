from agents.writter import BaseWriter
from agents.adversary import review
from schema.critique import Critique

MAX_RETRIES = 3

def review_writter_output(writter: BaseWriter):
    draft_text = writter.get_draft_text()

    # Run critque loop until agents agree or MAX_RETRIES
    for attempt in range(MAX_RETRIES):
        critque = review(draft_text)
        if not critque.flagged:
            return writter.get_draft()
        
        writter.revise(critque.issues)
        draft_text = writter.get_draft_text()

    return writter.get_draft()