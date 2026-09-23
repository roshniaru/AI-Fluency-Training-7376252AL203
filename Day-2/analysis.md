# Day 2 – Analysis

## 1. ReAct Trace

The paper ReAct trace was compared with the actual agent trace from `react_trace.py`.

The agent used the available tools to retrieve the course fees and perform the required calculations.

## 2. Chain-of-Thought Comparison

The same three questions were tested with and without Chain-of-Thought.

| Question | Without CoT | With CoT |
|----------|--------------|----------|
| Course instalment | Direct final answer | Step-by-step calculation |
| Computer sittings | Direct final answer | Step-by-step calculation |
| Height ordering | Direct final answer | Step-by-step reasoning |

Both approaches produced the correct final answers in the test run.

## 3. Self-Consistency

The first question was run 5 times using a temperature of 0.8.

All five runs produced the same numerical answer:

Rs. 9,562.50 per instalment.

The wording and formatting varied slightly between runs. The majority-answer mechanism selected the repeated answer as the final result.

## 4. Observation

ReAct shows the agent's interaction with tools through actions and observations.

Chain-of-Thought produces intermediate reasoning steps, while the direct approach produces only the final answer.

Self-consistency runs the reasoning process multiple times and uses the majority answer to reduce the effect of variation between individual responses.