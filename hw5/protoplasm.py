import sys
from ply.yacc import *
from parser import *
from gencode import *
from liveness import *
#from mipsCode import *

if (len(sys.argv) != 2):
    print "Usage: python " + sys.argv[0] + " <Protofilename>"
    sys.exit(-1)

try:
    f = open(sys.argv[1], "r")
    astRoot = yacc.parse(f.read())
except IOError:
    print "File " + sys.argv[1] + " not found!!"
    sys.exit(-1)

#wellformed(astRoot, decl, defined, classobj)
#print "AST wellformed"
gencode_blocks = final_codegen(astRoot)

function_lines = list()
all_lines = list()
for line in gencode_blocks:
    if line == "}\n" or line == "}":
        function_lines.append(line)
        all_lines.append(function_lines[:])
        del function_lines[:]
    elif line == "\n":
        pass
    else:
        function_lines.append(line)

coloredMapList = list()
spilledMapList = list()
for icLines in all_lines:
    icLines = icLines[::-1]
    (inSets, outSets) = final_liveness(icLines)
    intGraph = buildInterferenceGraph(inSets, outSets)
    (coloredList, spilledList) = graphColoring(intGraph, 1, icLines, inSets, outSets, tID, 0)
    tLines = list()
    tLines = gencode_blocks[:]
    for var in spilledList:
        (gencode_blocks, tID) = modifyIC(tLines, var, tID)
    coloredMapList.append(coloredList)
    spilledMapList.append(spilledList)

idx = 0
for coloredList in coloredMapList:
    print "ColoredList[" + str(idx) + "]:"
    idx += 1
    print coloredList
print "Spilled lists: "
for spilledList in spilledMapList:
    print spilledList
'''        
asmLines = genMIPSCode(gencode_blocks, coloredList, spilledList)
fileName = sys.argv[1]
(targetFile, _) = fileName.split('.', 2)
targetFile += ".asm"
f1 = open(targetFile, "w")
for line in asmLines:
    f1.write(line)
f1.close()
print "Compilation succeeded and output written to " + str(targetFile)
'''
