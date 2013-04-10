from gencode import *
from parser import *

def liveness (icLines):
    useSet = set()
    defSet = set()
    inSet = set()
    outSet = set()
    rhsVars = []
    tList = []

    for line in icLines:
        if not inSet:
            pass
        else:
            outSet = inSet
        useSet = set()
        inSet = set()
        defSet = set()
        if "store" in line or "load" in line:
            if "load" in line:
                (lhs, _) = line.split('=', 2)
                lhs = lhs.replace(" ", "")
                defSet.add(lhs)
            else:
                continue
        elif not "print" in line:
            (lhs, rhs) = line.split('=', 2)
            lhs = lhs.replace(" ", "")
            defSet.add(lhs)
            rhsVars = rhs.split()
            for var in rhsVars:
                if not var in ["+", "-", "*", "/", "%", "neg"] and not var.isdigit() and var != "input":
                    var = var.replace(" ", "")
                    useSet.add(var)
        else:
            tList = tokenize.generate_tokens(cStringIO.StringIO(line).readline)
            for t in tList:
                if t[0] == 1 and t[1] != "print":
                    useSet.add(t[1])
        
        inSet = useSet.union(outSet.difference(defSet))
        inSets.append(inSet)
        outSets.append(outSet)  
