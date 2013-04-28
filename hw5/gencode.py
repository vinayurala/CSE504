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
scratch_stack = list()
                                   

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

    blk1 = list()
    blk2 = list()
    blk3 = list()
    blk4 = list()

    if node.type is "if":
        end_if_lid = recent_if_lid
        blk_str = ae_extractor(node.children[0])
        temp_blk.append(blk_str)
        if len(node.children) == 3:
            label_str = "if not " + tVar + str(tID - 1) + " goto label else_lid" + str(else_lid) + "\n"
        else:
            label_str = "if not " + tVar + str(tID - 1) + " goto label end_if_lid" + str(end_if_lid) + "\n"

        end_if_lid += 1
        recent_if_lid += 1
        temp_blk.append(label_str)
        blk2 = gencode(node.children[1])
        if len(node.children) == 3:
            label_str = "goto label end_if_lid" + str(end_if_lid - 1) + " \n"
            temp_blk.append(label_str)
            label_str = "label else_lid" + str(else_lid) + " :\n"
            else_lid += 1
            temp_blk.append(label_str)
            blk3 = gencode(node.children[2])
            
        label_str = "label end_if_lid" + str(end_if_lid-1) + " :\n"
        end_if_lid -= 1
        temp_blk.append(label_str)
        
    elif node.type is "while":             
        end_while_lid = recent_while_lid
        blk_str = ae_extractor(node.children[0])
        label_str = "if not " + tVar + str(tID - 1) + " goto label end_while_lid" + str(end_while_lid) + "\n"
        end_while_lid += 1
        recent_while_lid += 1
        temp_blk.append(label_str)
        label_str = "label while_lid" + str(while_lid) + " :\n"
        while_lid += 1
        temp_blk.append(label_str)
        temp_blk.append(blk_str)
        blk2 = gencode(node.children[1])
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
        blk1 = gencode(node.children[0])
        blk_str = ae_extractor(node.children[1])
        label_str = "if " + tVar + str(tID - 1) + " goto label do_while_lid" + str(do_while_lid - 1) + "\n"
        do_while_lid += 1
        temp_blk.append(blk_str)
        temp_blk.append(label_str)

    elif node.type is "for":
        end_for_lid = recent_for_lid
        blk_str = se_extractor(node.children[0])
        temp_blk.append(blk_str)
        blk_str = ae_extractor(node.children[2])
        label_str = "if not " + tVar + str(tID - 1) + " goto label end_for_lid" + str(end_for_lid) + "\n"
        temp_blk.append(label_str)
        end_for_lid += 1
        label_str = "label for_lid" + str(for_lid) + " :\n"
        for_lid += 1
        temp_blk.append(label_str)
        temp_blk.append(blk_str)
        blk2 = gencode(node.children[5])
        blk_str = se_extractor(node.children[4])
        if not blk_str is None:
            if post_dec_str:
                temp_blk = place_seopt(blk2, post_dec_str)
            else:
                temp_blk = place_seopt(blk2, blk_str)

        label_str = "goto label for_lid" + str(for_lid - 1) + "\n"
        temp_blk.append(label_str)
        label_str = "label end_for_lid" + str(end_for_lid - 1) + " :\n"
        end_for_lid -= 1
        temp_blk.append(label_str)
                
    elif node.type is "FunDecl":
        str1 = node.children[1] + ": "
        scratch_stack.append(str1)
        if len(node.children) == 7:
            gencode(node.children[4])
            gencode(node.children[6])
        else:
            gencode(node.children[5])

    elif node.type is "VarDecl":
        return

    elif node.type is "Type":
        return

    elif node.type is "Input":
        tStr = tVar + str(tID) + " = input()\n"
        tID += 1
        temp_blk.append(tStr)

    elif node.type is "PrimaryParen":
        gencode(node.children[0])

    elif node.type is "ArrayAccess":
        gencode(node.children[0])
        scratch_stack.append("[")
        gencode(node.children[1])
        scratch_stack.append("]")

    elif node.type is "PrimaryAccess":
        gencode(node.children[0])

    elif node.type is "FunctionCall":
        
        
    elif node.type is "FieldAccess":
        field_extractor(node)
            
    elif node.type is "IntConst":
        


    elif node.type is "AE":
        child = node.children[0]
        if child.type is "Primary":
            gencode(child)
        elif child.type is "SE":
            se_extractor(child)
        else:
            gencode(child)
    
    elif node.type is "Binop":
        str1 = ae_extractor(node.children[0])
        str2 = ae_extractor(node.children[1])
        tStr = tVar + str(tID) + " = " + str1 + " " + node.leaf + " " + str2 + "\n"
        temp_blk.append(tStr)
        tID += 1

    elif node.type is "Unop":
        str1 = ae_extractor(node.children[0])
        tStr = tVar + str(tID) + " = " + node.leaf + " " + str1 + "\n"
        temp_blk.append(tStr)
        tID += 1


    elif node.type is "StmtSeq":
        #if node.children:
        #    blk1 = gencode(node.children[0])
        #    blk2 = gencode(node.children[1]) 
        return

    elif node.type is "Stmt":
        blk1 = gencode(node.children[0])
        blk2 = gencode(node.children[1])
        if len(node.children) == 3:
            blk3 = gencode(node.children[2])
        #    blk4 = gencode(node.children[3]) 

    elif node.type is "print":
        str1 = str(ae_extractor(node.children[0]))
        if "\n" in str1:
            idx = str1.rfind('\n')
            str2 = str1[idx+1:len(str1)]
            str3 = str1[0:idx+1]
            if str2:
                blk_str = str3 + "print " + str2 + "\n"
            else:
                blk_str = str3 + "print " + tVar + str(tID - 1) + "\n"
        else:
            blk_str = "print " + str1
        temp_blk.append(blk_str)

    elif node.type is "RCURLY":
        blk_str = str(node.leaf) + "\n"
        temp_blk.append(blk_str)

    elif node.type is "SEMI":
        pass
            
    elif node.type is "Block":
        pass

    elif node.type is "LCURLY":
        blk_str = str(node.leaf) + "\n"
        temp_blk.append(blk_str)

    elif node.type is "SEEq":
        child = node.children[0]
        if child.type is "FieldAccess":
            str1 = field_extractor(child)
        else:
            str1 = array_extractor(child)

        str2 = ae_extractor(node.children[1])
        tStr = tvar + str(tID) + 
        
    return temp_blk

def final_codegen(root):

    ir_blocks = gencode(root)
    return ir_blocks

if __name__ == "__main__":
    gencode(astRoot)
    print ir_blocks
    #return ir_blocks
