from liveness import *
from gencode import *

mipsCodeMap = {"+": "add", "-": "sub", "*": "mul", "/": "div", "%": "div", "=": ":=", "neg": "neg", ">=": "bge", ">":"bgt", "<=":"ble", "<":"blt", "goto":"b", "==": "beq", "!=": "bne"}
mipsInvCodeMap = {">=": "ble", ">":"blt", "<=":"bge", "<":"bgt", "==": "bne", "!=": "beq"}
mipsTemplate = {"input": "\tli $v0, 5\n\tsyscall\n", "print": "\tli $v0, 1\n\tsyscall\n", "exit":"exit:\n\tli $v0, 10\n\tsyscall\n", "space": ".data\nspace:\t.asciiz \"\\n\"", "printLn": "\taddi $v0, $zero, 4\n\tla $a0, space\n\tsyscall\n"}
registerMap = dict.fromkeys(range(15))

def init_reg_map():
    global registerMap

    ctr = 0
    for k in registerMap:
        if ctr < 10:
            registerMap[k] = "$t" + str(ctr)
        else:
            registerMap[k] = "$s" + str(ctr-10)
        ctr += 1

def genMIPSCode (icLines, coloredList, spilledList):
    mipsLines = list()
    init_reg_map()

    spilledVars = dict.fromkeys(spilledList)
    tIdx = 1
    for var in spilledVars:
        tVar = "var" + str(tIdx)
        tIdx += 1
        spilledVars[var] = tVar
    tStr = str()

    opList = ["+", "-", "*", "/", "%"]
    relop = ["<", ">", "<=", ">=", "==", "!="]
    scratchText = mipsTemplate["space"] + "\n.text \n main:\n"
    mipsLines.append(scratchText)

    count = 0
    for line in lines:
        tStr = str()
        if "=" in line:
            if "==" in line:
                idx = line.find('=')
                lhs = line[0:idx]
                rhs = line[idx+1:len(line)]
            else:
                (lhs, rhs) = line.split('=', 2)
            tokens = tokenize.generate_tokens(cStringIO.StringIO(rhs).readline)            
            tList = list()
            for t in tokens:
                if t[1] != "" and t[1] != " " and t[1] != '\n':
                    tList.append(t[1])
            lhs = lhs.replace(" ", "")
            if(tList[0] == "input"):
                tStr += mipsTemplate["input"]
                tStr += "move " + registerMap[coloredList[lhs]] + ", $v0" + "\n"

            elif len(tList) == 1:
                if tList[0].isdigit():
                    if coloredList[lhs] == None:
                        tStr += "li $s1, " + str(tList[0]) + "\n"
                    else:
                        tStr += "li " + registerMap[coloredList[lhs]] + ", " + str(tList[0]) + "\n"
                else:
                    if coloredList[lhs] == None:
                        tStr += "move $s1, " + registerMap[coloredList[tList[0]]] + "\n"
                    else:
                        tStr = "move " + registerMap[coloredList[lhs]] + ", " + registerMap[coloredList[tList[0]]] + "\n"

            elif (any (op in rhs for op in opList)):
                if "%" in rhs:
                    if tList[0].isdigit() and tList[2].isdigit():
                        tStr += "li $s6, " + str(tList[0]) + "\n"
                        tStr += "li $s7 , " + str(tList[2]) + "\n"
                        tStr += mipsCodeMap[tList[1]] + " " + "$s6 $s7\n"
                        
                    elif tList[2].isdigit():
                        tStr += "li $s6,  " + str(tList[2]) + "\n"
                        tStr += mipsCodeMap[tList[1]] + " " + registerMap[coloredList[tList[0]]] + ", $s6\n"
                    elif tList[0].isdigit():
                        tStr += "li $s7, " + str(tList[0]) + "\n"
                        tStr += mipsCodeMap[tList[1]] + " " + registerMap[coloredList[tList[2]]] + ", $s7n"
                    else:
                        tStr += mipsCodeMap[tList[1]] + " " + registerMap[coloredList[tList[2]]] + ", " + registerMap[coloredList[tList[0]]]
                    tStr += "mfhi " + registerMap[coloredList[lhs]] + "\n"
                elif tList[1] == "/":
                    if tList[0].isdigit() and tList[2].isdigit():
                        tStr += "li $s6 " + str(tList[0]) + "\n"
                        tStr += "li $s7, " + str(tList[2]) + "\n"
                        tStr += mipsCodeMap[tList[1]] + " " + "$s6, $s7\n"
 
                    elif tList[2].isdigit():
                        tStr += "li $s7, " + str(tList[2]) + "\n"
                        tStr += mipsCodeMap[tList[1]] + " " + registerMap[coloredList[tList[0]]] + ", $s7\n"
    
                    elif tList[0].isdigit():
                        tStr += "li $s7, " + str(tList[0]) + "\n"
                        tStr += mipsCodeMap[tList[1]] + " " + registerMap[coloredList[tList[2]]] + ", $s7\n"

                    else:
                        tStr += mipsCodeMap[tList[1]] + " " + registerMap[coloredList[tList[2]]] + ", " + registerMap[coloredList[tList[0]]]
                    tStr += "mflo " + registerMap[coloredList[lhs]] + "\n"
                else:
                    if tList[0].isdigit() and tList[2].isdigit():
                        tStr += "li $s6, " + str(tList[0]) + "\n"
                        tStr += "li $s7, " + str(tList[2]) + "\n"
                        tStr += mipsCodeMap[tList[1]] + " " + registerMap[coloredList[lhs]] + ", $s6, $s7 \n"

                    elif tList[2].isdigit():
                        tStr += mipsCodeMap[tList[1]] + " " + registerMap[coloredList[lhs]] + ", " + registerMap[coloredList[tList[0]]] + ", " + str(tList[2]) + "\n"
                    elif tList[0].isdigit():
                        tStr += mipsCodeMap[tList[1]] + " " + registerMap[coloredList[lhs]] + ", " + registerMap[coloredList[tList[2]]] + ", " + str(tList[0]) + "\n"
                    else:
                        tStr += mipsCodeMap[tList[1]] + " " + registerMap[coloredList[lhs]] + ", " + registerMap[coloredList[tList[0]]] + ", " + registerMap[coloredList[tList[2]]] + "\n"
                    
            elif (tList[0] == "neg"):
                if tList[1].isdigit():
                    tStr += "li $s7, " + str(tList[1]) + "\n"
                    tStr += "neg " + registerMap[coloredList[lhs]] + ", $s7\n"
                else:
                    tStr += "neg " + registerMap[coloredList[lhs]] + ", " + registerMap[coloredList[tList[1]]] + "\n"

            elif 

            elif (tList[0] == "load"):
                if not lhs in coloredList:
                    coloredList[lhs] = 10 + (count) % 10
                    count += 1
                tStr += "lw " + registerMap[coloredList[lhs]] + ", " + spilledVars[tList[1]] + "\n"

            elif (any (op in rhs for op in relop)):
                tStr = str()
                str1 = ()
                str2 = ()

                tIdx = icLines.index(line)
                nextLine = icLines[tIdx+1]
                labelLine = nextLine.split(' ')
                labelStr = labelLine[len(labelLine) - 1]

                if "goto do_while_labelID" in labelLine:
                    opcode = mipsCodeMap[tList[1]]
                else:
                    opcode = mipsCodeMap[tList[1]]

                if tList[0].isdigit():
                    str1 = "li $s6, " + str(tList[0]) + "\n"
                    op1 = "$s6"
                else:
                    op1 = registerMap[coloredList[tList[0]]]

                if tList[2].isdigit():
                    str2 = "li $s7, " + str(tList[2]) + "\n"
                    op2 = "$s7"
                else:
                    op2 = registerMap[coloredList[tList[2]]]

                if str1 and str2:
                    tStr = str1 + str2 + opcode + " " + op1 + ", " + op2 + ", " + str(labelStr)
                elif str1:
                    tStr = str1 + opcode + " " + op1 + ", " + op2 + ", " + str(labelStr)
                elif str2:
                    tStr = str2 + opcode + " " + op1 + ", " + op2 + ", " + str(labelStr)
                else:
                    tStr = opcode + " " + op1 + ", " + op2 + ", " + str(labelStr)
                
        elif "print" in line:
            tokens = tokenize.generate_tokens(cStringIO.StringIO(line).readline)
            tList = list()
            for t in tokens:
                tList.append(t[1])
            tStr += "move $a0 " + registerMap[coloredList[tList[1]]] + "\n"
            tStr += mipsTemplate["print"]
            tStr += mipsTemplate["printLn"]

        elif "goto" in line:
            if "if not" in line or "do_while_lid" in line:
                continue
            else:
                labelStr = line.split(' ')[2]
                tStr = "b " + labelStr + "\n"
                
        elif "label " in line:
            if "if not" in line:
                continue
            else:
                labelStr = line.split(' ')[1]
                tStr = labelStr + ":\n"

        elif "{" in line or "}" in line:
            continue

        elif "store" in line:
            (_, var) = line.split()
            if var.isdigit():
                tStr += "li $s0, " + str(var) + "\n"
            else:
                tStr += "move $s0, $s1\n"
            
            tStr += "sw $s0, " + spilledVars[var] + "\n"

        mipsLines.append("\t")
        mipsLines.append(tStr)

    mipsLines.append(mipsTemplate["exit"])
    if spilledVars:
        scratchText = str(".data\n")
        mipsLines.append(scratchText)
        scratchText = str()
        for var in spilledVars:
            scratchText += spilledVars[var] + ":\t .word 0\n"

    return mipsLines


if __name__ == "__main__":
    with open("test.ic") as f:
        lines = f.readlines()
    #with open("test2.ic") as f:
    #    lines = f.readlines()
    
    coloredList = {'t14': 14, 't15': 13, 't16': 12, 't17': 0, 't10': 11, 't11': 1, 't12': 10, 't13': 9, 't18': 2, 't19': 8, 'a': 7, 'c': 6, 'b': 5, 't8': 3, 't9': 4, 't6': 3, 't7': 2, 't4': 4, 't5': 1, 't2': 5, 't3': 0, 't1': 6, 's': 7, 't20': 8}

    #coloredList = {'a': 3, 'b': 2, 't2': 1, 't3': 0}
    spilledList = []
    mipsLines = genMIPSCode(lines, coloredList, spilledList)
    print "MIPS code: "
    for line in mipsLines:
        print line
        
