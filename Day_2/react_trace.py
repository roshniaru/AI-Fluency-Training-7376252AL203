"""Day 2, Part D: print the agent's real ReAct trace to compare with your paper trace."""

import sys
import os

# Add Day-1 folder to the beginning of Python's import path
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "Day_1")
    )
)

from agent import agent

QUESTION = (
    "Which is cheaper: CS101 and AI202 with a 10% scholarship, "
    "or all three courses with a 25% scholarship? By how much?"
)

print("QUESTION:", QUESTION, "\n")
print("--- the agent's actions and observations ---")

answer = agent(QUESTION, max_steps=8)

print("\nFINAL ANSWER:", answer)