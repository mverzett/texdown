tokens = ( #SYM == SYMBOL
    'ENVIRON',
    'ATTRIBUTE', 
    'DOUBLEHASH', 
    'BULLET',
    'PLAINTEXT',
#    'WHITESPACE',
    'NEWLINE',
    'BOLD',
    'ITALIC',
    )

# Tokens
def t_eolcomment(t):
    r'%.*'
    pass

def t_ENVIRON(t):
    r'@[A-Za-z][A-Za-z0-9_]*\ *'
    t.value = t.value[1:].strip()
    return t

def t_ATTRIBUTE(t):
    r'&[A-Za-z][A-Za-z0-9_]*\ *'
    t.value = t.value[1:].strip()
    return t

def t_DOUBLEHASH(t):
    r'\#\#'
    return t

def t_BULLET(t):
    r'\ \ +\*'
    return t

def t_BOLD(t):
    r'\*\*'
    return t

def t_ITALIC(t):
    r'__'
    return t

#def t_WHITESPACE(t):
#    r'[ \t\v\r]'
#    return t

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t

def t_PLAINTEXT(t):
    r'(?:[^\n\*\_\#%]|\*(?!\*)|_(?!_)|\#(?!\#))+'#'(?:[^\s\*\_]|\*(?!\*)|_(?!_))+'
    return t

#t_ignore = ' \t\v\r'


def t_error(t):
    raise ValueError('Lexical error: "' + str(t.value[0]) + '" in line ' + str(t.lineno))
#    #t.lexer.skip(1)

import ply.lex as lex
lexer = lex.lex()

if __name__ == '__main__':
    lexer.input(open('test2.md').read())
    counter = 0
    tok = lexer.token()
    while tok:
        if not tok:
            break
        print tok
        counter += 1
        tok = lexer.token()
