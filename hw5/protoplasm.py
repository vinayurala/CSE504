import sys
from ply.yacc import *
from parser import *
from gencode import *
#from liveness import *
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
icLines = list()
tList = list()
for i in gencode_blocks:
    tList = i.split("\n")
    for t in tList:
        icLines.append(t)
icLines = filter(None, icLines)
icLines = icLines[::-1]
gencode_blocks = icLines[::-1]

(inSets, outSets) = final_liveness(icLines)
intGraph = buildInterferenceGraph(inSets, outSets)
(coloredList, spilledList) = graphColoring(intGraph, 1, icLines, inSets, outSets, tID, 0)
tLines = list()
tLines = gencode_blocks[:]
for var in spilledList:
    (gencode_blocks, tID) = modifyIC(tLines, var, tID)
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
