"""Tools the agent is allowed to use, plus their JSON Schema descriptions."""

import ast
import operator

from config import COURSE_FEES


def get_course_fee(course_code: str) -> str:
    """Look up the fee for one course code."""
    fee = COURSE_FEES.get(course_code.strip().upper())

    return str(fee) if fee is not None else f"Unknown course code: {course_code}"


# A safe calculator: only numbers and + - * / ( ) are allowed.
# Never use eval().

_ALLOWED = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
}


def calculator(expression: str) -> float:
    """Safely calculate a basic arithmetic expression."""

    def evaluate(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value

        if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED:
            return _ALLOWED[type(node.op)](evaluate(node.operand))

        if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED:
            return _ALLOWED[type(node.op)](
                evaluate(node.left),
                evaluate(node.right)
            )

        raise ValueError("Only numbers and + - * / ( ) are allowed")

    tree = ast.parse(expression, mode="eval")
    return evaluate(tree.body)


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_course_fee",
            "description": "Look up the private college fee for one course code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_code": {
                        "type": "string"
                    }
                },
                "required": ["course_code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate a basic arithmetic expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


TOOL_FUNCTIONS = {
    "get_course_fee": get_course_fee,
    "calculator": calculator,
}


if __name__ == "__main__":
    print("get_course_fee('ai202') ->", get_course_fee("ai202"))
    print(
        "calculator('(12000 + 18000) * 0.9) ->",
        calculator("(12000 + 18000) * 0.9")
    )
    print(
        "calculator('15000 - 12000') ->",
        calculator("15000 - 12000")
    )