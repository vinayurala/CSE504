from parser import *
from lexer import tokens

ir_blocks = list()
temp_blk = list()
tID = 1
tVar = "t"
labelID = 1
if_lid = 1
else_lid = 1
end_if_lid = 1
while_lid = 1
end_while_lid = 1
do_while_lid = 1
end_do_while_lid = 1
for_lid = 1
end_for_lid = 1
recent_if_lid = 1
recent_while_lid = 1
recent_for_lid = 1
recent_dow_lid = 1
post_dec_str = str()
post_dec_list = list()
atomic_op = str()
post_op_list = list()
scratch_stack = list()
function_called = False

three_ops = ["+", "-", "*", "/", "%", "[", "]", ".", "="]
rel_ops = ["&&", "||", "<", ">", "<=", ">=", "==", "!="]
two_ops = ["UMINUS", "NOT"]
inc_dec = ["++", "--"]

def clear_stack():
    global scratch_stack
    global temp_blk
    global tVar
    global tID
    global post_op_list

    tStr = str()
    str1 = str2 = str()
    pre_op = False

    if not scratch_stack:
        return

    scratch_stack = scratch_stack[::-1]
    #print scratch_stack
    
    if "(" in scratch_stack and ")" in scratch_stack and "," in scratch_stack:   # Function Call
        if "=" in scratch_stack:
            str1 = scratch_stack.pop(0)               # =
            str2 = scratch_stack.pop(0)               # ret
            
        while scratch_stack:
            tStr += scratch_stack.pop() + " "
        
        if str2 and str1:
            tStr = str2 + " " + str1 + " " + tStr
            
        tStr += "\n"
        temp_blk.append(tStr)
        return


    if len(scratch_stack) == 2:                              # Ops with increment such as x++
        if "++" in scratch_stack or "--" in scratch_stack:
            str1 = scratch_stack.pop()
            str2 = scratch_stack.pop()
            if str2 == "++" or str2 == "--":
                str1, str2 = str2, str1
                pre_op = False
            else:
                pre_op = True

            if pre_op:
                tStr = str2 + " = " + str2 + " " + str1[0] + " 1\n"
                temp_blk.append(tStr)
            else:
                postStr = str2 + " = " + str2 + " " + str1[0] + " 1\n"
                post_op_list.append(postStr)
            scratch_stack.append(str2)

        else:
            str1 = scratch_stack.pop()
            str2 = scratch_stack.pop()
            tStr = tVar + str(tID) + " = " + str1 + str2 + "\n"
            temp_blk.append(tStr)
            tStr = tVar + str(tID)
            tID += 1
            scratch_stack.append(tStr)


    elif len(scratch_stack) == 3:                      # Assignment; need to take care of cascaded assignments too
        if "=" in scratch_stack:
            str1 = scratch_stack.pop()
            str2 = scratch_stack.pop(0)
            str3 = scratch_stack.pop()
            tStr = str3 + " " + str2 + " " + str1 + "\n"
        else:                                       # For Binop (eg. arr[c+d])
            str1 = scratch_stack.pop()
            str2 = scratch_stack.pop()
            str3 =scratch_stack.pop()
            tStr = tVar + str(tID) + " = " + str2 + " " + str3 + " " + str1 + "\n"
            tID += 1

        temp_blk.append(tStr)
        return

    while len(scratch_stack) > 1:
        postStr = str()
        preStr = str()
        tStr = str()
        insert_flag = False

        str1 = scratch_stack.pop()
        str2 = scratch_stack.pop()
        str3 = scratch_stack.pop()
        
        if str1 == "++" or str1 == "--":
            str2, str1 = str1, str2
            pre_op = True

        elif str3 == "++" or str3 == "--":
            str3, str2 = str2, str3
            str1, str3 = str3, str1
            insert_flag = True
            pre_op = False

        if str1 == "UMINUS" or str1 == "NOT":
            str1, str2 = str2, str1
    
        elif str3 == "UMINUS" or str3 == "NOT":
            str3, str2 = str3, str2

        if not str2 in two_ops and not str2 in inc_dec:
            if str3 in three_ops:
                if str3 is "=":
                    tStr = str2 + " " + str3 + " " + str1 +"\n"
                    temp_blk.append(tStr)     
                    if "=" in scratch_stack:
                        scratch_stack.append(str2)

                else:
                    tStr = tVar + str(tID) + " = " + str2 + " " + str3 + " " + str1 + "\n"
                    temp_blk.append(tStr)
                    tStr = tVar + str(tID)
                    tID += 1
                    scratch_stack.append(tStr)

            elif any(i in rel_ops for i in scratch_stack):                                   # For && and ||
                scratch_stack.extend([str3, str1, str2])
                idx = 1
                line_list = list()
                while scratch_stack:
                    str1 = scratch_stack.pop()
                    if str1 in rel_ops:
                        if not str1 in ["&&", "||"]:
                            tList = list(tStr)
                            str1 += " "
                            tList.insert(2, str1)
                            tStr = "".join(tList)
                            line_list.append(tStr)
                            tStr = str()
                        else:
                            str1 += " " 
                            line_list.insert(idx, str1)
                            idx += 2
                    else:
                        tStr += str1 + " "

                tStr = "".join(line_list)
                tStr = tVar + str(tID) + " = " + tStr + "\n"
                tID += 1
                temp_blk.append(tStr)
            
        else:
            #if not pre_op:
            #    str1, str3 = str3, str1
            scratch_stack.append(str3)                                             # Pre and Post ops
            if str2 in inc_dec:
                if pre_op:
                    tStr = str1 + " = " + str1 + " " + str2[0] + " 1\n"
                    temp_blk.append(tStr)
                else:
                    postStr = str1 + " = " + str1 + " " + str2[0] + " 1\n"
                    post_op_list.append(postStr)
                if insert_flag:
                    scratch_stack.insert(len(scratch_stack) - 1, str1)
                else:
                    scratch_stack.append(str1)

            else:                                                                 # UMINUS and NOT
                if str2 == "UMINUS":
                    str2 = "neg"
                else:
                    str2 = "not"
                tStr = tVar + str(tID) +  " = " + str2 + " " + str1 + "\n"
                temp_blk.append(tStr)
                tStr = tVar + str(tID)
                scratch_stack.append(tStr)
                tID += 1

    while post_op_list:
        temp_blk.append(post_op_list.pop())

    #if scratch_stack:
    #    scratch_stack.pop()
    return

def gencode(node):
    global ir_blocks
    global temp_blk
    global tID
    global tVar
    global post_dec_str
    global if_lid
    global else_lid
    global end_if_lid
    global while_lid
    global end_while_lid
    global do_while_lid
    global for_lid
    global end_for_lid
    global recent_if_lid 
    global recent_while_lid
    global recent_for_lid
    global atomic_op
    global scratch_stack
    global function_called

    blk1 = list()
    blk2 = list()
    blk3 = list()
    blk4 = list()

    if node.type is "if":
        end_if_lid = recent_if_lid
        gencode(node.children[0])
        clear_stack()
        if len(node.children) == 3:
            label_str = "if not " + tVar + str(tID - 1) + " goto label else_lid" + str(else_lid) + "\n"
        else:
            label_str = "if not " + tVar + str(tID - 1) + " goto label end_if_lid" + str(end_if_lid) + "\n"

        end_if_lid += 1
        recent_if_lid += 1
        temp_blk.append(label_str)
        gencode(node.children[1])
        if len(node.children) == 3:
            label_str = "goto label end_if_lid" + str(end_if_lid - 1) + " \n"
            temp_blk.append(label_str)
            label_str = "label else_lid" + str(else_lid) + " :\n"
            else_lid += 1
            temp_blk.append(label_str)
            gencode(node.children[2])
            
        label_str = "label end_if_lid" + str(end_if_lid-1) + " :\n"
        end_if_lid -= 1
        temp_blk.append(label_str)
        
    elif node.type is "while":             
        end_while_lid = recent_while_lid
        label_str = "label while_lid" + str(while_lid) + " :\n"
        while_lid += 1
        temp_blk.append(label_str)
        gencode(node.children[0])
        clear_stack()
        label_str = "if not " + tVar + str(tID - 1) + " goto label end_while_lid" + str(end_while_lid) + "\n"
        end_while_lid += 1
        recent_while_lid += 1
        temp_blk.append(label_str)
        gencode(node.children[1])
        label_str = "goto label while_lid" + str(while_lid - 1) + "\n"
        while_lid += 1
        temp_blk.append(label_str)
        label_str = "label end_while_lid" + str(end_while_lid - 1) + " :\n"
        end_while_lid -= 1
        temp_blk.append(label_str)

    elif node.type is "do":
        label_str = "label do_while_lid" + str(do_while_lid) + " :\n"
        do_while_lid += 1
        temp_blk.append(label_str)
        gencode(node.children[0])
        gencode(node.children[1])
        clear_stack()
        label_str = "if " + tVar + str(tID - 1) + " goto label do_while_lid" + str(do_while_lid - 1) + "\n"
        do_while_lid += 1
        temp_blk.append(label_str)

    elif node.type is "for":
        single_var_flag = 0
        end_for_lid = recent_for_lid
        gencode(node.children[0])
        clear_stack()
        label_str = "label for_lid" + str(for_lid) + " :\n"
        for_lid += 1
        temp_blk.append(label_str)
        gencode(node.children[2])
        clear_stack()
        label_str = "if not " + tVar + str(tID - 1) + " goto label end_for_lid" + str(end_for_lid) + "\n"
        temp_blk.append(label_str)
        end_for_lid += 1
        gencode(node.children[5])
        gencode(node.children[4])
        clear_stack()
        label_str = "goto label for_lid" + str(for_lid - 1) + "\n"
        temp_blk.append(label_str)
        label_str = "label end_for_lid" + str(end_for_lid - 1) + " :\n"
        end_for_lid -= 1
        temp_blk.append(label_str)
                
    elif node.type is "FunDecl":
        idNode = node.children[1]
        str1 = idNode.leaf 
        if len(node.children) != 7:
            str1 += " ():"
        else:
            str1 += " ("

        if len(node.children) == 7:
            gencode(node.children[4])
            scratch_stack = scratch_stack[::-1]
            while scratch_stack:
                str1 += scratch_stack.pop()
            str1 = str1[0:len(str1)-2]
            str1 += "):"
            temp_blk.append(str1)
            temp_blk.append("{")
            gencode(node.children[6])
        else:
            temp_blk.append(str1)
            temp_blk.append("{")
            gencode(node.children[5])

        temp_blk.append("}")

    elif node.type is "Formals":
        idNode = node.children[1]
        str1 = idNode.leaf
        gencode(node.children[2])
        str1 += ", "
        scratch_stack.append(str1)
        if len(node.children) > 3:
            gencode(node.children[4])
            
    elif node.type is "RetStmt":
        if len(node.children) > 2:
            gencode(node.children[1])
            str1 = scratch_stack.pop()
            str1 = "ret " + str1
            temp_blk.append(str1)
            del scratch_stack[:]
        else:
            temp_blk.append("ret")
            

    elif node.type is "Pgm":
        gencode(node.children[0])

    elif node.type is "DeclSeq":
        if node.children:
            gencode(node.children[0])
            gencode(node.children[1])
            
    elif node.type is "Decl":
        child = node.children[0]
        if child.type is "FunDecl":
            gencode(child)

    elif node.type is "VarDecl":
        return

    elif node.type is "VarDeclSeq":
        return

    elif node.type is "ClassDecl":
        return
        
    elif node.type is "VarList":
        return

    elif node.type is "Var":
        return

    elif node.type is "Lhs":
        gencode(node.children[0])

    elif node.type is "DimStar":
        if node.children:
            gencode(node.children[2])
    
    elif node.type is "IDType":
        idNode = node.children[0]
        scratch_stack.append(str(idNode.leaf))

    elif node.type is "ID":
        scratch_stack.append(str(node.leaf))

    elif node.type is "Type":
        scratch_stack.append(str(node.leaf))

    elif node.type is "Input":
        tStr = tVar + str(tID) + " = input()"
        tID += 1
        temp_blk.append(tStr)

    elif node.type is "PrimaryParen":
        gencode(node.children[0])

    elif node.type is "ArrayAccess":
        gencode(node.children[0])
        str1 = scratch_stack.pop()
        init_len = len(scratch_stack)
        gencode(node.children[1])
        curr_len = len(scratch_stack)
        if (curr_len - init_len) > 1:
            stack1 = scratch_stack[init_len:curr_len]
            del scratch_stack[init_len:curr_len]
            stack2 = scratch_stack[:]
            scratch_stack = stack1[:]
            clear_stack()
            scratch_stack = stack2[:] + scratch_stack
            if len(stack1) == 2:
                str2 = str(scratch_stack.pop())
            else:
                str2 = tVar + str(tID - 1)
        else:
            str2 = str(scratch_stack.pop())
        tStr = tVar + str(tID) + " = " + str2 + " * 4\n"
        tID += 1
        tStr = tStr + tVar + str(tID) + " = " + str1 + " + " + tVar + str(tID - 1) + "\n"
        temp_blk.append(tStr)
        tStr = tVar + str(tID)
        tID += 1
        #str1 = str1 + "[" + str2 + "]"
        scratch_stack.append(tStr)

    elif node.type is "PrimaryAccess":
        gencode(node.children[0])

    elif node.type is "FunctionCall":
        str1 = str()
        function_called = True
        idNode = node.children[0]
        str1 = "call_" + str(idNode.leaf)
        scratch_stack.append(str1)
        scratch_stack.append("(")
        if len(node.children) == 4:
            gencode(node.children[2])
        scratch_stack.append(")")

    elif node.type is "Args":
        gencode(node.children[0])
        if len(node.children) > 1:
            scratch_stack.append(",")
            gencode(node.children[2])
        
    elif node.type is "NewObject":
        idNode = node.children[1]
        str1 = "new " + str(idNode.leaf) + "()"
        scratch_stack.append(str1)

    elif node.type is "NewArray":
        typeNode = node.children[1]
        str1 = "new " + str(typeNode.leaf)
        init_len = len(scratch_stack)
        gencode(node.children[2])
        curr_len = len(scratch_stack)
        if (curr_len - init_len) > 1:
            clear_stack()
            str2 = tVar + str(tID - 1)
        elif len(scratch_stack) == 1:
            str2 = scratch_stack.pop()
        str1 = str1 + "[" + str2 + "]"
        init_len = len(scratch_stack)
        gencode(node.children[3])
        curr_len = len(scratch_stack)
        if (curr_len - init_len) > 1:
            clear_stack()
            str2 = tVar + str(tID - 1)
            str1 += "[" + str2 + "]"
        elif len(scratch_stack) == 1:
            str2 = scratch_stack.pop()
            str1 += "[" + str2 + "]"
        scratch_stack.append(str1)

    elif node.type is "DimExpr":
        gencode(node.children[1])

    elif node.type is "FieldAccess":
        if len(node.children) > 1:
            gencode(node.children[0])
            str1 = scratch_stack.pop()
            idNode = node.children[2]
            str1 = str1 + "." + str(idNode.leaf)
            scratch_stack.append(str1)
        else:
            gencode(node.children[0])

    elif node.type is "IntConst":
        scratch_stack.append(str(node.leaf))

    elif node.type is "AE":
        gencode(node.children[0])

    elif node.type is "Primary":
        gencode(node.children[0])

    elif node.type is "AEOpt":
        if node.children:
            gencode(node.children[0])

    elif node.type is "SEOpt":
        if node.children:
            gencode(node.children[0])

    elif node.type is "BlockExt":
        if len(node.children) == 1:
            gencode(node.children[0])
        else:
            gencode(node.children[1])

    elif node.type is "Binop":
        temp_var = str()
        child = node.children[1]
        gencode(node.children[0])
        if len(scratch_stack) == 1:
            temp_var = scratch_stack.pop()
        gencode(node.children[1])
        if temp_var:
            scratch_stack.append(temp_var)
        scratch_stack.append(str(node.leaf))        

    elif node.type is "Unop":
        scratch_stack.append(str(node.leaf))
        gencode(node.children[0])

    elif node.type is "StmtSeq":
        if node.children:
            gencode(node.children[0])
            gencode(node.children[1])
        else:
            return

    elif node.type is "Stmt":
        gencode(node.children[0])
        if len(node.children) > 1:
            gencode(node.children[1])

    elif node.type is "print":
        gencode(node.children[0])
        if len(scratch_stack) == 1:
            str1 = scratch_stack.pop()
        else:
            clear_stack()
            str1 = tVar + str(tID - 1)

        str1 = "print " + str1
        temp_blk.append(str1)

    elif node.type is "RCURLY":
        temp_blk.append("}\n")

    elif node.type is "SEMI":
        clear_stack()
        if scratch_stack:
            scratch_stack.pop()
            
    elif node.type is "Block":
        gencode(node.children[1])

    elif node.type is "LCURLY":
        if function_called:
            clear_stack()
            function_called = False

        temp_blk.append("{")

    elif node.type is "SEEq":
        eqNode = node.children[1]
        gencode(node.children[2])
        gencode(node.children[0])        
        scratch_stack.append(eqNode.leaf)

    elif node.type is "SEPost":
        gencode(node.children[0])
        postNode = node.children[1]
        scratch_stack.append(postNode.leaf)

    elif node.type is "SEPre":
        preNode = node.children[0]
        scratch_stack.append(preNode.leaf)
        gencode(node.children[1])
    
    return

def final_codegen(root):
    gencode(root)
    for line in temp_blk:
        print line
    return temp_blk

if __name__ == "__main__":
    gencode(astRoot)
    print ir_blocks
    #return ir_blocks
