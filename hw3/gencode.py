import sys

from parser import result

blocks = list()

def parsetree(node):
    block = list()
    if node.leaf == None:
        pass
    else:
        if not node.leaf in ["if", "while"]:
            block.append(node.leaf)
            for child in node.children:
                parsetree(child)
        else:
            for child in node.children:
                parsetree(child)
            
            block.append(node.leaf)


def gencode(blocks):
    
    return 
