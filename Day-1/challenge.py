"""A question none of the three systems was designed for."""

from config import QUESTIONS, COURSE_FEES
from chatbot import chatbot
from workflow import workflow
from agent import agent


CHALLENGE = (
    "I am a new AI student. "
    "If I take AI202 and DS303 together, "
    "how much will I pay after a 15% scholarship?"
)


if __name__ == "__main__":

    print("\n=== CHALLENGE ===\n")

    print("Question:")
    print(CHALLENGE)
    print("\n" + "-" * 70)

    print("\nSYSTEM 1: CHATBOT")
    print("A:", chatbot(CHALLENGE))

    print("\n" + "-" * 70)

    print("\nSYSTEM 2: RULE-BASED WORKFLOW")
    print("A:", workflow(CHALLENGE))

    print("\n" + "-" * 70)

    print("\nSYSTEM 3: AI AGENT")
    print("A:", agent(CHALLENGE))

    print("\n" + "-" * 70)