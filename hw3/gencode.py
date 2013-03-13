import sys

from parser import *

blocks = list()
block = list()
braceCount = 0
labelID = 1

def parsetree(node):
    global blocks
    global braceCount
    
    if not node.leaf == None:
        block.append(str(node.leaf))
    for child in node.children[:]:
        parsetree(child)

    if node.leaf == "{":
        braceCount += 1
    elif node.leaf == "}":
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
    global labelID
    label = "label"
    expr = expr[::-1]
    line = str()                
    blk = list()
    blk_list = list()
    if_line = str()
    for t in expr:
        if t == "{":
            if "while" in expr:
                tStr = "label " + str(labelID) + ":\n"
                line = tStr + line
            else:
                pass
        elif t == "}":
            if "if" in expr:
                line += t + "\n"
            else:
                pass
            
        elif not t in ["+", "-", "*", "/", "%", "=", "print", "UMINUS", "if", "else", "while", "&&", "||", "<=", ">=", "==", "!=", ">", "<"]:
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
                t1 = temp_stack.pop();
                line += "if "
                line += str(t1) + " :\n"

            elif t == "while":
                t1 = temp_stack.pop()
                if_line += "if " + str(t1) + " goto label " + str(labelID) + "\n"
                labelID += 1

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

    if "while" in expr:
        line += if_line

    blk = line.split("\n")
    blk = filter(None, blk)
    if "if" in line and not "while" in expr:
        blk = blk[::-1]
        if_indices = [blk.index(s) for s in blk if (s.startswith("if") and s.find("goto") == -1)]
        for t in if_indices:
            blk[t], blk[t+1] = blk[t+1], blk[t]
        
        brace_idx = list()

        t = 0
        while t in range(len(blk)):
            if ((blk[t].startswith("if")) and (blk[t].find("goto") == -1)):
                for i in range(len(blk)):
                    if blk[i] == "}": 
                        brace_idx.append(i)

                (_, condn_str, _) = blk[t].split(" ")
                tStr1 = "if not "
                tStr2 = "goto label" + str(labelID)
                blk.insert(t, tStr1 + condn_str + " " + tStr2)
                blk[max(brace_idx) + 1] = "label" + str(labelID) + ":" 
                del brace_idx[-1]
                labelID += 1
                t += 2
            else:
                t += 1
        
    return (blk, tempIdx)

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
        (simExpr, tIdx) = genSimExpr(blk, tIdx)
        ic_lines.append(simExpr)

    print "Blocks: "
    for lines in ic_lines:
        print lines

    return blocks


if __name__ == "__main__":
    gencode(blocks)
