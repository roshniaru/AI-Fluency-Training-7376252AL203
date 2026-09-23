## 4. Comparison

| Criterion | Chatbot | Workflow | AI Agent |
|---|---|---|---|
| Private data access | No | Yes | Yes |
| Flexibility | High | Low | High |
| Fixed rules | No | Yes | No |
| Tool usage | No | No | Yes |
| Multi-step tasks | Limited | Limited | Yes |
| Reliability | Depends on LLM | Predictable | Depends on LLM and tools |
| Main strength | Natural conversation | Predictable results | Flexible problem solving |
| Main weakness | Cannot access private data | Rigid rules | Tool selection may vary |

## Agent Trace

What is the total fee for CS101 and AI202 after a 10% scholarship?

| Step | Tool Called | Input | Result |
|---:|---|---|---:|
| 1 | `get_course_fee` | CS101 | Rs. 12,000 |
| 2 | `get_course_fee` | AI202 | Rs. 18,000 |
| 3 | `calculator` | `12000 + 18000` | Rs. 30,000 |
| 4 | `calculator` | `30000 * 0.9` | Rs. 27,000 |
