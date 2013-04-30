from gencode import *
from parser import *
import cStringIO, tokenize
import re
import itertools

#inSets = list()
#outSets = list()
defined_var = set()
funcn_args = list()

rel_ops = ["&&", "||", "<", ">", "<=", ">=", "==", "!="]

def liveness (icLines):
    useSet = set()
    defSet = set()
    inSet = set()
    outSet = set()
    outSets = list()
    inSets = list()

    #global inSets
    #global outSets
    global defined_var
    global funcn_args

    rhsVars = []
    tList = []
    outSets = inSets = list()
    defined_var = set()
    
    ret_str = icLines.pop(1)
    ret_val = ret_str.split()
    if len(ret_val) > 1:
        if ret_val[1].isdigit():
            pass
        else:
            outSet.add(ret_val[1])

    args_str = icLines.pop(len(icLines)-1)
    lparen_idx = args_str.index('(')
    rparen_idx = args_str.index(')')
    args = args_str[lparen_idx+1:rparen_idx]
    idx = 0
    funcn_args = list()
    for arg in args:
        if arg is "," or arg is " ":
            pass
        else:
            if idx < 4:
                idx += 1
                funcn_args.append(arg)
            else:
                defined_var.add(arg)
        
    for line in icLines:
        if line == '':
            continue

        if "if not" in line or "goto" in line or "label" in line or "}" in line or "{" in line or "new" in line or ":" in line or "ret" in line or "call_" in line:
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
                defined_var.add(lhs)        
            else:
                continue
        elif not "print" in line:            
            if '==' in line or '!=' in line:
                idx = line.index('=')
                lhs = line[0:idx]
                rhs = line[idx+1:len(line)]
            else:
                (lhs, rhs) = line.split('=', 2)

            lhs = lhs.replace(" ", "")
            if not any(i in rhs for i in rel_ops) and not lhs in funcn_args:
                defSet.add(lhs)
                defined_var.add(lhs)        

            rhsVars = rhs.split()
            for var in rhsVars:
                if not var in ["+", "-", "*", "/", "%", "neg", "not", "&&", "||", "<", ">", ">=", "<=", "!=", "=="] and not var.isdigit() and var != "input":
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

    return (inSets, outSets)


def final_liveness (icLines):
    (inSets, outSets) = liveness(icLines)
    return (inSets, outSets)

def buildInterferenceGraph(inSets, outSets):
    graph = dict()
    varSet = set()
    for inSet in inSets:
        for var in inSet:
            if var and not var in funcn_args:
                varSet.add(var)
    for outSet in outSets:
        for var in outSet:
            if var and not var in funcn_args:
                varSet.add(var)
    
    varSet = varSet.union(set(defined_var))
    graph = dict.fromkeys(list(varSet))
    varList = list(varSet)
    for i1, i2 in itertools.combinations(varList, 2):
        tSet = set((i1, i2))
        for set1 in inSets:
            if (tSet.issubset(set1)):
                if graph[i1] is None:
                    graph[i1] = set()
                graph[i1].add(i2)
                if graph[i2] is None:
                    graph[i2] = set()
                graph[i2].add(i1)

    return graph


def modifyIC(lines, var, tempIdx):
    
    words = [w.find(var) for w in lines]
    tempIdx += 1
    tVar = "t" + str(tempIdx)
    storeVar = "store " + str(var)
    loadVar = str(tVar)+ " = load " + str(var)
    
    for w in words:
        if w > -1:
            idx = words.index(w)
            reVar = "\\b" + var + "\\b"
            exactMatches = re.findall(reVar, lines[idx])
            if not exactMatches:
                continue
            else:
                words.insert(words.index(w) + 1, -1)
                string = lines[idx]
                if("=" in string):
                    if(string.find(var) > string.find("=")):
                        lines.insert(idx, loadVar)
                        string = lines[idx + 1].replace(var, tVar)
                        del lines[idx + 1]
                        lines.insert(idx+1, string)
                    else:
                        lines.insert(idx + 1, storeVar)
                else:
                    if ("print" in string):
                        lines.insert(idx, loadVar)
                        string = lines[idx + 1].replace(var, tVar)
                        del lines[idx + 1]
                        lines.insert(idx+1, string)
                
                    else:
                        lines.insert(idx + 1, storeVar)

    return (lines, tempIdx)

def graphColoring(intGraph, reTryCount, ic_lines, inSets, outSets, tempIdx, lastRun):
    tStack = list()
    coloredList = []
    coloredList = dict.fromkeys(intGraph.keys())
    spilledList = []
    while (not all(intGraph[k] is None for k in intGraph)):
        nextKey = None
        flag = 1
        for keys in intGraph:
            if intGraph[keys] is None:
                continue
            if not flag:
                break
            if (len(intGraph[keys]) < 15):
                nextKey = keys
                flag = 0
        if(flag):
            nextKey = ""
            for k in intGraph:
                if not intGraph[k] is None:
                    if len(intGraph[k]) > len(nextKey):
                        nextKey = k

            
        edges = (nextKey, intGraph[nextKey])
        del intGraph[nextKey]
        tStack.append(edges)
        
    colorV = 0
    while tStack:
        (v, E) = tStack.pop()
        intGraph[v] = E
        flag = 1
        neighborColors = list()
        for e in E:
            neighborColors.append(coloredList[e])
        if neighborColors is None:
            flag = 0
        while(flag and colorV < 15):
            if colorV in neighborColors:
                colorV += 1
            else:
                flag = 0

        if(flag):
            spilledList.append(v)
        else:
            coloredList[v] = colorV
            colorV = (colorV + 1) % 15

    for keys in coloredList:
        if ((coloredList[keys] == None) and (not keys in spilledList)):
            coloredList[keys] = colorV 
            colorV = (colorV + 1) % 15
    
    argcolorList = dict()
    arg_regs = "$a"
    arg_ridx = 0
    for arg in funcn_args:
        argcolorList[arg] = arg_regs + str(arg_ridx)
        arg_ridx += 1

    return (coloredList, spilledList, argcolorList)


if __name__ == "__main__":
    with open("test1.ic") as f:
        lines = f.readlines()
    
    inSetList = list()
    outSetList = list()
    function_lines = list()
    all_lines = list()
    for line in lines:
        if line == "}\n":
            function_lines.append(line)
            all_lines.append(function_lines[:])
            del function_lines[:]
        elif line == "\n":
            pass
        else:
            function_lines.append(line)
            
    for icLines in all_lines:
        icLines = icLines[::-1]
        (inSets, outSets, argColorList) = final_liveness(icLines)
        inSets = inSets[::-1]
        outSets = outSets[::-1]
        inSetList.append(inSets)
        outSetList.append(outSets)
        ouSets = inSets = list()


    inSets = outSets = list()
    for (inSets, outSets) in (inSetList, outSetList):
        print "Insets :"
        print inSets
        print ""
        print "Outsets: "
        print outSets
        print ""
        
        intGraph = buildInterferenceGraph(inSets, outSets)
        (coloredList, spilledList, argColorList) = graphColoring(intGraph, 1, icLines, inSets, outSets, tID, 0)
        print "Colored List: "
        print coloredList
        print ""
        print "Spilled List: "
        print spilledList
        print ""

