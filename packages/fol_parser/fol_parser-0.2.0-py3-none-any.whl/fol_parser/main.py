import sys
from antlr4 import *
from ANTLR.FOLLexer import FOLLexer
from ANTLR.FOLParser import FOLParser
from antlr4.tree.Tree import ParseTreeWalker
from antlr4.tree.Trees import Trees
from graphviz import Digraph

def add_nodes_edges(t, dot, parser):
    text = Trees.getNodeText(t, ruleNames=parser.ruleNames)
    if t.getChildCount() == 0:
        dot.node(str(id(t)), text)
    else:
        dot.node(str(id(t)), text)
        for child in t.getChildren():
            dot.edge(str(id(t)), str(id(child)))
            add_nodes_edges(child, dot, parser)

def main():
    input_stream = FileStream("test.pl") 
    lexer = FOLLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = FOLParser(stream)
    
    tree = parser.p_text()
    print(tree.toStringTree(recog=parser))

    dot = Digraph(comment='Parse Tree')
    add_nodes_edges(tree, dot, parser)
    dot.render('graphs/parse_tree.gv', view=True)  

if __name__ == "__main__":
    main()
