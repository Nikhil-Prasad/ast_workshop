# ast_workshop/ast_codec.py
"""
AST ⇄ JSON codec for round-trip serialization.

This codec supports the expression nodes that the parser currently emits:
- Num: numeric literals
- UnaryOp: unary operations (-, +, not)
- BinOp: binary operations (+, -, *, /, etc.)

Usage:
    from ast_codec import to_obj, from_obj
    import json
    
    # Serialize
    obj = to_obj(ast_node)
    json_str = json.dumps(obj)
    
    # Deserialize
    ast_node = from_obj(json.loads(json_str))
"""
from __future__ import annotations
import expr_ast as ast


def to_obj(node: ast.Expr) -> dict:
    """
    Convert an AST node to a JSON-serializable dict.
    
    Each dict has a 't' key indicating the node type, plus the node's attributes.
    """
    if isinstance(node, ast.Num):
        return {"t": "Num", "n": node.n}
    
    if isinstance(node, ast.UnaryOp):
        return {
            "t": "UnaryOp",
            "op": node.op,
            "operand": to_obj(node.operand)
        }
    
    if isinstance(node, ast.BinOp):
        return {
            "t": "BinOp",
            "op": node.op,
            "left": to_obj(node.left),
            "right": to_obj(node.right)
        }
    
    if isinstance(node, ast.Name):
        return {"t": "Name", "id": node.id}
    
    if isinstance(node, ast.Compare):
        return {
            "t": "Compare",
            "op": node.op,
            "left": to_obj(node.left),
            "right": to_obj(node.right)
        }
    
    if isinstance(node, ast.BoolOp):
        return {
            "t": "BoolOp",
            "op": node.op,
            "left": to_obj(node.left),
            "right": to_obj(node.right)
        }
    
    raise TypeError(f"Unsupported node for codec: {type(node).__name__}")


def from_obj(obj: dict) -> ast.Expr:
    """
    Reconstruct an AST node from a JSON-serializable dict.
    """
    t = obj["t"]
    
    if t == "Num":
        return ast.Num(obj["n"])
    
    if t == "UnaryOp":
        return ast.UnaryOp(obj["op"], from_obj(obj["operand"]))
    
    if t == "BinOp":
        return ast.BinOp(
            from_obj(obj["left"]),
            obj["op"],
            from_obj(obj["right"])
        )
    
    if t == "Name":
        return ast.Name(obj["id"])
    
    if t == "Compare":
        return ast.Compare(
            from_obj(obj["left"]),
            obj["op"],
            from_obj(obj["right"])
        )
    
    if t == "BoolOp":
        return ast.BoolOp(
            obj["op"],
            from_obj(obj["left"]),
            from_obj(obj["right"])
        )
    
    raise ValueError(f"Unknown node tag: {t}")
