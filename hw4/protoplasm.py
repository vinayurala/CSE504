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

#wellformed(astRoot, decl, defined)
print "AST wellformed"
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
print "Blocks :"
for blk in gencode_blocks:
    print blk
(inSets, outSets) = final_liveness(icLines)
#print "Insets: "
#print inSets
#print "OutSets: "
#print outSets
intGraph = buildInterferenceGraph(inSets, outSets)
#print "Interference graph: "
#print intGraph
(coloredList, spilledList) = graphColoring(intGraph, 1, icLines, inSets, outSets, tID, 0)
print "Colored List:"
#for k in coloredList:
#    print "Var: " + k + "  Reg: " + str(coloredList[k])
print coloredList
print "Spilled List: "
print spilledList
#for v in spilledList:
#    print v
tLines = list()
tLines = gencode_blocks[:]
for var in spilledList:
    (gencode_blocks, tID) = modifyIC(tLines, var, tID)
#if spilledList:
#    print "Modified IC Lines: "
#    for blk in gencode_blocks:
#        print blk
#asmCode = genMIPSCode(icLines, coloredList, spilledList)
#for line in asmCode:
#    print line
