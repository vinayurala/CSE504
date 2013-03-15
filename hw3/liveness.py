#from gencode import *
import tokenize, cStringIO, StringIO

operators = ["+", "-", "*", "/", "%", "<", ">", "<=", ">=", "&&", "||", "print"]
inSets = set()
outSets = set()
tlist = list()

def flattenList(blocks):
    tlist1 = list()
    global tlist
    
    for tblk in blocks:
        if isinstance(tblk, list):
            tlist = flattenList(tblk)
        else:
            tlist.append(tblk)

    return tlist

def parseBlocks(blocks):
    defSet = set()
    useSet = set()
    defSets = list()
    useSets = list()

    tlist = flattenList(blocks)
    for expr in tlist:
        
        if any(operators in expr):
            if "=" in expr:
                (lhsVar, _ , rhsVars) = expr.split("=", 3)
                defSet.add(lhsVar)
                for var in rhsVars:
                    if not var in:
                        useSet.add(var)
            else "print" in expr:
                  tList = tokenize.generate_tokens(cStringIO.StringIO(line).readline)
                  for t in tList:
                      if t[0] == 1 and t[1] != "print":
                          useSet.add(t[1])
            

    return (defSet, useSet)

def livenessanalysis(blocks):
    (defSets, useSets) = parseBlocks(blocks)
    return (inSets, outSets)

if __name__ == "__main__":
    livenessanalysis(blocks)
