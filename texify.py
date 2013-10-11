# /bin/env python

import sys
from lexer import lexer
from parser import parser
import textools as masters
from pdb import set_trace

md_name   = 'test.md' #sys.argv[-2]
#templates = sys.argv[-1]
#templates = templates.strip('.py')
#module    = __import__(templates)


if __name__ == '__main__':
    md_file = open(md_name).read()
    lexer.input(md_file)
    parse_tree = parser.parse(lexer=lexer)
    tex_name = md_name.replace('md', 'tex')
    with open(tex_name,'w') as output:
        output.write(masters.header)
        for slide in parse_tree:
            if hasattr(masters, slide.master):
                int_slide = hasattr(masters, slide.master)(slide)
                output.write(int_slide)
            else:
                raise AttributeError('No master slide named %s available in the theme collection' % slide.master)

