import re
import subprocess
import time

# === Tokenizer ===
def tokenize(expr):
    token_spec = r'\d+|[()+\-*/]'
    return re.findall(token_spec, expr.replace(' ', ''))

# === AST Node ===
class ASTNode:
    def __init__(self, op=None, left=None, right=None, value=None):
        self.op = op
        self.left = left
        self.right = right
        self.value = value

    def is_leaf(self):
        return self.op is None

# === Parser ===
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

    def parse_expr(self):
        node = self.parse_term()
        while self.peek() in ('+', '-'):
            op = self.consume()
            right = self.parse_term()
            node = ASTNode(op=op, left=node, right=right)
        return node

    def parse_term(self):
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
            return ASTNode(value=int(self.consume()))
        else:
            raise ValueError(f"Unexpected token: {tok}")

# === TMP Code Generator ===
def to_cpp_tmp(node):
    if node.is_leaf():
        return f"Int<{node.value}>"
    op_map = {'+': 'Add', '-': 'Sub', '*': 'Mul', '/': 'Div'}
    left_code = to_cpp_tmp(node.left)
    right_code = to_cpp_tmp(node.right)
    return f"Expr<{op_map[node.op]}, {left_code}, {right_code}>"

# === Final C++ Builder ===
def build_cpp_program(expr_code):
    return f"""
#include "meta_func.hpp"
#include <iostream>
#include <limits>

using ExprType = {expr_code};
constexpr int result = Eval<ExprType>::result::value;

int main() {{
    std::cout << "Result: " << result << std::endl;
    // Wait for Enter key to close
    std::cout << "Press Enter to exit...";
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\\n');
    return 0;
}}
"""

# === Full Pipeline ===
def compile_and_run(expression):
    tokens = tokenize(expression)
    parser = Parser(tokens)
    ast = parser.parse()
    cpp_expr = to_cpp_tmp(ast)
    cpp_code = build_cpp_program(cpp_expr)

    with open("generated.cpp", "w") as f:
        f.write(cpp_code)
    subprocess.run(["g++", "generated.cpp", "-o", "result"])
    start_time = time.time()
    subprocess.run(["./result"])
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Subprocess execution time: {execution_time:.10f} seconds")

# === Try It! ===
if __name__ == "__main__":
    expr = input("Enter arithmetic expression: ")
    compile_and_run(expr)
