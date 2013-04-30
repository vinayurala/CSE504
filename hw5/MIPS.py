from liveness import *
from gencode import *
import re

arg_num = 0
#########################################
mipsCodeMap = {"+": "add", "-": "sub", "*": "mul", "/": "div", "%": "div", "=": ":=", "neg": "neg", ">=": "bge", ">":"bgt", "<=":"ble", "<":"blt", "goto":"b", "==": "beq", "!=": "bne"}
mipsInvCodeMap = {">=": "blt", ">":"ble", "<=":"bgt", "<":"bge", "==": "bne", "!=": "beq"}
mipsTemplate = {"input": "\tli $v0, 5\n\tsyscall\n", "print": "\tli $v0, 1\n\tsyscall\n", "exit":"exit:\n\tli $v0, 10\n\tsyscall\n", "space": ".data\nspace:\t.asciiz \"\\n\"", "printLn": "\taddi $v0, $zero, 4\n\tla $a0, space\n\tsyscall\n"}
registerMap = dict.fromkeys(range(15))
arr_dict = dict()
size_dict = dict()
data_section = str()
arr_alias_list = dict()

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
    global arr_dict
    global size_dict
    global data_section
    global arg_num
    
    spilledVars = dict.fromkeys(spilledList)
    tIdx = 1
    for var in spilledVars:
        tVar = "var" + str(tIdx)
        tIdx += 1
        spilledVars[var] = tVar
    tStr = str() + "\n"
    
    opList = ["+", "-", "*", "/", "%"]
    relop = ["<", ">", "<=", ">=", "==", "!="]
    scratchText = mipsTemplate["space"] + "\n.text \n main:\n"
    mipsLines.append(scratchText)
    
    count = 0
    for line in icLines:
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
    
                    
            elif tList[0] == new and tList[1] in classdict.keys():                      ################ For Classes
                count = len(classdict[tList[1]])
                count = count*4
                data_section = "\n .align 4\n"
                data_section += "class_" + lhs + ":\t.space  " + str(count) + "\n"

            elif len(tList) == 1:
                if (lhs) in arr_alias_list.values():
                    if tList[0].isdigit():
                        tStr = "li $s6, " + str(tList[0]) + "\n"
                        op1 = "$s6"
                    else:
                        op1 = registerMap[coloredList[tList[0]]]
                
                    tStr += "sw " + op1 + ", 0(" + registerMap[coloredList[lhs]] + ")\n"
                
                elif ("arr_"+tList[0]) in arr_dict.values():
                    tStr += "lw " + registerMap[coloredList[tList[0]]] + ", 0(" + registerMap[coloredList[lhs]] + ")\n"

                elif (tList[0]) in arr_alias_list.values():
                    tStr += "lw " + registerMap[coloredList[lhs]] + ", 0(" + registerMap[coloredList[tList[0]]] + ")\n"


                elif tList[0].isdigit():
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
                
                elif tList[1] == "+":
                    if ("arr_" + tList[0]) in arr_dict.values():
                        arr_size = size_dict[tList[0]]
                        tStr += "la $s6, " + str(arr_size) + "\n"
                        tStr += "lw $s6, 0($s6)\n"
                        tStr += "mul $s6, $s6, 4\n"
                        tStr += "bltz " + registerMap[coloredList[tList[2]]] + ", exit\n"
                        tStr += "bge " + registerMap[coloredList[tList[2]]] + ", $s6, exit\n"
                        tStr += "la " + registerMap[coloredList[tList[0]]] + ", " +  arr_dict[tList[0]] + "\n"
                        tStr += "add " + registerMap[coloredList[tList[0]]] + ", " + registerMap[coloredList[tList[0]]] + ", " + registerMap[coloredList[tList[2]]] + "\n"
                        arr_alias_list[tList[0]] = lhs
                        tStr += "move " + registerMap[coloredList[lhs]] + ", " + registerMap[coloredList[tList[0]]] + "\n"
                    
                    else:
                        if tList[2].isdigit():
                            op2 = str(tList[2])
                        else:
                            op2 = registerMap[coloredList[tList[2]]]
                    
                        if tList[0].isdigit():
                            tStr += "li $s6, " + str(tList[0]) + "\n"
                            op1 = "$s6"
                        else:
                            op1 = registerMap[coloredList[tList[0]]]
                        
                        tStr += "add " + registerMap[coloredList[lhs]] + ", " + op1 + ", " + op2 + "\n"

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

            elif (tList[0] == "not"):
                if tList.isdigit():
                    tStr += "li $s7, " + str(tList[1]) + "\n"
                    tStr += "xori $s7, $s7, 0x0\nsltu $s7, 1\n"
                else:
                    tStr += "xori " + registerMap[coloredList[tList[1]]] + ", " + registerMap[coloredList[tList[1]]] + ", 0x0\n"
                    tStr += "sltu " + registerMap[coloredList[lhs]] + ", " + registerMap[coloredList[tList[1]]] + ", 1\n"

            elif (tList[0] == "load"):
                if not lhs in coloredList:
                    coloredList[lhs] = 10 + (count) % 10
                    count += 1
                tStr += "lw " + registerMap[coloredList[lhs]] + ", " + spilledVars[tList[1]] + "\n"


            elif (tList[0] == "new"):
                arr_dict[lhs] = "arr_"+lhs
                size_dict[lhs] = "size_"+lhs
                data_section = size_dict[lhs] + ":\t.word  " + tList[3] + "\n .align 4\n"
                data_section += arr_dict[lhs] + ":\t.space  " + str(4 * int(tList[3])) + "\n"

            elif (any (op in rhs for op in relop)):
                tStr = str()
                str1 = ()
                str2 = ()
                
                tIdx = icLines.index(line)
                line1 = icLines[tIdx-2]
                line2 = icLines[tIdx+1]
                if "do_while_lid" in line2:
                    nextLine = line2
                
                if "end_if_lid" in line2:
                    nextLine = line2
                
                if "end_while_lid" in line1:
                    nextLine = line1
                
                if "end_for_lid" in line1:
                    nextLine = line1
                
                labelLine = nextLine.split(' ')
                labelStr = labelLine[len(labelLine) - 1]
                
                if re.match("do_while_lid", labelStr):
                    opcode = mipsCodeMap[tList[1]]
                else:
                    opcode = mipsInvCodeMap[tList[1]]

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
                    tStr = str1 + str2 + opcode + " " + op1 + ", " + op2 + ", " + str(labelStr) + "\n"
                elif str1:
                    tStr = str1 + opcode + " " + op1 + ", " + op2 + ", " + str(labelStr) + "\n"
                elif str2:
                    tStr = str2 + opcode + " " + op1 + ", " + op2 + ", " + str(labelStr) + "\n"
                else:
                    tStr = opcode + " " + op1 + ", " + op2 + ", " + str(labelStr) + "\n"

        elif "print" in line:
            tokens = tokenize.generate_tokens(cStringIO.StringIO(line).readline)
            tList = list()
            for t in tokens:
                tList.append(t[1])
            
            if tList[1] in arr_alias_list.values():
                tStr += "lw " + registerMap[coloredList[tList[1]]] + ", 0(" + registerMap[coloredList[tList[1]]] + ")\n"
            tStr += "move $a0, " + registerMap[coloredList[tList[1]]] + "\n"
            tStr += mipsTemplate["print"]
            tStr += mipsTemplate["printLn"]

        elif "goto" in line:
            if "if not" in line or "do_while_lid" in line:
                continue
            else:
                labelStr = line.split(' ')[2]
                tStr = "\n" + "b " + labelStr + "\n"

        elif "label " in line:
            if "if not" in line:
                continue
            else:
                labelStr = line.split(' ')[1]
                tStr = "\n" + labelStr + ":\n"

        elif "{" in line or "}" in line:
            continue

        elif "store" in line:
            (_, var) = line.split()
            if var.isdigit():
                tStr += "li $s0, " + str(var) + "\n"
            else:
                tStr += "move $s1, $s0\n"

            tStr += "sw $s0, " + spilledVars[var] + "\n"


        elif ":" in line and "call_" not in line:
            (lhs, rhs) = line.split('=', 2)
            tokens = tokenize.generate_tokens(cStringIO.StringIO(rhs).readline)
            tList = list()
            for t in tokens:
                if t[1] != "" and t[1] != " " and t[1] != '\n':
                    tList.append(t[1])
            lhs = lhs.replace(" ", "")

            func_name = tlist[0]
            func_name = func_name[5:]
                
            tStr = functemplate["func_call"]

            count = 0
            for arg in tlist[1:]:
                if arg != "(" and arg != "," and arg != ")" :
                    if count != 4:
                        if arg.isdigit():
                            tStr += " li $a" +count+ ", " + arg + "\n"
                        else:
                            tStr += " addi $sp, $sp, -4 \n"
                            tStr += " move $a" +count+ ", " + coloredList[arg] + " \n"
                    else:
                                
                        if arg.isdigit():
                            tStr += " li $s7," + arg + "\n"
                            tStr += " addi $sp, $sp, -4 \n"
                            tStr += " sw $s7, 0($sp) \n"
                        else:
                            tStr += " addi $sp, $sp, -4 \n"
                            tStr += " sw " + coloredList[arg] + " , 0($sp) \n"
                
            tStr += "jal " + func_name + " \n"
                
            tStr += functemplate["func_cont"]
                
                
        elif ":" in line and "label" not in line:
            line = line.replace(" ", "")
            line = line.replace(":", "")
            
            # extract args
            tStr += functemplate["new_func"]

        elif "ret" in line:
            tokens = tokenize.generate_tokens(cStringIO.StringIO(line).readline)
            tList = list()
            for t in tokens:
                if t[1] != "" and t[1] != " " and t[1] != '\n':
                    tList.append(t[1])
            arg = tList[1]
            if arg.isdigit():
                tStr += " li $v0 , " + arg + "  \n"
            else:
                tStr += " move $v0 , " + coloredList[arg] + " \n"

        elif "}" in line:
            tStr = functemplate["func_return"]

        elif 
            

        mipsLines.append(tStr)

    mipsLines.append(mipsTemplate["exit"])
    scratchText = str(".data\n")
    mipsLines.append(scratchText)
    if data_section:
        mipsLines.append(data_section)
    if spilledVars:
        scratchText = str()
        for var in spilledVars:
            scratchText += spilledVars[var] + ":\t .word 0\n"

    return mipsLines


if __name__ == "__main__":
    #with open("test.ic") as f:
    #    lines = f.readlines()
    with open("test2.ic") as f:
        lines = f.readlines()
    
    #coloredList = {'t14': 14, 't15': 13, 't16': 12, 't17': 0, 't10': 11, 't11': 1, 't12': 10, 't13': 9, 't18': 2, 't19': 8, 'a': 7, 'c': 6, 'b': 5, 't8': 3, 't9': 4, 't6': 3, 't7': 2, 't4': 4, 't5': 1, 't2': 5, 't3': 0, 't1': 6, 's': 7, 't20': 8}
    
    
    coloredList = {'a': 4, 'b': 5, 'd': 3, 't4': 2, 't5': 6, 't2': 7, 't3': 1, 't1': 0}
    #coloredList = {'a': 3, 'b': 4, 'd': 2, 't2': 5, 't3': 1, 't1': 0}
    spilledList = []
    mipsLines = genMIPSCode(lines, coloredList, spilledList)
    print "MIPS code: "
    for line in mipsLines:
        print line
##########################################################

push ={ "push" : " \t addi $sp, $sp, -4 \n \t sw str, 0($sp)" }
pop = { "pop" : " \t addi $sp, $sp, 4 \n " }
popstr = { "popstr" : "\t lw str,0($sp) \n \t add $sp,$sp,4 \n"}

func_call :

'''
    sub $sp, $sp, 56
    sw $a3, 52($sp)
    sw $a2, 48($sp)
    sw $a1, 44($sp)
    sw $a0, 40($sp)
    sw $t9, 36($sp)
    sw $t8, 32($sp)
    sw $t7, 28($sp)
    sw $t6, 24($sp)
    sw $t5, 20($sp)
    sw $t4, 16($sp)
    sw $t3, 12($sp)
    sw $t2, 8($sp)
    sw $t1, 4($sp)
    sw $t0, 0($sp)
    
    //jal str
    
    '''

new_func :

'''
    subu $sp, $sp, 40
    sw $ra, 36($sp)
    sw $fp, 32($sp)
    sw $s7, 28($sp)
    sw $s6, 24($sp)
    sw $s5, 20($sp)
    sw $s4, 16($sp)
    sw $s3, 12($sp)
    sw $s2, 8($sp)
    sw $s1, 4($sp)
    sw $s0, 0($sp)
    
    '''
functemplate = { "new_func" : "subu $sp, $sp, 40 \n sw $ra, 36($sp) \n sw $fp, 32($sp) \n sw $s7, 28($sp) \n sw $s6, 24($sp) \n sw $s5, 20($sp) \n sw $s4, 16($sp) \nsw $s3, 12($sp) \n sw $s2, 8($sp) \n sw $s1, 4($sp) \n sw $s0, 0($sp) \n  " , "func_return" : " addu $sp, $sp, 40 \n lw $ra, -4($sp) \n lw $fp, -8($sp) \n lw $s7, -12($sp) \n lw $s6, -16($sp)\n lw $s5, -20($sp) \n lw $s4, -24($sp) \n lw $s3, -28($sp) \n lw $s2, -32($sp) \n lw $s1, -36($sp) \n lw $s0, -40($sp) \n jr $ra \n" , "func_call" : " sub $sp, $sp, 56 \n sw $a3, 52($sp) \n sw $a2, 48($sp) \n sw $a1, 44($sp) \n sw $a0, 40($sp) \n sw $t9, 36($sp) \n sw $t8, 32($sp) \n sw $t7, 28($sp) \n sw $t6, 24($sp) \n sw $t5, 20($sp) \n sw $t4, 16($sp) \n sw $t3, 12($sp) \n sw $t2, 8($sp) \n sw $t1, 4($sp) \n sw $t0, 0($sp) \n" , "func_cont" : " addu $sp, $sp, 56 \n lw $a3, -4($sp) \n lw $a2, -8($sp) \n lw $a1, -12($sp) \n lw $a0, -16($sp) \n lw $t9, -20($sp) \n lw $t8, -24($sp) \n lw $t7, -28($sp) \n lw $t6, -32($sp) \n lw $t5, -36($sp) \n lw $t4, -40($sp) \n lw $t3, -44($sp) \n lw $t2, -48($sp) \n lw $t1, -52($sp) \n lw $t0, -56($sp) "}


func_return :

'''
    
    addu $sp, $sp, 40
    lw $ra, -4($sp)
    lw $fp, -8($sp)
    lw $s7, -12($sp)
    lw $s6, -16($sp)
    lw $s5, -20($sp)
    lw $s4, -24($sp)
    lw $s3, -28($sp)
    lw $s2, -32($sp)
    lw $s1, -36($sp)
    lw $s0, -40($sp)
   
   jr $ra
    
    '''

func_cont :

'''
    addu $sp, $sp, 56
    lw $a3, -4($sp)
    lw $a2, -8($sp)
    lw $a1, -12($sp)
    lw $a0, -16($sp)
    lw $t9, -20($sp)
    lw $t8, -24($sp)
    lw $t7, -28($sp)
    lw $t6, -32($sp)
    lw $t5, -36($sp)
    lw $t4, -40($sp)
    lw $t3, -44($sp)
    lw $t2, -48($sp)
    lw $t1, -52($sp)
    lw $t0, -56($sp)
    
    '''
    




