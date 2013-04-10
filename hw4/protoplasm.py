import sys
from ply.yacc import *
from parser import *
from gencode import *
from liveness import *

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
print "Blocks :"
for blk in gencode_blocks:
    print blk
icLines = gencode_blocks[::-1]
icLinesStr = ''.join(icLines)
icLines = icLinesStr.split('\n')
icLines = filter(None, icLines)
gencode_blocks = icLines[::-1]
#print "Blocks :"
#for blk in gencode_blocks:
#    print blk
(inSets, outSets) = final_liveness(icLines)
print "Insets: "
print inSets
print "OutSets: "
print outSets
