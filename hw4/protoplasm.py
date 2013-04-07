import sys
from ply.yacc import *
from parser import *
from gencode import *
#from liveness import *

if (len(sys.argv) != 2):
    print "Usage: python " + sys.argv[0] + " <Protofilename>"
    sys.exit(-1)

try:
    f = open(sys.argv[1], "r")
    astRoot = yacc.parse(f.read())
except IOError:
    print "File " + sys.argv[1] + " not found!!"
    sys.exit(-1)

wellformed(astRoot, decl, defined)
print "AST wellformed"
gencode_blocks = final_codegen(astRoot)
print "Blocks :"
for block in gencode_blocks:
    print block
#(inSets, outSets) = livenessanalysis(gencode_blocks)
