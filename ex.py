import re

def tokenize(expr):
    token_spec = r'\d+|[()+\-*/]'
    return re.findall(token_spec, expr.replace(' ', ''))

class ASTNode:
    def __init__(self, op=None, left=None, right=None, value=None):
        self.op = op            # Operator: '+', '-', '*', '/' (or None for value node)
        self.left = left        # Left child (ASTNode)
        self.right = right      # Right child (ASTNode)
        self.value = value      # Integer value for leaf node

    def is_leaf(self):
        return self.op is None

    def __repr__(self):
        if self.is_leaf():
            return f"Int({self.value})"
        else:
            return f"Expr({self.op}, {repr(self.left)}, {repr(self.right)})"

def to_cpp_tmp(node):
    if node.is_leaf():
        return f"Int<{node.value}>"
    else:
        # Map Python operators to Tessellator types
        op_map = {
            '+': 'Add',
            '-': 'Sub',
            '*': 'Mul',
            '/': 'Div'
        }
        op_type = op_map[node.op]
        left_code = to_cpp_tmp(node.left)
        right_code = to_cpp_tmp(node.right)
        return f"Expr<{op_type}, {left_code}, {right_code}>"

def build_cpp_program(expr_code):
    return f"""
#include "meta_func.hpp"
#include <iostream>

using ExprType = {expr_code};
constexpr int result = Eval<ExprType>::result::value;

int main() {{
    std::cout << "Result: " << result << std::endl;
    return 0;
}}
"""

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self):
        tok = self.peek()
        self.pos += 1
        return tok

    def parse(self):
        return self.parse_expr()

    def parse_expr(self):  # handles '+' and '-'
        node = self.parse_term()
        while self.peek() in ('+', '-'):
            op = self.consume()
            right = self.parse_term()
            node = ASTNode(op=op, left=node, right=right)
        return node

    def parse_term(self):  # handles '*' and '/'
        node = self.parse_factor()
        while self.peek() in ('*', '/'):
            op = self.consume()
            right = self.parse_factor()
            node = ASTNode(op=op, left=node, right=right)
        return node

    def parse_factor(self):
        tok = self.peek()
        if tok == '(':
            self.consume()
            node = self.parse_expr()
            if self.consume() != ')':
                raise ValueError("Missing closing parenthesis")
            return node
        elif tok.isdigit():
            self.consume()
            return ASTNode(value=int(tok))
        else:
            raise ValueError(f"Unexpected token: {tok}")

expr = ASTNode(
    op='*',
    left=ASTNode(value=7),
    right=ASTNode(
        op='+',
        left=ASTNode(value=4),
        right=ASTNode(value=3)
    )
)
print(build_cpp_program(to_cpp_tmp(expr)))
expr_str = "7 * (2 + 3)"
tokens = tokenize(expr_str)
parser = Parser(tokens)
ast = parser.parse()
print(build_cpp_program(to_cpp_tmp(ast)))
