# ast_workshop/tests/test_contract.py
"""
Contract tests: AST invariant validation.

Tests that:
1. Parsed ASTs pass validation (no violations)
2. Malformed ASTs are detected

Run with: pytest tests/test_contract.py -v
"""
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from parse import Lexer, Parser
from utils.validate import validate_ast, Violation
import expr_ast as ast


def parse(src: str):
    """Parse source code to AST."""
    return Parser(Lexer(src)).parse()


def test_validate_clean_on_parsed_exprs():
    """All parsed expressions should pass validation."""
    srcs = [
        "3 + 5 * 2",
        "-(2+3)*4",
        "8 - 3 - 2",
        "12 + (34 - 5) * 2",
        "42",
        "-7",
        "2 * -3",
        "(((3 + 5)))",
        "100 / 4 * 2",
    ]
    for src in srcs:
        tree = parse(src)
        violations = validate_ast(tree)
        assert violations == [], f"{src}: {violations}"


def test_validate_num_node():
    """Num node with valid value passes."""
    node = ast.Num(42)
    assert validate_ast(node) == []
    
    node2 = ast.Num(3.14)
    assert validate_ast(node2) == []


def test_validate_binop_valid_operators():
    """BinOp with valid operators passes."""
    for op in ["+", "-", "*", "/", "//", "%", "**"]:
        node = ast.BinOp(ast.Num(1), op, ast.Num(2))
        violations = validate_ast(node)
        assert violations == [], f"Operator {op} should be valid"


def test_validate_binop_invalid_operator():
    """BinOp with invalid operator fails."""
    node = ast.BinOp(ast.Num(1), "invalid_op", ast.Num(2))
    violations = validate_ast(node)
    assert len(violations) == 1
    assert violations[0].code == "BIN_OP"


def test_validate_unaryop_valid():
    """UnaryOp with valid operators passes."""
    for op in ["-", "+", "not"]:
        node = ast.UnaryOp(op, ast.Num(5))
        violations = validate_ast(node)
        assert violations == [], f"Operator {op} should be valid"


def test_validate_unaryop_invalid():
    """UnaryOp with invalid operator fails."""
    node = ast.UnaryOp("~", ast.Num(5))  # ~ not in allowed set
    violations = validate_ast(node)
    assert len(violations) == 1
    assert violations[0].code == "UNARY_OP"


def test_validate_none_child():
    """None as a child is detected."""
    node = ast.BinOp(ast.Num(1), "+", None)
    violations = validate_ast(node)
    assert any(v.code == "NONE_NODE" for v in violations)


def test_validate_nested_expression():
    """Deeply nested expressions are validated recursively."""
    # (1 + 2) * (3 + 4)
    left = ast.BinOp(ast.Num(1), "+", ast.Num(2))
    right = ast.BinOp(ast.Num(3), "+", ast.Num(4))
    root = ast.BinOp(left, "*", right)
    
    violations = validate_ast(root)
    assert violations == []


def test_validate_name_node():
    """Name node with valid id passes."""
    node = ast.Name("x")
    assert validate_ast(node) == []


def test_validate_name_empty():
    """Name node with empty id fails."""
    node = ast.Name("")
    violations = validate_ast(node)
    assert len(violations) == 1
    assert violations[0].code == "NAME_ID"


def test_validate_assign_valid():
    """Assign statement with valid target passes."""
    node = ast.Assign("x", ast.Num(42))
    assert validate_ast(node) == []


def test_validate_assign_empty_target():
    """Assign statement with empty target fails."""
    node = ast.Assign("", ast.Num(42))
    violations = validate_ast(node)
    assert len(violations) == 1
    assert violations[0].code == "ASSIGN_TARGET"


def test_validate_compare_valid():
    """Compare with valid operators passes."""
    for op in ["<", ">", "==", "!=", "<=", ">="]:
        node = ast.Compare(ast.Num(1), op, ast.Num(2))
        violations = validate_ast(node)
        assert violations == [], f"Operator {op} should be valid"


def test_validate_boolop_valid():
    """BoolOp with valid operators passes."""
    for op in ["and", "or"]:
        node = ast.BoolOp(op, ast.Num(1), ast.Num(2))
        violations = validate_ast(node)
        assert violations == [], f"Operator {op} should be valid"


if __name__ == "__main__":
    test_validate_clean_on_parsed_exprs()
    test_validate_num_node()
    test_validate_binop_valid_operators()
    test_validate_binop_invalid_operator()
    test_validate_unaryop_valid()
    test_validate_unaryop_invalid()
    test_validate_none_child()
    test_validate_nested_expression()
    test_validate_name_node()
    test_validate_name_empty()
    test_validate_assign_valid()
    test_validate_assign_empty_target()
    test_validate_compare_valid()
    test_validate_boolop_valid()
    print("\n All contract tests passed!")
