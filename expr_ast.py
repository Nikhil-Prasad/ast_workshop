"""
Minimal learning implementation for abstract syntax trees. 

We start by implementing the Expr class, and then implementing literals as the base cases of the AST

"""
from typing import Any, Optional

class Statement:
    """
    An abstract class representing a Python statement
    
    We think of a python statement as being more a general piece of code than a single expression, and that can have some kind of effect.   
    """

    def evaluate(self, env: dict[str, Any]) -> Optional[Any]:
        """
        Evaluate this statement with the given environment.

        Should have the same effect as evaluating the statement by a python interpreter
        """
        raise NotImplementedError

class Module: 
    """
    A class representing a full python program. 

    Instance attributes: 
        -body: A sequence of statements.
    """
    body: list[Statement]

    def __init__(self, body: list[Statement]) -> None:
        """Initialize a new module with the given body"""
        self.body = body


    def evaluate(self) -> None:
        """Evaluate this statement with the given environment."""

        env = {}
        for statement in self.body:
            statement.evaluate(env)

class Expr(Statement):
    """
    Abstract class that represents a Python expression.
    """
    def evaluate(self, env: dict[str, Any]) -> Any:
        """
        Return the *value* of this expression. The returned value is the result of how this expression is evaluated by the python interpreter. A subclass now of the generic statement
        """
        raise NotImplementedError

class Num(Expr):
    """
    A numeric literal

    Instance attributes: 
        - n: the value of the literal
    """
    n: int | float

    def __init__(self, number: int | float) -> None:
        """Initialize a new numeric literal"""
        self.n = number
    
    def evaluate(self, env: dict[str, Any]) -> Any:
        """Here we can simply return the number, since the python interpreter recognizes it as an int or a float"""
        
        return self.n

class Name(Expr):
    """
    A variable expression. 

    Instance attributes:
        -id: The variable name.
    """
    id: str

    def __init__(self, id_: str) -> None:
        """initialize a new variable expression"""
        self.id = id_


    def evaluate(self, env: dict[str, Any]) -> Any:
        """Returns the python interpreted evaluated version of this expression"""
        if self.id in env:
            return env[self.id]
        else: 
            raise NameError(f"name '{self.id}' is not defined")

class Assign(Statement):
    """An assignment statement (with a single target)
    
    Instance attributes:
        - target: the variable name on the left hand side of the equals sign
        - value: expression on the right hand side of the equals sign 
    """
    target: str
    value: Expr

    def __init__(self, target: str, value: Expr) -> None:
        """initialize a new assign node"""
        self.target = target
        self.value = value

    def evaluate(self, env: dict[str, Any]) -> ...:
        """Evalute this statement with the given environment."""
        env[self.target] = self.value.evaluate(env)

class Print(Statement):
    """A statement representing a call to the print function

    Instance Attributes: 
        - argument: The argument expression to the print function
    """

    def __init__(self, argument: Expr) -> None:
        self.argument = argument
    
    def evaluate(self, env: dict[str, Any]) -> None:
        """This evaluates the argument of the print call, and then actually prints it"""
        print(self.argument.evaluate(env))

class If(Statement):
    """
    An if statement. 

    This is a statement of the form: 
        if <test>:
            <body>
        else:
            <orelse>
    
    Instance Attributes:
        -test: The condition expression of this if statement. 
        -body: A sequence of statements to evaluate if the condition is True.
        -orelse: A sequence of statements to evaluate if the condition is False. 
                (This would be empty in the case that there is no else block)
    """
    test: Expr
    body: list[Statement]
    orelse: list[Statement]

    def __init__(self, test: Expr, body: list[Statement], orelse: list[Statement]) -> Any:
        self.test = test
        self.body = body
        self.orelse = orelse
    
    def evaluate(self, env:dict[str, Any]) -> Any:
        test_result = self.test.evaluate(env)
        if test_result:
            for statement in self.body:
                statement.evaluate(env)
        else: 
            for statement in self.orelse:
                statement.evaluate(env)
    
class ForRange(Statement):
    """
    A for loop that loops over a range of numbers. 
        for <target> in range(<start>, <stop>):
            <body>
    
    Instance attributes:
        - target: the loop variable
        - start: the start of the range(inclusive)
        - stop: The end of the range( this is exclusive, so stop is not included in the loop)
        - body: the statements to execute in the loop body.
    """
    target: str
    start: Expr
    stop: Expr
    body: list[Statement]

    def __init__(self, target: str, start: Expr, stop: Expr, body: list[Statement]) -> None:
        self.target = target
        self.start = start
        self.stop = stop 
        self.body = body

    def evaluate(self, env):
        start_val = self.start.evaluate(env)
        stop_val = self.stop.evaluate(env)

        for i in range(start_val, stop_val):
            env[self.target] = i
            for statement in self.body:
                statement.evaluate(env)

class BinOp(Expr):
    """
    An arithmetic binary operation. 

    Instance attributes:
        - left: the left operand
        - op: the name of the operator
        - right: the right operand
    
    Representation Invariants:
        - self.op in {'+', '*', '-', '/', '//', '%', '**'}
    """
    left: Expr
    op: str
    right: Expr

    def __init__(self, left: Expr, op: str, right: Expr) -> None:
        """Initialize a new bin op"""
        self.left = left
        self.op = op 
        self.right = right

    def evaluate(self, env: dict[str, Any]) -> Any:
        """Returns the interpreter valid value of a bin op expression"""
        left_val = self.left.evaluate(env)
        right_val = self.right.evaluate(env)

        if self.op == "+":
            return left_val + right_val
        if self.op == "*":
            return left_val * right_val
        if self.op == "-":
            return left_val - right_val
        if self.op == "/":
            return left_val / right_val
        if self.op == "//":
            return left_val // right_val
        if self.op == "%":
            return left_val % right_val
        if self.op == "**":
            return left_val ** right_val

        else:
            raise ValueError(f'Invalid Operator {self.op}')

class Compare(Expr):
    """
    A comparison operation.
    
    Instance attributes:
        - left: the left operand
        - op: the comparison operator
        - right: the right operand
    
    Representation Invariants:
        - self.op in {'<', '>', '==', '!=', '<=', '>='}
    """
    left: Expr
    op: str
    right: Expr

    def __init__(self, left: Expr, op: str, right: Expr) -> None:
        """Initialize a new comparison operation"""
        self.left = left
        self.op = op
        self.right = right

    def evaluate(self, env: dict[str, Any]) -> bool:
        """Evaluate the comparison and return a boolean result"""
        
        left_val = self.left.evaluate(env)
        right_val = self.right.evaluate(env)

        if self.op == "<": 
            return left_val < right_val
        if self.op == ">":
            return left_val > right_val
        if self.op == "==":
            return left_val == right_val
        if self.op == "!=":
            return left_val != right_val
        if self.op == "<=": 
            return left_val <= right_val
        if self.op == ">=":
            return left_val >= right_val

        else:
            raise ValueError(f'Invalid Operator {self.op}')

class BoolOp(Expr):
    """
    A boolean operation (and/or).
    
    Instance attributes:
        - op: the boolean operator ('and' or 'or')
        - left: the left operand
        - right: the right operand
    
    Representation Invariants:
        - self.op in {'and', 'or'}
    """
    op: str
    left: Expr
    right: Expr

    def __init__(self, op: str, left: Expr, right: Expr) -> None:
        """Initialize a new boolean operation"""
        self.op = op
        self.left = left
        self.right = right

    def evaluate(self, env: dict[str, Any]) -> bool:
        """Evaluate the boolean operation and return the result"""
        
        left_val = self.left.evaluate(env)
        if self.op == "and":
            if not left_val:
                return left_val
            right_val = self.right.evaluate(env)
            if not right_val:
                return right_val
            return right_val

        if self.op == "or":
            if left_val:
                return left_val
            return self.right.evaluate(env)
        
        else:
            raise ValueError(f'Invalid Operator {self.op}')
       
class UnaryOp(Expr):
    """
    A unary operation.
    
    Instance attributes:
        - op: the unary operator
        - operand: the expression to apply the operator to
    
    Representation Invariants:
        - self.op in {'-', '+', 'not'}
    """
    op: str
    operand: Expr

    def __init__(self, op: str, operand: Expr) -> None:
        """Initialize a new unary operation"""
        self.op = op
        self.operand = operand

    def evaluate(self, env: dict[str, Any]) -> Any:
        """Evaluate the unary operation and return the result"""
        operand_value = self.operand.evaluate(env)

        if self.op == "-":
            return -(operand_value)
        if self.op == "+":
            return (operand_value)
        if self.op == "not":
            return not operand_value
        
        else:
            raise ValueError(f'Invalid Operator {self.op}')
