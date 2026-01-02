# ast_workshop/validate.py
"""
AST validation: cheap, local invariant checks.

Returns a list of Violations for any structural issues found.
Empty list = AST is valid.

Usage:
    from validate import validate_ast
    
    violations = validate_ast(ast_node)
    if violations:
        for v in violations:
            print(f"{v.code} at {v.path}: {v.msg}")
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import expr_ast as ast


@dataclass(frozen=True)
class Violation:
    """A single validation error."""
    code: str      # Short code like "NONE_NODE", "BIN_OP", etc.
    path: str      # Path in the tree like "root.left.right"
    msg: str       # Human-readable description


# Allowed operators for each node type
_ALLOWED_BINOPS = {"+", "-", "*", "/", "//", "%", "**"}
_ALLOWED_UNARY = {"-", "+", "not"}
_ALLOWED_COMPARE = {"<", ">", "==", "!=", "<=", ">="}
_ALLOWED_BOOLOP = {"and", "or"}


def validate_ast(node: Any) -> list[Violation]:
    """
    Validate an AST node and all its children.
    
    Returns a list of Violations (empty if valid).
    """
    out: list[Violation] = []

    def v(code: str, path: str, msg: str):
        out.append(Violation(code=code, path=path, msg=msg))

    def walk(n: Any, path: str):
        if n is None:
            v("NONE_NODE", path, "node is None")
            return

        # Expr nodes
        if isinstance(n, ast.Num):
            if not isinstance(n.n, (int, float)):
                v("NUM_TYPE", f"{path}.n", f"Num.n must be int|float, got {type(n.n).__name__}")
            return

        if isinstance(n, ast.Name):
            if not isinstance(n.id, str) or not n.id:
                v("NAME_ID", f"{path}.id", "Name.id must be non-empty string")
            return

        if isinstance(n, ast.UnaryOp):
            if n.op not in _ALLOWED_UNARY:
                v("UNARY_OP", f"{path}.op", f"invalid unary op: {n.op}")
            walk(n.operand, f"{path}.operand")
            return

        if isinstance(n, ast.BinOp):
            if n.op not in _ALLOWED_BINOPS:
                v("BIN_OP", f"{path}.op", f"invalid bin op: {n.op}")
            walk(n.left, f"{path}.left")
            walk(n.right, f"{path}.right")
            return

        if isinstance(n, ast.Compare):
            if n.op not in _ALLOWED_COMPARE:
                v("CMP_OP", f"{path}.op", f"invalid compare op: {n.op}")
            walk(n.left, f"{path}.left")
            walk(n.right, f"{path}.right")
            return

        if isinstance(n, ast.BoolOp):
            if n.op not in _ALLOWED_BOOLOP:
                v("BOOL_OP", f"{path}.op", f"invalid bool op: {n.op}")
            walk(n.left, f"{path}.left")
            walk(n.right, f"{path}.right")
            return

        # Statement nodes
        if isinstance(n, ast.Assign):
            if not isinstance(n.target, str) or not n.target:
                v("ASSIGN_TARGET", f"{path}.target", "Assign.target must be non-empty string")
            walk(n.value, f"{path}.value")
            return

        if isinstance(n, ast.Print):
            walk(n.argument, f"{path}.argument")
            return

        if isinstance(n, ast.If):
            walk(n.test, f"{path}.test")
            if not isinstance(n.body, list):
                v("IF_BODY", f"{path}.body", "If.body must be list[Statement]")
            else:
                for i, st in enumerate(n.body):
                    walk(st, f"{path}.body[{i}]")
            if not isinstance(n.orelse, list):
                v("IF_ORELSE", f"{path}.orelse", "If.orelse must be list[Statement]")
            else:
                for i, st in enumerate(n.orelse):
                    walk(st, f"{path}.orelse[{i}]")
            return

        if isinstance(n, ast.ForRange):
            if not isinstance(n.target, str) or not n.target:
                v("FOR_TARGET", f"{path}.target", "ForRange.target must be non-empty string")
            walk(n.start, f"{path}.start")
            walk(n.stop, f"{path}.stop")
            if not isinstance(n.body, list):
                v("FOR_BODY", f"{path}.body", "ForRange.body must be list[Statement]")
            else:
                for i, st in enumerate(n.body):
                    walk(st, f"{path}.body[{i}]")
            return

        if isinstance(n, ast.Module):
            if not isinstance(n.body, list):
                v("MODULE_BODY", f"{path}.body", "Module.body must be list[Statement]")
            else:
                for i, st in enumerate(n.body):
                    walk(st, f"{path}.body[{i}]")
            return

        v("UNKNOWN_NODE", path, f"unknown node type: {type(n).__name__}")

    walk(node, "root")
    return out
