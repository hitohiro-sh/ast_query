import sys
from antlr4 import *
#from antlr4 import 
from Python3Lexer import Python3Lexer
from Python3Parser import Python3Parser


def tr(tree, depth, func):
    if not isinstance(tree, TerminalNode):
        func(type(tree), depth)
        func(tree.getText(), depth)
        func(tree.start, depth)
        func(tree.stop, depth)
        for i in range(tree.getChildCount()):
            child = tree.getChild(i)
            tr(child, depth+1, func)    

def main(argv):
    input_stream = FileStream(argv[1])
    lexer = Python3Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Python3Parser(stream)
    tree = parser.file_input()
    
    tr(tree, 0, lambda v, d: print('{}{}'.format(' ' * d, v)))
 
if __name__ == '__main__':
    main(sys.argv)
