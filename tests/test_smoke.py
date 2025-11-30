import os
import sys

# Add the src directory to the Python path so we can import fc26_bot
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
SRC_PATH = os.path.join(ROOT, "src")
sys.path.insert(0, SRC_PATH)

import fc26_bot  # noqa: E402


def test_answer_question_runs():
    """
    Simple smoke test: ensure the chatbot can answer a basic question
    using the FC26 dataset without crashing.
    """
    reply = fc26_bot.answer_question("What player is the best?")
    assert isinstance(reply, str)
    assert len(reply) > 0
