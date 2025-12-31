"""
Problem Spec:

Given a string s representing a valid expression, implement a basic calculator to evaluate it, and return the result of the evaluation.

Note: You are not allowed to use any built-in function which evaluates strings as mathematical expressions, such as eval().

 

Example 1:

Input: s = "1 + 1"
Output: 2
Example 2:

Input: s = " 2-1 + 2 "
Output: 3
Example 3:

Input: s = "(1+(4+5+2)-3)+(6+8)"
Output: 23
 

Constraints:

1 <= s.length <= 3 * 105
s consists of digits, '+', '-', '(', ')', and ' '.
s represents a valid expression.
'+' is not used as a unary operation (i.e., "+1" and "+(2 + 3)" is invalid).
'-' could be used as a unary operation (i.e., "-1" and "-(2 + 3)" is valid).
There will be no two consecutive operators in the input.
Every number and running calculation will fit in a signed 32-bit integer.


Solution Logic: 

Ok so the way to do this is to build the parse + AST evaluate logic. We should start with the AST core concepts. According to this, the AST is only concerned about numbers, and bin ops. 

The end logic of this is you get a string. You parse it char by char into an AST. Then you evaluate the AST recurisvely to get a numeric result. The end. 

So we can make a shorter version. We have statment and expr and num. Then we have binOp. Within binop we are given plus and minus. I guess no multiplication or division. Lparen and RParen are happening at the parser level. So our binop is just 2 conditons. They only mention - for unary ops. 

#NOTE: you need binding power for this even for associativity. since lbp < min_bp (not less than or equal to) so that things like 8-3-2 evaluate as BinOP(BinOP(8,-,3), -, 2)) not BinOP(8,-, BinOp(3, -,2))

"""
from typing import Any, Optional


## AST core 


class Expr():
    "ABC"
    def evaluate(self, env: dict[str, Any]) -> Any:
        raise NotImplementedError
    
class Num(Expr):
    n: int | float

    def __init__(self, number: int | float) -> None: 
        """Initialize a new numeric literal"""
        self.n = number

    def evaluate(self, env: dict[str, Any]) -> Any:
        return self.n #base case 

class UnaryOp(Expr):
    op: str
    operand: Expr

    def __init__(self, op: str, operand: Expr) -> None:
        self.op = op
        self.operand = operand

    def evaluate(self, env: dict[str, Any]) -> Any:
        operand_val = self.operand.evaluate(env)
        if self.op == '-':
            return -operand_val
        return operand_val

class BinOP(Expr):
    """
    Arithmetic Binary Operation. 
    """
    left: Expr
    op: str
    right: Expr

    def __init__(self, left: Expr, op: str, right: Expr) -> None:
        self.left = left
        self.op = op 
        self.right = right

    def evaluate(self, env: dict[str,Any]) -> Any:
        "calculate"

        left_val = self.left.evaluate(env)
        right_val = self.right.evaluate(env)

        if self.op == "+":
            return left_val + right_val
        if self.op == "-":
            return left_val - right_val
        

# Parser core

NUMBER = "NUMBER"
PLUS = "PLUS"
MINUS = "MINUS"
LPAREN = "LPAREN"
RPAREN = "RPAREN"
EOF = "EOF"

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0 #current position

    def next_token(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos +=1 #deals with removing whitespace 
        if self.pos >= len(self.text):
            return Token(EOF, None) #ends statement 
        
        current_char = self.text[self.pos]

        if current_char.isdigit():
            #need to check if it is multi digit. 
            self.pos += 1
            total_char = [] #holds the multi digit
            total_char.append(current_char)
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                total_char.append(self.text[self.pos])
                self.pos +=1
            number_str = "".join(total_char)
            return Token(NUMBER, int(number_str))

        elif current_char == "+":
            self.pos += 1 
            return Token(PLUS, current_char)
        
        elif current_char == "-":
            self.pos += 1
            return Token(MINUS, current_char)
    
        elif current_char == "(":
            self.pos += 1
            return Token(LPAREN, current_char)
        
        elif current_char == ")":
            self.pos += 1 
            return Token(RPAREN, current_char)
    
class Parser: 
    "basic arithemetic only. Builds the AST for binops for arithmetic. Inherits the lexer"
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = lexer.next_token() #you could do this in one class 

    def peek(self):
        """See current token without consuming it. Just a helper"""
        return self.current_token.type
    
    def advance(self):
        """Moves to next token"""
        self.current_token = self.lexer.next_token()

    def expect(self, token_type):
        if self.current_token.type != token_type:
            raise SyntaxError
        self.advance()
    
    def get_infix_binding_power(self, op_type):
        """Returns the binding power for an operator"""
        BP = {
            PLUS: (3,4),
            MINUS: (3,4),
        }
        if op_type in BP:
            return BP[op_type]
        else:
            raise ValueError(f"unknown operator: {op_type}")
    
    def parse_primary(self):
        if self.current_token.type == NUMBER:
            value = self.current_token.value
            self.advance()
            return Num(value)
        elif self.current_token.type == MINUS: 
            value = self.current_token.value
            self.advance()
            expr = self.parse_expr(7) #high BP 
            return UnaryOp(value, expr)
        elif self.current_token.type == LPAREN:
            value = self.current_token.value
            self.advance()
            expr = self.parse_expr(0)
            self.expect(RPAREN)
            return expr
        else: 
            raise SyntaxError

    def parse_expr(self, min_bp):
        
        lhs = self.parse_primary()

        while True:
            op_type = self.peek()
            if op_type not in [PLUS, MINUS]:
                break
            lbp, rbp = self.get_infix_binding_power(op_type)
            if lbp < min_bp:
                break
            value = self.current_token.value
            self.advance()
            rhs = self.parse_expr(rbp)
            lhs = BinOP(lhs, value, rhs)

        return lhs

class Solution:
    def calculate(self, s:str) -> int:
        parser = Parser(Lexer(s))
        ast = parser.parse_expr(0) #init min bp
        result = ast.evaluate({})
        return result


if __name__ == "__main__":
    sol = Solution()
    
    # Test 1: Simple addition
    test1 = "1 + 1"
    result1 = sol.calculate(test1)
    print(f"Test 1: {test1} = {result1} (expected: 2)")
    
    # Test 2: Subtraction chain
    test2 = "2-1 + 2"
    result2 = sol.calculate(test2)
    print(f"Test 2: {test2} = {result2} (expected: 3)")
    
    # Test 3: Parentheses
    test3 = "(1+(4+5+2)-3)+(6+8)"
    result3 = sol.calculate(test3)
    print(f"Test 3: {test3} = {result3} (expected: 23)")
    
    # Test 4: Associativity check (critical!)
    test4 = "8-3-2"
    result4 = sol.calculate(test4)
    print(f"Test 4: {test4} = {result4} (expected: 3, NOT 7)")
    
    # Test 5: Unary minus
    test5 = "-5 + 3"
    result5 = sol.calculate(test5)
    print(f"Test 5: {test5} = {result5} (expected: -2)")
    
    print("\nDone! Check if results match expected values.")
