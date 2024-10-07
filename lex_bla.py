import ply.lex as lex
import sys

# List of token names
tokens = (
    'ID',
    'BINARY_LITERAL',
    'A', 'S', 'M', 'D',  # Operators
    'EQUALS',  # '='
    'LPAREN', 'RPAREN',  # '(' ')'
    'WHITESPACE',
    'COMMENT',
    'ILLEGAL'
)

# Regular expression rules for simple tokens
t_A = r'A'
t_S = r'S'
t_M = r'M'
t_D = r'D'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'

# Functions defining the more complex token regular expressions, and formatting token output
def t_ID(t):
    r'[_a-z_][_a-z0-9]*'   # Regular expression
    t.value = f'ID,{t.value}'   # Format the token for output
    return t

def t_BINARY_LITERAL(t):
    r'[+-]?[10]+'   # optional + or - at the start
    t.value = f'BINARY_LITERAL,{t.value}'
    return t

# Rule for comments (either a long block or single-line)
def t_COMMENT(t):
    r'(/\*([^*]|\*+[^*/])*\*/)|(//[^\n]*)' # ^ - don't include the newline character
    t.value = f'COMMENT'
    return t
# def t_COMMENT(t):
#     r'(/\*([^*]|\*+[^*/])*\*/)|(//[^\n]*)'
#     pass  # Ignore comments

# Rule for whitespace (spaces, tabs, newlines, etc.)
def t_WHITESPACE(t):
    r'[ \t\n\r]+'
    t.value = 'WHITESPACE'
    return t
# def t_WHITESPACE(t):
#     r'[ \t\n\r]+'
#     pass  # Skip and ignore whitespace tokens


# Rule for illegal characters
def t_ILLEGAL(t):
    r'[^_a-zA-SD=\(\)01 \t\n\r/]+'
    t.value = f'ILLEGAL,{t.value}'
    return t

# Error handling rule (skips over illegal characters)
def t_error(t):
    print(f"Illegal character {t.value[0]}")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()



# Function to tokenize the file content
def tokenize_file(filename):
    try:
        with open(filename, 'r') as f:
            data = f.read()

        lexer.input(data)

        # Output to .tkn file
        output_filename = filename.replace('.bla', '.tkn')
        with open(output_filename, 'w') as token_file:
            for tok in lexer:
                print(tok.value)  # Print token to the console
                token_file.write(tok.value + '\n')  # Write token to the file

    except FileNotFoundError:
        print(f"Error: The file '{filename}' does not exist.")

# Entry point for the script
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: lex_bla.py <inputfile.bla>")
    else:
        tokenize_file(sys.argv[1])