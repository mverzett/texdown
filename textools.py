
def texify_text(text):
    retval = ''
    indent = -1
    for item in text.content:
        if item.type == 'plaintext':
            if indent > -1:
                retval += '\end{itemize}\n'
                indent = -1
            retval += item.content
        elif item.type == 'bullet':
            if item.indent > indent:
                retval += '\\begin{itemize}\n'
                indent = item.indent
            elif item.indent < indent:
                retval += '\end{itemize}\n'
                indent = item.indent
            retval += '\\item ' + item.content
        elif item.type == 'bold':
            retval += '\\textbf{%s}' % item.content
        elif item.type == 'italic':
            retval += '\\textit{%s}' % item.content
        else:
            raise ValueError('Parsed object type "%s" not recognized' % item.type)
    return retval

header = '''
\\documentclass{beamer}
\\begin{document}
\\date{\today} 
'''

class Slide(object):
    def __init__(self, parsed_struct):
        titles = [i for i in parsed_struct.content if i.type == 'title']
        if len( titles ) > 1:
            raise AttributeError('multiple title assignment! for slide %s' % titles) #FIXME, should go in the parser
        self.title = titles[0] if titles else None
        text  = sum([i for i in parsed_struct.content if i.type == 'text'],[]) #join them in case they are split (not probable)
        self.text = texify_text(text)
        self.attributes = digest_attributes(parsed_struct.content)

    def tex_title(self):
        return '\\frametitle{%s}' % self.title

    def digest_attributes(content_list):
        attr_dict = {}
        for i in content_list:
            if i.type == 'attribute':
                if i.keyword not in attr_dict:
                    attr_dict[i.keyword] = i.content
                else:
                    if isinstance(attr_dict[i.keyword], list):
                        attr_dict[i.keyword].append(i.content)
                    else:
                        attr_dict[i.keyword] = [ attr_dict[i.keyword], 
                                                 i.content]
        return attr_dict


class Title(Slide):
    def __init__(self, p):
        super(Title, self).__init__(p)
    
    def __repr__(self):
        return '''\\title{%s}   
        \\author{%s} 
        \\frame{\\titlepage} 
        ''' % (self.title, self.text)

class Text_and_pic(Slide):
    def __init__(self, p):
        super(Text_and_pic, self).__init__(p)
    
    def __repr__(self):
        return ''' 
        \\frame{
        %s
        \\begin{columns}
        \\begin{column}{0.5\textwidth}
        %s
        \\end{column}
        \\begin{column}{0.5\textwidth}
        \\begin{figure}
        \\includegraphics[angle=-0,width=\textwidth]{%s} 
        \\end{figure}
        \\end{column}
        \\end{columns}
        } 
        ''' % (self.tex_title(), self.text, self.attributes['picture'].strip())
        #\\caption{show an example picture}


class Text(Slide):
    def __init__(self, p):
        super(Title, self).__init__(p)
    
    def __repr__(self):
        return ''' 
        \\frame{%s
        %s
        } 
        ''' % (self.tex_title(), self.text)


