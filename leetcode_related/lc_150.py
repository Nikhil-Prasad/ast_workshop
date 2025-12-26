"""

Some relevant leetcode problems as I'm building the notational logic for the AST and the Parser

Problem Spec: 

You are given an array of strings tokens that represents an arithmetic expression in a Reverse Polish Notation.

Evaluate the expression. Return an integer that represents the value of the expression.

Note that:

The valid operators are '+', '-', '*', and '/'.
Each operand may be an integer or another expression.
The division between two integers always truncates toward zero.
There will not be any division by zero.
The input represents a valid arithmetic expression in a reverse polish notation.
The answer and all the intermediate calculations can be represented in a 32-bit integer.
 

Example 1:

Input: tokens = ["2","1","+","3","*"]
Output: 9
Explanation: ((2 + 1) * 3) = 9
Example 2:

Input: tokens = ["4","13","5","/","+"]
Output: 6
Explanation: (4 + (13 / 5)) = 6
Example 3:

Input: tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
Output: 22
Explanation: ((10 * (6 / ((9 + 3) * -11))) + 17) + 5
= ((10 * (6 / (12 * -11))) + 17) + 5
= ((10 * (6 / -132)) + 17) + 5
= ((10 * 0) + 17) + 5
= (0 + 17) + 5
= 17 + 5
= 22
 

Constraints:

1 <= tokens.length <= 104
tokens[i] is either an operator: "+", "-", "*", or "/", or an integer in the range [-200, 200].


Solution Logic: 

You are essentially building an operator model similar to my AST BinOP. The job is just translating the notation into a place where you can correctly figure out if something is a number or an operator. 

To do this you iterate through the token list. If it is an operator, you know that it is middle. You can take the numbers left and right of it, and then operate on them. But if you try to keep a running total or something, you're not going to be able to deal with intermediate results from * or adition or whatever. 

So the way to do this is to have a stack. IF its a number, you add it to the stack. If you see an operator, based on the problem, you know that the item has to pop the last two items off of the stack and operate on it. Then you add that to the stack. 

This treats the stack as a sort of running accumulator. The end result is the final value. 

The rest is very similar to the BinOP operation in @expr_ast.py 
"""

from typing import List

class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        total = []
        operators = ["+", "-", "*", "/"]
        for token in tokens:
            if token not in operators:
                total.append(int(token))
            if token in operators:
                right = total.pop()
                left = total.pop()
                if token == "+":
                    total.append(left + right)
                if token == "-":
                    total.append(left - right)
                if token == "*": 
                    total.append(left * right)
                if token == "/": 
                    total.append(int(left / right)) #problem specifies no floats/decimals
        return total[0]