import sys
from antlr4 import *
#from antlr4 import 
from Python3Lexer import Python3Lexer
from Python3Parser import Python3Parser

def context_path(trace : list[ParserRuleContext]) -> str:
    return "/".join([str(type(t)).replace("Python3Parser.Python3Parser.","") \
                        .replace("<class '", "") \
                        .replace("'>","") + ":{}:{}".format(t.start.line, t.stop.line) for t in trace])

def to_str(tree : ParserRuleContext) -> str:
    return f"type={type(tree)},text={tree.getText()}" + \
            f",start={tree.start},stop={tree.stop}"

class ParseContextItem:
    def __init__(self, tree : ParserRuleContext, depth : int) -> None:
        self.tree = tree
        self.depth = depth
        self.type = type(tree)
        self.text = tree.getText()

        self.start = tree.start
        self.start_line = tree.start.line

        self.stop = tree.stop
        self.stop_line = tree.stop.line

    def array(self) -> list:
        return [self.depth, 
            self.type, 
            self.text, 
            self.start, self.stop, 
            self.start_line, self.stop_line]

    def __str__(self) -> str:
        return to_str(self.tree)
        
class TrMem:
    def __init__(self, func = None, trace = None) -> None:
        if trace != None:
            self.trace = trace
        else:
            self.trace = []
        self.func = func
        pass

    def set(self, tree : ParserRuleContext, depth : int) -> None:
        self.tree = tree
        self.depth = depth
        self.trace.append(tree)

    def call_func(self) -> None:
        if self.func != None:
            self.func(self)

    def clone(self) -> object:
        return TrMem(self.func, list(self.trace))






def tr(tree, depth, mem : TrMem):
    if not isinstance(tree, TerminalNode):
        #if isinstance(func, TrMem):
        mem.set(tree, depth)
        mem.call_func()
        #func(type(tree), depth)
        #func(tree.getText(), depth)
        #func(tree.start, depth)
        #func(tree.stop, depth)
        for i in range(tree.getChildCount()):
            child = tree.getChild(i)
            tr(child, depth+1, mem.clone())    

def main(argv):
    input_stream = FileStream(argv[1])
    lexer = Python3Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Python3Parser(stream)
    tree = parser.file_input()
    
    def f(mem):
        tree = mem.tree
        depth = mem.depth

        indent = ' ' * depth
        print('{}{}'.format(indent, context_path(mem.trace) + ',' + to_str(tree)))
        print('{}{}'.format(indent, type(tree)))
        print('{}{}'.format(indent, tree.getText()))
        print('{}{}'.format(indent, tree.start))
        print('{}{}'.format(indent, tree.stop))

    mem = TrMem(f)

    tr(tree, 0, mem)
 
if __name__ == '__main__':
    main(sys.argv)
