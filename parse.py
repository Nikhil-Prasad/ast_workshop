NUMBER = "NUMBER"
PLUS = "PLUS"
MINUS = "MINUS"
STAR = "STAR"
SLASH = "SLASH"
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
        """Returns the next token, advancing position"""
        #skip whitespace
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1
        # check if current token is EOF 
        if self.pos >= len(self.text):
            return Token(EOF, None) #will work as soon as we get out of range
        #get current character
        current_char = self.text[self.pos]
        #do checks based on constant types defined above.
        if current_char.isdigit():
            self.pos += 1
            total_char = []
            total_char.append(current_char)
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                total_char.append(self.text[self.pos])
                self.pos +=1
            number_str = "".join(total_char)
            return Token(NUMBER, int(number_str))
        elif current_char == "+":
            self.pos +=1
            return Token(PLUS, current_char)
        elif current_char == "-":
            self.pos +=1
            return Token(MINUS, current_char)
        elif current_char == "*":
            self.pos +=1
            return Token(STAR, current_char)
        elif current_char == "/":
            self.pos +=1
            return Token(SLASH, current_char)
        elif current_char == "(": 
            self.pos +=1
            return Token(LPAREN, current_char)
        elif current_char == ")":
            self.pos +=1
            return Token(RPAREN, current_char)
         

        

