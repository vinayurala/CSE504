import sys
from ply.yacc import *
from parser import *
from gencode import *
from liveness import *
from MIPS import *

if (len(sys.argv) != 2):
    print "Usage: python " + sys.argv[0] + " <Protofilename>"
    sys.exit(-1)

try:
    f = open(sys.argv[1], "r")
    lines = f.read()
except IOError:
    print "File " + sys.argv[1] + " not found!!"
    sys.exit(-1)

line_str = "".join(lines)
astRoot = yacc.parse(line_str)

ismain(astRoot,done)
if done[0] == 0:
    print "Main function ERROR: Main Function Not WellFormed"
    sys.exit(-1)

isreturn(astRoot)

find(astRoot)
findfunc(astRoot)
declareonce(astRoot,decl,parent)

wellformed(astRoot,decl,defined,classobj, candidate)
welltyped(astRoot, vars, classobj)

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
argColorList = list()
functions = list()
for icLines in all_lines:
    icLines = icLines[::-1]
    (inSets, outSets, func_name) = final_liveness(icLines)
    inSets = inSets[::-1]
    outSets = outSets[::-1]
    intGraph = buildInterferenceGraph(inSets, outSets)
    (coloredList, spilledList, argColorMap) = graphColoring(intGraph, 1, icLines, inSets, outSets, tID, 0)
    tLines = list()
    inSets = outSets = list()
    tLines = gencode_blocks[:]
    for var in spilledList:
        (gencode_blocks, tID) = modifyIC(tLines, var, tID)
    coloredMapList.append(coloredList)
    spilledMapList.append(spilledList)
    argColorList.append(argColorMap)
    functions.append(func_name)
    coloredList = spilledList = list()
    argColorMap = dict()

asmLines = list()
mipsLines = list()
data_section_list = list()
spilledVarsList = list()
idx = 0
scratchText = mipsTemplate["space"] + "\n"
asmLines.append(scratchText)
scratchText = str(".data\nerror_stmt: .asciiz \"Array out of bounds!!!\"\n")
asmLines.append(scratchText)
scratchText = ".text\n"
asmLines.append(scratchText)

for icLines in all_lines:
    coloredList = coloredMapList[idx]
    spilledList = spilledMapList[idx]
    argsColor = argColorList[idx]
    func_name = functions[idx]
    idx += 1
    init_reg_map()
    (mipsLines, data_section, spilledVars) = genMIPSCode(icLines, coloredList, spilledList, argsColor, func_name)
    asmLines.append(mipsLines)
    data_section_list.append(data_section)

asmLines.append(mipsTemplate["exit"])
scratchText = str(".data\n")
asmLines.append(mipsTemplate["bounds_error"])
asmLines.append(scratchText)

asmLines.append(scratchText)
for data_section in data_section_list:
    if data_section:
        asmLines.append(data_section)
        if spilledVars:
            scratchText = str()
            for var in spilledVars:
                scratchText += spilledVars[var] + ":\t .word 0\n"

fileName = sys.argv[1]
(targetFile, _) = fileName.split('.', 2)
targetFile += ".asm"
f1 = open(targetFile, "w")
for line in asmLines:
    line_str = "".join(line)
    f1.write(line_str)
f1.close()


