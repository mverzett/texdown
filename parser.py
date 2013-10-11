from lexer import tokens
from pdb import set_trace
import logging
import sys

start = 'md'    # the start symbol in our grammar
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class struct(object):
    def __init__(self, entries): 
        self.__dict__.update(entries)

    def __repr__(self):
        return 'struct('+self.__dict__.__repr__()+')'

def p_md(p):
    'md : slide NEWLINE NEWLINE md'
    logging.debug(sys._getframe().f_code.co_name)
    p[0] = [p[1]] + p[4]

def p_md_newline(p):
    'md : NEWLINE md'
    logging.debug(sys._getframe().f_code.co_name)
    p[0] = p[2]
    
def p_md_empty(p):
    'md : '
    logging.debug(sys._getframe().f_code.co_name)
    p[0] = [ ]

def p_slide(p):
    'slide : ENVIRON NEWLINE content'
    logging.debug(sys._getframe().f_code.co_name)
    p[0] = struct({'type':'slide', 'master':p[1], 'content':p[3]})

def p_content(p):
    'content : elem content'
    logging.debug(sys._getframe().f_code.co_name)
    p[0] = [p[1]] + p[2]

def p_content_empty(p):
    'content : '
    logging.debug(sys._getframe().f_code.co_name)
    p[0] = []

def p_elem_title(p):
    'elem : DOUBLEHASH PLAINTEXT DOUBLEHASH NEWLINE'
    logging.debug(sys._getframe().f_code.co_name)
    p[0] = struct({'type':'title', 'content':p[2]})

def p_elem_atrribute(p):
    'elem : ATTRIBUTE PLAINTEXT NEWLINE'
    logging.debug(sys._getframe().f_code.co_name)
    p[0] = struct({'type':'attribute', 'keyword':p[1], 'content':p[2].strip()})

def p_elem_text(p):
    'elem : text' #WORD NEWLINE'
    logging.debug(sys._getframe().f_code.co_name)
    p[0] = struct({'type':'text', 'content':p[1]})

def p_text(p):
    'text : text text'
    logging.debug(sys._getframe().f_code.co_name)
    p[0] = p[1]+p[2]

def p_text_plain(p):
    'text : PLAINTEXT'
    logging.debug(sys._getframe().f_code.co_name)
    p[0] = [struct({'type':'plaintext', 'content':p[1]})] #FIXME: make sure \b \t... are properly parsed as LaTex rather than tab and so on

def p_text_plainnewline(p):
    'text : PLAINTEXT NEWLINE'
    logging.debug(sys._getframe().f_code.co_name)
    p[0] = [struct({'type':'plaintext', 'content':p[1]+p[2]})]

#def p_text_plainnewline2(p):
#    'text : PLAINTEXT NEWLINE PLAINTEXT'
#    logging.debug(sys._getframe().f_code.co_name)
#    p[0] = [struct({'type':'plaintext', 'content':''.join(p[1:])})]

def p_text_bullet(p):
    'text : BULLET text NEWLINE'
    logging.debug(sys._getframe().f_code.co_name)
    indent = len(p[1].split('*')[0])/2 -1
    p[0] = [struct({'type':'bullet', 'indent':indent, 'content':p[2].strip()+p[3]})]

def p_bold(p):
    'text : BOLD PLAINTEXT BOLD'
    p[0] = [struct({'type':'bold', 'content':p[2]})]

def p_italic(p):
    'text : ITALIC PLAINTEXT ITALIC'
    p[0] = [struct({'type':'italic', 'content':p[2]})]

def p_error(p):
    print("Syntax error at '%s'" % repr(p)) #p.value)

import ply.yacc as yacc
parser = yacc.yacc()

if __name__ == '__main__':
    from lexer import lexer
    import pprint
    import sys
    input_string = open(sys.argv[-1]).read()
    lexer.input(input_string)
    parse_tree = parser.parse(lexer=lexer)
    pprint.pprint( parse_tree )
