# lexer.py

import re

# Define token patterns
TOKEN_TYPES = [
    ('COMMENT', r'//.*'),
    ('KEYWORD', r'\b(num|text|bool|cond|else|loop|for|break|func|return|show|true|false|sqrt)\b'),
    ('NUMBER', r'\b\d+\b'),
    ('STRING', r'\".*?\"'),
    ('ID', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
    ('OPERATOR', r'(\*\*|==|!=|<=|>=|&&|\|\||[+\-*/%^=><])'),
    ('SYMBOL', r'[;{}()\[\],]'),
    ('SKIP', r'[ \t]+'),
]

def tokenize(code):
    tokens = []
    
    for line_no, line in enumerate(code.split('\n'), start=1):
        position = 0
        
        while position < len(line):
            match = None
            
            for token_type, pattern in TOKEN_TYPES:
                regex = re.compile(pattern)
                match = regex.match(line, position)
                
                if match:
                    value = match.group(0)
                    
                    if token_type in ['SKIP', 'COMMENT']:
                        position = match.end(0)
                        break
                    tokens.append((token_type, value, line_no))                        
                    
                    position = match.end(0)
                    break
            
            if not match:
                print(f"Lexical Error at line {line_no}: {line[position]}")
                position += 1

    return tokens