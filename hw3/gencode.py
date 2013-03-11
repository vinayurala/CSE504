import sys

from parser import *

blocks = list()
block = list()
braceCount = 0

def parsetree(node):
    global blocks
    global braceCount
    if node.leaf == None:
        for child in node.children:
            parsetree(child)
    else:
        for child in node.children:
            parsetree(child)

        block.append(str(node.leaf))

        if node.leaf == "{":
            braceCount += 1
        if node.leaf == "}":
            if (braceCount > 1):
                braceCount -= 1
            else:
                braceCount = 0
                blocks.append(block[:])
                del block[:]
        elif node.leaf == ";":
            del block[-1]
            if "{" in block:
                return
            else:
                blocks.append(block[:])
                del block[:]


    return

def genSimExpr(expr, tempIdx):
    tvar = "t"
    temp_stack = list()
    if not "if" in expr and not "while" in expr:
        expr = expr[::-1]
    line = str()                
    blk = list()
    blk_list = list()
    for t in expr:
        if t == "{" or t == "}":
            pass
        elif not t in ["+", "-", "*", "/", "%", "=", "print", "UMINUS", "if", "else", "while"]:
            temp_stack.append(t)
        else:
            if t == "=":
                t1 = temp_stack.pop()
                t2 = temp_stack.pop()
                line += str(t1) + " " + t + " " + str(t2) + "\n"

            elif t == "UMINUS":
                t1 = temp_stack.pop()
                line += tvar
                tempIdx += 1
                line += str(tempIdx) + " = " + "neg " + t1 + "\n"
                temp_stack.append(tvar + str(tempIdx))

            elif t == "if":
                line += "if "
                if len(temp_stack) > 1:
                    t1 = temp_stack.pop()
                    t2 = temp_stack.pop()
                    t3 = temp_stack.pop()
                    line += str(t2) + " " + str(t1) + " " + str(t3) + ":\n"

                else:
                    t1 = temp_stack.pop();
                    line += str(t1) + ":\n"

            elif t == "else":
                line += "else:\n"
                
            elif t == "print":
                t1 = temp_stack.pop()
                
            else:
                t1 = temp_stack.pop()
                t2 = temp_stack.pop()
                line += tvar 
                tempIdx += 1
                line += str(tempIdx) + " = " + str(t1) + " " +  t + " " + str(t2) + "\n"
                temp_stack.append(tvar + str(tempIdx))

    return (line, tempIdx)

def extract_simexprs(blk):
    open_indices = [i for i, x in enumerate(blk) if x == "{"]
    close_indices = [i for i, x in enumerate(blk) if x == "}"]

    simblk = blk[(max(open_indices) + 1): min(close_indices)]
    del blk[max(open_indices) : (min(close_indices) + 1)]

    if_indices = [i for i, x in enumerate(blk) if x == "if"]
    if_condn = blk[(max(if_indices) + 1) : max(open_indices)]
    if_condn.insert(0, "if")
    del blk[(max(if_indices)) : max(open_indices)]

    return (blk, simblk, if_condn)
    

def gencode(astRoot):
    tIdx = 1
    parsetree(astRoot)
    for blks in blocks:
        print blks

    ic_lines = list()
    tempStack = list()
    nestedBlks = list()
    currBlk = list()
    for blk in blocks:
        #if not "if" in blk and not "while" in blk:
        (simExpr, tIdx) = genSimExpr(blk, tIdx)
        ic_lines.append(simExpr)
        """
        elif "if" in blk:
            scratchBlk = blk[:]
            while scratchBlk:
                (scratchBlk, simblk, ifcondn) = extract_simexprs(scratchBlk)
                (simExpr, tIdx) = genSimExpr(ifcondn, tIdx)
                ic_lines.append(simExpr)
                (simExpr, tIdx) = genSimExpr(simblk, tIdx)
                ic_lines.append(simExpr)
        """        

    for lines in ic_lines:
        print lines

    return blocks


if __name__ == "__main__":
    gencode(blocks)
