from gencode import *
from parser import *
import cStringIO, tokenize

inSets = list()
outSets = list()

def liveness (icLines):
    useSet = set()
    defSet = set()
    inSet = set()
    outSet = set()
    global inSets
    global outSets
    rhsVars = []
    tList = []

    for line in icLines:
        if line == '':
            continue

        if "if not" in line or "goto" in line or "label" in line or "}" in line or "{" in line or "new" in line:
            continue

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
            if '==' in line:
                idx = line.index('=')
                lhs = line[0:idx]
                rhs = line[idx+1:len(line)]
            else:
                (lhs, rhs) = line.split('=', 2)

            lhs = lhs.replace(" ", "")
            defSet.add(lhs)
            rhsVars = rhs.split()
            for var in rhsVars:
                if not var in ["+", "-", "*", "/", "%", "neg", "not", "&&", "||", ">", "<", ">=", "<=", "==", "!="] and not var.isdigit() and var != "input":
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


def final_liveness (icLines):
    liveness(icLines)
    return (inSets, outSets)

if __name__ == "__main__":
    (inSets, outSets) =  liveness(icLines)
    print "Insets :"
    print inSets
    print "Outsets: "
    print outSets

