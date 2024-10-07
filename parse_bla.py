import ply.yacc as yacc
import sys
from lex_bla_helper import tokens  # Import token definitions from the lexer


# Abstract Syntax Tree (AST) Node class
class ASTNode:
    def __init__(self, name, children=None):
        self.name = name
        self.children = children if children else []

    def add_child(self, child):
        self.children.append(child)

    def __str__(self, level=0):
        ret = "\t" * level + f"{self.name}\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

# Grammar rules
def p_program(p):
    """program : statement_list"""
    p[0] = ASTNode("Program", p[1])

def p_statement_list(p):
    """statement_list : statement_list statement
                      | statement"""
    if len(p) == 3:  # Two statements
        p[0] = p[1] + [p[2]]
    else:  # Single statement
        p[0] = [p[1]]

def p_statement(p):
    """statement : ID EQUALS expression"""
    p[0] = ASTNode("=", [ASTNode(f"{p[1]}"), p[3]])

def p_expression(p):
    """expression : expression A term
                  | expression S term
                  | term"""
    if len(p) == 4:
        p[0] = ASTNode(p[2], [p[1], p[3]])
    else:
        p[0] = p[1]

def p_term(p):
    """term : term M factor
            | term D factor
            | factor"""
    if len(p) == 4:
        p[0] = ASTNode(p[2], [p[1], p[3]])
    else:
        p[0] = p[1]

# def p_factor(p):
#     """factor : LPAREN expression RPAREN
#               | BINARY_LITERAL
#               | ID"""
#     if len(p) == 4:  # Parenthesized expression
#         p[0] = p[2]
#     else:
#         # Use only the value part directly
#         p[0] = ASTNode(f"{p.slice[1].type},{p[1]}")
def p_factor(p):
    """factor : LPAREN expression RPAREN
              | BINARY_LITERAL
              | ID"""
    if len(p) == 4:  # Parenthesized expression
        p[0] = p[2]
    else:
        p[0] = ASTNode(f"{p[1]}")  # Use the type and value correctly


def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' (line {p.lineno}, column {p.lexpos})")
    else:
        print("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()

def parse_file(filename):
    try:
        with open(filename, 'r') as f:
            data = f.read()
        result = parser.parse(data)

        if result:
            output_filename = filename.replace('.bla', '.ast')
            with open(output_filename, 'w') as ast_file:
                print(result)
                ast_file.write(str(result))

    except FileNotFoundError:
        print(f"Error: The file '{filename}' does not exist.")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: parse_bla.py <inputfile.bla>")
    else:
        parse_file(sys.argv[1])
