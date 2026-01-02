# ast_workshop/tests/test_roundtrip.py
"""
Round-trip tests for AST codec.

Ensures: parse → serialize → deserialize → evaluate gives same result.

Run with: pytest tests/test_roundtrip.py -v
"""
import json
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from parse import Lexer, Parser
from utils.ast_codec import to_obj, from_obj


def parse(src: str):
    """Parse source code to AST."""
    return Parser(Lexer(src)).parse()


def test_roundtrip_preserves_meaning():
    """
    AST → JSON → AST round-trip preserves evaluation semantics.
    """
    srcs = [
        "3 + 5 * 2",
        "(3 + 5) * 2",
        "-(2+3)*4",
        "8 - 3 - 2",
        "12 + (34 - 5) * 2",
        "-5 + 3",
        "2 * -3",
        "- - 5",
        "100 / 4 * 2",
        "(((3)))",
    ]
    for src in srcs:
        ast1 = parse(src)
        original_result = ast1.evaluate({})
        
        # Serialize to JSON and back
        obj = to_obj(ast1)
        blob = json.dumps(obj, sort_keys=True)  # deterministic
        ast2 = from_obj(json.loads(blob))
        
        roundtrip_result = ast2.evaluate({})
        assert original_result == roundtrip_result, (
            f"Round-trip failed for {src!r}: "
            f"original={original_result}, roundtrip={roundtrip_result}"
        )


def test_roundtrip_structure():
    """
    Serialized structure is deterministic.
    """
    src = "3 + 5 * 2"
    ast1 = parse(src)
    
    obj1 = to_obj(ast1)
    blob1 = json.dumps(obj1, sort_keys=True)
    
    # Parse again and serialize - should be identical
    ast2 = parse(src)
    obj2 = to_obj(ast2)
    blob2 = json.dumps(obj2, sort_keys=True)
    
    assert blob1 == blob2, "Serialization should be deterministic"


def test_codec_node_types():
    """Test codec handles each node type we emit."""
    # Num
    ast_num = parse("42")
    assert to_obj(ast_num) == {"t": "Num", "n": 42}
    
    # UnaryOp
    ast_unary = parse("-5")
    obj_unary = to_obj(ast_unary)
    assert obj_unary["t"] == "UnaryOp"
    assert obj_unary["op"] == "-"
    
    # BinOp
    ast_bin = parse("3 + 5")
    obj_bin = to_obj(ast_bin)
    assert obj_bin["t"] == "BinOp"
    assert obj_bin["op"] == "+"


def test_roundtrip_all_operators():
    """Test round-trip for all supported operators."""
    expressions = [
        "3 + 5",
        "10 - 3",
        "4 * 5",
        "20 / 4",
        "-7",
        "- -3",
    ]
    for src in expressions:
        ast1 = parse(src)
        ast2 = from_obj(to_obj(ast1))
        assert ast1.evaluate({}) == ast2.evaluate({}), f"Failed for {src}"


if __name__ == "__main__":
    test_roundtrip_preserves_meaning()
    test_roundtrip_structure()
    test_codec_node_types()
    test_roundtrip_all_operators()
    print("\n✅ All round-trip tests passed!")
