from liveness import *
from gencode import *

mipsCodeMap = {"+": "add", "-": "sub", "*": "mul", "/": "div", "%": "div", "=": ":=", "neg": "neg", "&&":"and", "||": "or", ">=": "bge", ">":"bgt", "<=":"ble", "<":"blt", "goto":"b"}
mipsTemplate = {"input": "li $v0, 5\nsyscall\n", "print": "li $v0, 1\nsyscall\n", "exit":"li $v0, 10\nsyscall\n", "space": ".data\nspace:\t.asciiz \"\\n\"", "printLn": "addi $v0, $zero, 4\nla $a0, space\nsyscall\n"}
registerMap = dict.fromkeys(range(15))

def init_reg_map():
    global registerMap

    ctr = 0
    for k in registerMap:
        if ctr < 10:
            registerMap[k] = "$t" + str(ctr)
        else:
            registerMap[k] = "$s" + str(ctr-10)

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
            (lhs, rhs) = line.split('=', 2)
            tokens = tokenize.generate_tokens(cStringIO.StringIO(rhs).readline)            
            tList = list()
            for t in tokens:
                if t[1] != "" and t[1] != " ":
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
                        tStr += "li " + registerMap[coloredList[lhs]] + " " + str(tList[0]) + "\n"
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

            elif (tList[0] == "load"):
                if not lhs in coloredList:
                    coloredList[lhs] = 10 + (count) % 10
                    count += 1
                tStr += "lw " + registerMap[coloredList[lhs]] + ", " + spilledVars[tList[1]] + "\n"

        elif "print" in line:
            tokens = tokenize.generate_tokens(cStringIO.StringIO(line).readline)
            tList = list()
            for t in tokens:
                tList.append(t[1])
            tStr += "move $a0 " + registerMap[coloredList[tList[1]]] + "\n"
            tStr += mipsTemplate["print"]
            tStr += mipsTemplate["printLn"]

        elif "store" in line:
            (_, var) = line.split()
            if var.isdigit():
                tStr += "li $s0, " + str(var) + "\n"
            else:
                tStr += "move $s0, $s1\n"
            
            tStr += "sw $s0, " + spilledVars[var] + "\n"

        elif any(relop) in line:
            tStr = str()
            tStr = mipsCodeMap[relop]
            idx = line.find('=')
            lhs = line[0:idx]
            rhs = line[idx+1:len(line)]
            lhs = lhs.replace(" ", "")
            rhs = rhs.replace(" ", "")
            tokens = tokenize.generate_tokens(cStringIO.StringIO(rhs).readline)
            tList = []
            for t in tokens:
                if t[1] != "" and t[1] != " ":
                    tList.append(t[1])

            tIdx = icLines.index(line)
            
            tStr += mipsCodeMap[t[1]] + " " + coloredList[t[0]] + ", " + coloredList[t[2]] + ", " + 
 
        mipsLines.append(tStr)

    mipsLines.append(mipsTemplate["exit"])
    if spilledVars:
        scratchText = str(".data\n")
        mipsLines.append(scratchText)
        scratchText = str()
        for var in spilledVars:
            scratchText += spilledVars[var] + ":\t .word 0\n"

    return mipsLines
