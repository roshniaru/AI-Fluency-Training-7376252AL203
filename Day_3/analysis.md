# Day 3 – ReAct Agent Failure Analysis

## 1. Objective

The objective of this lab is to build a ReAct agent in plain Python using tools, understand the Reason–Act–Observe loop, deliberately test failure conditions, and improve the agent using safety guards.

The agent uses two tools:
- `calculator` – performs arithmetic calculations safely.
- `read_webpage` – reads local HTML files or web pages and extracts readable text.

## 2. Tools Implementation

### Calculator

The calculator uses Python's Abstract Syntax Tree (AST) module to evaluate arithmetic expressions safely instead of using `eval()`.

Test results:
- `(12000 + 18000) * 0.9` → `27000.0`
- `2 ** 10` → `1024`
- `import os` → Calculator error

### Webpage Reader

The `read_webpage` tool reads local files or HTTP/HTTPS URLs. It removes HTML tags and extra spaces and truncates long content to prevent excessive input to the language model.

Test results:
- `notice.html` → Successfully read the fee notice.
- `no_such_file.html` → Returned a file-not-found error message.

The tools return error messages instead of allowing most tool errors to crash the program.

## 3. ReAct Agent Implementation

The agent follows the ReAct loop:

1. **Reason:** The language model decides whether a tool is needed.
2. **Act:** The agent executes the requested tool.
3. **Observe:** The tool result is added to the conversation.
4. **Repeat:** The model can request another tool or provide its final answer.

The agent uses a maximum step limit to prevent unlimited tool calls.

## 4. Normal Test Results

### Test 1: Total Fee Including Hostel Laboratory Charge

**Question:** Read `notice.html` and calculate the total fee for all three courses, including the Rs. 4,500 hostel laboratory charge.

**Calculation:**

12000 + 18000 + 15000 + 4500 = 49500

**Observed result:** The agent read the notice and used the calculator. It returned the total fee as **Rs. 49,500**.

### Test 2: Merit Scholarship

**Question:** Read `notice.html` and calculate the total fee for CS101 and AI202 after the merit scholarship.

**Calculation:**

- CS101 fee = Rs. 12,000
- AI202 fee = Rs. 18,000
- Combined fee = Rs. 30,000
- Scholarship = 10% of Rs. 30,000 = Rs. 3,000
- Final fee = Rs. 27,000

**Observed result:** The agent read the fee notice and returned the final amount as **Rs. 27,000**. In this run, the model performed the arithmetic in its final response rather than making a separate calculator call.

## 5. Failure Analysis

### Failure 1: Missing File and Repeated Tool Calls

**Test question:** Read `fees.html` and tell me the fee for CS101.

**Expected issue:** The file does not exist. An agent might repeatedly call the same tool with the same arguments without making progress.

**Observed result:** The agent called `read_webpage` once. The tool returned a missing-file error, and the agent responded that it could not locate the file.

**Analysis:** The repeated-call loop was not reproduced in this run. However, repeatedly retrying the same failed tool call could waste API calls and increase execution time.

**Improvement:** Track previous tool calls and stop when the same call is repeated without progress.

### Failure 2: Hallucinated Tool

**Test setup:** A temporary instruction was added to the system prompt telling the model to use a nonexistent `send_email` tool when the fee exceeded Rs. 25,000.

**Observed result:** The model attempted to call `send_email`, which was not included in the available tool definitions. The API returned a tool-call validation error.

**Analysis:** A language model may request a tool that the application has not implemented. The application should validate every requested tool name before executing it.

**Improvement:** Use safe dictionary lookup with `TOOL_FUNCTIONS.get(name)`. If the tool does not exist, return an informative error message instead of directly indexing the dictionary.

A separate `KeyError` crash was not reproduced during my test.

### Failure 3: Context Overflow

**Test setup:** The truncation logic in `my_tools.py` was temporarily disabled. The agent was then asked to read `big.html` and count the listed students.

**Observed result:** The model request failed with an HTTP 413 / `rate_limit_exceeded` error because the request exceeded the provider's token-per-minute limit.

**Analysis:** Sending an entire large webpage to the model can exceed request limits, consume unnecessary resources, and interrupt execution.

**Improvement:** Restore the truncation logic and limit the amount of tool output passed to the model.

## 6. Safety Guards in the Fixed Agent

The fixed agent, implemented in `my_agent_fixed.py`, includes the following guards:

1. **Repeated-call detection:** Tracks tool names and arguments and stops after the same call occurs three times.
2. **Observation truncation:** Limits long tool results using `MAX_TOOL_CHARS = 2000`.
3. **Character budget:** Uses `CHAR_BUDGET = 35000` to limit the accumulated conversation content.
4. **Safe tool lookup:** Checks whether a requested tool exists before executing it.
5. **Maximum step limit:** Stops execution after the configured maximum number of steps.

These guards help reduce repeated API calls, avoid oversized observations, and prevent invalid tool requests from directly causing a dictionary lookup crash.

## 7. Fixed Agent Test Results

### Test 1: Scholarship Calculation

**Observed result:** The agent read `notice.html` and returned the final fee as Rs. 27,000.

### Test 2: Missing File

**Observed result:** The agent returned a missing-file error and explained that it could not locate `fees.html`.

### Test 3: Large Webpage

**Observed result:** The agent read the beginning of `big.html`, but the model requested the same webpage again. The repeated-call guard stopped execution after the third identical tool call.

**Analysis:** The repeated-call guard worked as intended. However, the agent did not successfully count all the students in this run.

## 8. Observation Table

| Test case | Expected issue or behaviour | Actual observation |
|---|---|---|
| Calculator test | Safe arithmetic | Correct results returned |
| Read `notice.html` | Read local HTML file | Successfully read |
| Missing file | File error | Error message returned |
| Hostel fee calculation | Calculate total fee | Rs. 49,500 |
| Scholarship calculation | Apply 10% scholarship | Rs. 27,000 |
| Repeated-call failure | Repeated calls may occur | No repeated call observed in the original missing-file test |
| Hallucinated tool | Invalid tool request | API validation error occurred |
| Large webpage without truncation | Oversized request | HTTP 413 / rate-limit error |
| Fixed agent with large webpage | Prevent repeated calls | Stopped after three identical calls |

## 9. Failure Log

- **Missing file:** `fees.html` was not found. The original agent stopped after one tool call.
- **Hallucinated tool:** The model attempted to call `send_email`, which was not an available tool. The API rejected the request.
- **Context overflow:** Reading the large webpage without truncation resulted in a request-size/token-limit error.
- **Fixed-agent large-page test:** Repeated tool calls were detected and execution was stopped.

## 10. Discussion

### Why is a maximum step limit necessary?

A maximum step limit prevents the agent from running indefinitely when the model repeatedly requests tools or fails to produce a final answer.

### Why should unknown tools be handled safely?

The model may request a tool that does not exist. Safe lookup allows the application to return a useful error message rather than crashing because of an invalid dictionary key.

### Why is output truncation important?

Large webpage contents can increase token usage and exceed provider request limits. Truncation reduces the size of observations sent back to the model.

### What is the purpose of a character budget?

A character budget limits accumulated conversation content and provides an additional safety check against oversized requests.

### What is the difference between the original and fixed agents?

The original agent can encounter repeated tool calls, invalid tool requests, and oversized observations. The fixed agent adds repeated-call detection, output truncation, a character budget, safe tool lookup, and a maximum step limit.

## 11. Conclusion

In this lab, I implemented a ReAct agent using Python, a calculator tool, and a webpage-reading tool. I tested normal operations and observed failures involving a missing file, an unavailable tool, and an oversized model request.

I then implemented safety guards in the fixed agent to detect repeated calls, limit tool output, control accumulated conversation content, and handle unknown tools safely.

This lab helped me understand the ReAct loop, tool integration, failure analysis, and the importance of guardrails when building reliable AI agents.