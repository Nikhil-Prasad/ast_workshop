import expr_ast as ast

NUMBER = "NUMBER"
PLUS = "PLUS"
MINUS = "MINUS"
STAR = "STAR"
SLASH = "SLASH"
LPAREN = "LPAREN"
RPAREN = "RPAREN"
EOF = "EOF"

class Token:
    def __init__(self, type, value, pos=0):
        self.type = type
        self.value = value
        self.pos = pos  # Position in source where token starts

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0 #current position

    def next_token(self):
        """Returns the next token, advancing position"""
        #skip whitespace
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1
        # check if current token is EOF 
        if self.pos >= len(self.text):
            return Token(EOF, None, self.pos)
        
        # Remember token start position
        token_start = self.pos
        current_char = self.text[self.pos]
        
        #do checks based on constant types defined above.
        if current_char.isdigit():
            total_char = [current_char]
            self.pos += 1
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                total_char.append(self.text[self.pos])
                self.pos += 1
            number_str = "".join(total_char)
            return Token(NUMBER, int(number_str), token_start)
        elif current_char == "+":
            self.pos += 1
            return Token(PLUS, current_char, token_start)
        elif current_char == "-":
            self.pos += 1
            return Token(MINUS, current_char, token_start)
        elif current_char == "*":
            self.pos += 1
            return Token(STAR, current_char, token_start)
        elif current_char == "/":
            self.pos += 1
            return Token(SLASH, current_char, token_start)
        elif current_char == "(": 
            self.pos += 1
            return Token(LPAREN, current_char, token_start)
        elif current_char == ")":
            self.pos += 1
            return Token(RPAREN, current_char, token_start)
        else:
            raise SyntaxError(f"Unexpected character '{current_char}' at position {self.pos}")
         
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = lexer.next_token()

    def peek(self):
        """See current token without consuming it"""
        return self.current_token.type
    
    def advance(self):
        """Move to next token"""
        self.current_token = self.lexer.next_token()

    def expect(self, token_type):
        """Consume token if it matches, else error"""
        if self.current_token.type != token_type:
            raise SyntaxError(
                f"Expected {token_type}, got {self.current_token.type} "
                f"at position {self.current_token.pos}"
            )
        self.advance()
    
    def get_infix_binding_power(self, op_type):
        """Returns the binding power for an operator"""
        BP = {
            PLUS: (3,4),
            MINUS: (3,4),
            STAR: (5,6),
            SLASH: (5,6)
        }
        if op_type in BP:
            return BP[op_type]
        else:
            raise ValueError(f"unknown operator: {op_type}")
        
    def parse_primary(self):
        """Base case primary/prefix parser"""
        if self.current_token.type == NUMBER:
            value = self.current_token.value
            self.advance()
            return ast.Num(value)
        elif self.current_token.type == LPAREN:
            self.advance()
            expr = self.parse_expr(0)
            self.expect(RPAREN)
            return expr 
        elif self.current_token.type == MINUS:
            value = self.current_token.value
            self.advance()
            expr = self.parse_expr(7) #harcoded higher for unaryOps
            return ast.UnaryOp(value, expr)
        else:
            raise SyntaxError(
                f"Unexpected token in primary position: {self.current_token.type} "
                f"at position {self.current_token.pos}"
            )
        
    def parse_expr(self, min_bp):
        """Core pratt algorithm"""
        lhs = self.parse_primary()   
        while True: 
            op_type = self.peek()
            if op_type not in [PLUS, MINUS, STAR, SLASH]:
                break         
            lbp, rbp = self.get_infix_binding_power(op_type)
            if lbp < min_bp:
                break            
            value = self.current_token.value
            self.advance()
            rhs = self.parse_expr(rbp)
            lhs = ast.BinOp(lhs, value, rhs)
        
        return lhs

    def parse_statement(self):
        """Parse individual statements"""
        NotImplemented
    
    def parse_module(self):
        """Parse full module"""
        NotImplemented
    
    def parse(self):
        """Entry point - parse a complete expression"""
        return self.parse_expr(0)
