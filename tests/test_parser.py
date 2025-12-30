"""Quick tests for the parser"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from parse import Lexer, Parser

# Test 1: Simple addition
code1 = "3 + 5"
parser1 = Parser(Lexer(code1))
ast1 = parser1.parse()
result1 = ast1.evaluate({})
print(f"Test 1: {code1} = {result1}")  # Should be 8
assert result1 == 8, f"Expected 8, got {result1}"

# Test 2: Precedence
code2 = "3 + 5 * 2"
parser2 = Parser(Lexer(code2))
ast2 = parser2.parse()
result2 = ast2.evaluate({})
print(f"Test 2: {code2} = {result2}")  # Should be 13 (not 16)
assert result2 == 13, f"Expected 13, got {result2}"

# Test 3: Parentheses
code3 = "(3 + 5) * 2"
parser3 = Parser(Lexer(code3))
ast3 = parser3.parse()
result3 = ast3.evaluate({})
print(f"Test 3: {code3} = {result3}")  # Should be 16
assert result3 == 16, f"Expected 16, got {result3}"

# Test 4: Unary minus
code4 = "-5 + 3"
parser4 = Parser(Lexer(code4))
ast4 = parser4.parse()
result4 = ast4.evaluate({})
print(f"Test 4: {code4} = {result4}")  # Should be -2
assert result4 == -2, f"Expected -2, got {result4}"

# Test 5: Complex expression
code5 = "10 / 2 + 3 * 4"
parser5 = Parser(Lexer(code5))
ast5 = parser5.parse()
result5 = ast5.evaluate({})
print(f"Test 5: {code5} = {result5}")  # Should be 17 (5 + 12)
assert result5 == 17, f"Expected 17, got {result5}"

print("\n✅ All tests passed!")
