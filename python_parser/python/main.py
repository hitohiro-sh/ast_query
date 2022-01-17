import sys
import json

from antlr4 import *
#from antlr4 import 
from Python3Lexer import Python3Lexer
from Python3Parser import Python3Parser

def context_path(trace : list[ParserRuleContext]) -> str:
    return "/".join([str(type(t)).replace("Python3Parser.Python3Parser.","") \
                        .replace("<class '", "") \
                        .replace("'>","") + ":{}:{}".format(t.start.line, t.stop.line) for t in trace])


def context_path_to_list(trace : list[ParserRuleContext]) -> str:
    return [str(type(t)).replace("Python3Parser.Python3Parser.","") \
                        .replace("<class '", "") \
                        .replace("'>","") + ":{}:{}".format(t.start.line, t.stop.line) for t in trace]

def tree_to_str(tree : ParserRuleContext) -> str:
    return f"type={type(tree)},text={tree.getText()}" + \
            f",start={tree.start},stop={tree.stop}"

def tree_to_dict(tree : ParserRuleContext) -> str:
    return {
        "type": f"{type(tree)}",
        "text": f"{tree.getText()}",
        "start": f"{tree.start}",
        "stop": f"{tree.stop}",
    }

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
        return tree_to_str(self.tree)
        
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
    if argv[1] == '--stdin':
        input_stream = StdinStream()
    else:
        input_stream = FileStream(argv[1])

    lexer = Python3Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Python3Parser(stream)
    tree = parser.file_input()

    if len(argv) > 2:
        o_type = argv[2]
    else:
        o_type = "text"
    
    def f_json(mem):
        tree = mem.tree
        depth = mem.depth

        #indent = ' ' * depth
        print(json.dumps([{"indent": depth, "context_path": context_path_to_list(mem.trace)},tree_to_dict(tree)]))        

    def f(mem):
        tree = mem.tree
        depth = mem.depth
        #depth = 0

        indent = ' ' * depth
        print('{}{}'.format(indent, context_path(mem.trace) + ',' + json.dumps(tree_to_dict(tree))))
        #print('{}{}'.format(indent, type(tree)))
        #print('{}{}'.format(indent, tree.getText()))
        #print('{}{}'.format(indent, tree.start))
        #print('{}{}'.format(indent, tree.stop))

    if o_type == "json":
        mem = TrMem(f_json)
    elif o_type == "text":
        mem = TrMem(f)

    tr(tree, 0, mem)

if __name__ == '__main__':
    main(sys.argv)
