# ast_workshop/tests/test_parser.py
"""
Parser tests using golden fixtures.

Run with: pytest tests/test_parser.py -v
"""
import json
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from parse import Lexer, Parser

FIXTURES = Path(__file__).parent / "fixtures_expr.json"


def eval_expr(src: str):
    """Parse and evaluate an expression string."""
    parser = Parser(Lexer(src))
    ast = parser.parse()
    return ast.evaluate({})


def test_fixtures():
    """Test all expressions in fixtures_expr.json."""
    data = json.loads(FIXTURES.read_text())
    for row in data:
        src = row["src"]
        expected = row["expected"]
        got = eval_expr(src)
        assert got == expected, f'{src!r} -> {got}, expected {expected}'


def test_precedence_mul_over_add():
    """Multiplication binds tighter than addition."""
    assert eval_expr("3 + 5 * 2") == 13  # not 16


def test_associativity_left():
    """Subtraction is left-associative: 8-3-2 = (8-3)-2 = 3."""
    assert eval_expr("8 - 3 - 2") == 3  # not 7


def test_unary_minus():
    """Unary minus has high precedence."""
    assert eval_expr("-5 + 3") == -2
    assert eval_expr("2 * -3") == -6


def test_parentheses_override():
    """Parentheses override precedence."""
    assert eval_expr("(3 + 5) * 2") == 16


def test_nested_parens():
    """Deeply nested parentheses work."""
    assert eval_expr("(((3 + 5)))") == 8


def test_double_unary():
    """Double unary minus: - - 5 = 5."""
    assert eval_expr("- - 5") == 5


def test_unary_in_parens():
    """Unary inside parentheses: -(2+3)*4 = -20."""
    assert eval_expr("-(2+3)*4") == -20


def test_whitespace_tolerance():
    """Parser handles various whitespace."""
    assert eval_expr("  12 + (34 - 5) * 2 ") == 70


if __name__ == "__main__":
    # Allow running directly for quick testing
    test_fixtures()
    test_precedence_mul_over_add()
    test_associativity_left()
    test_unary_minus()
    test_parentheses_override()
    test_nested_parens()
    test_double_unary()
    test_unary_in_parens()
    test_whitespace_tolerance()
    print("\n✅ All parser tests passed!")
