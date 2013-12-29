# -*- coding: UTF-8 -*-
"""
your file description here
"""
import re
import sys
from pygments.lexers import PythonLexer
from pygments.token import Punctuation, Comment

if __name__ == "__main__":
    lexer = PythonLexer()
    pattern = re.compile(u".*(given|and_|when|then)\((.+)")
    steps = [] 
    print "# -*- coding: UTF-8 -*-"
    print "from pyfeature import step"
    for l in sys.stdin.xreadlines():
        m = pattern.match(l)
        if m:
            s = lexer.get_tokens(m.group(2)) 
            desc = ""
            for t in s:
                if t[0] != Punctuation and t[1] != u",":
                    desc += "".join(chr(c) for c in [ord(b) for b in t[1]])
                else:
                    break
            steps.append([desc.strip()])
            omit_next_token = False
            for t in s:
                if t[1] == "=":
                    omit_next_token = True
                elif not omit_next_token and t[1] != "," and t[1] != ")" and t[0] != Comment:
                    steps[-1].append(t[1])
                else:
                    omit_next_token = False
            
    for i in xrange(len(steps)):
        step = steps[i]
        print '\n\n@step(\'%s$\')' % step[0].strip('\'"')
        print 'def _%d(%s):' % (i, ', '.join(t.strip() for t in ["step"] + step[1:] if t.strip()) if len(step) > 1 else "")
        print '    pass'

