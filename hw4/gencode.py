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

def unop_extractor(node):
    global tVar
    global tID

    unop_str = ()
    if node.leaf is "UMINUS":
        unop_str = "neg "
    else:
        unop_str = "not "
    if node.children[0].type in ["IntConst", "ID"]:
        unop_str += str(node.children[0].leaf)
    else:
        unop_str += str(ae_extractor(node.children[0]))
    
    unop_str = tVar + str(tID) + " = " + unop_str + "\n" 
    tID += 1

    return unop_str

def ae_extractor(node):
    global tID
    global tVar
    blk_str = str()
    
    if node.leaf == "input":
        blk_str = node.leaf
    
    elif node.type is "AE":
        if node.children[0].type is "Binop":
            blk_str = ae_extractor(node.children[0])

        if node.children[0].type is "NEW":
            blk_str = "new int" 
            str1 = ae_extractor(node.children[2])
            str2 = ae_extractor(node.children[3])
            blk_str += "[" + str(str1) + "]" + str(str2)

    elif node.type is "AEOpt":
        if node.children:
            return (ae_extractor(node.children[0]))

    elif node.type in ["IntConst", "ID"]:
        blk_str = node.leaf

    elif node.type is "DimExpr":
        blk_str = ae_extractor(node.children[1])

    elif node.type is "DimStar":
        if node.children:
            return ae_extractor(node.children[2])

    elif node.type in ["SEPost", "SEPre"]:
        blk_str = se_extractor(node)

    elif node.type is "Lhs":
        blk_str = lhs_extractor(node)

    elif node.type is "Binop":
        if node.children[1].type is "Binop":
            blk_str += ae_extractor(node.children[1])
            
        if node.children[0].type is "Binop":
            blk_str += ae_extractor(node.children[0])
        
        if node.children[1].type is "Unop":
            blk_str += unop_extractor(node.children[1])

        if node.children[0].type is "Unop":
            blk_str += unop_extractor(node.children[0])

        if node.children[1].type in ["SEPost", "SEPre"]:
            blk_str += se_extractor(node.children[1])

        if node.children[0].type in ["SEPost", "SEPre"]:
            blk_str += se_extractor(node.children[0])

        if node.children[0].type is "AE" :
            blk_str += ae_extractor(node.children[0])

        if node.children[1].type is "AE":
            blk_str += ae_extractor(node.children[1])

        if node.children[0].type is "Lhs":
            blk_str += lhs_extractor(node.children[0])

        if node.children[1].type is "Lhs":
            blk_str += lhs_extractor(node.children[1])

        if node.children[1].type is "Lhs" or node.children[0].type is "Lhs":
            if node.children[1].type is "Lhs":
                blk_str += " " + str(node.leaf) + " "
                blk_str += str(node.children[0].leaf) 
            else:
                blk_str += " " + str(node.leaf) + " "
                blk_str += str(node.children[1].leaf) 

        if node.children[1].type is "AE" and node.children[1].type is "AE":
            blk_str += tVar + str(tID - 2) + " " + str(node.leaf) + " " + tVar + str(tID - 1)

        if node.children[0].type in ["IntConst", "ID"] or node.children[1].type in ["IntConst", "ID"]:
            if node.children[0].leaf and not node.children[1].type is "Lhs":
                if node.children[1].type in ["SEPre", "SEPost"]:
                    blk_str += " " + str(node.leaf) + " "
                    blk_str += str(node.children[0].leaf) + " "
                else:
                    blk_str += str(node.children[0].leaf) + " "
                    blk_str += str(node.leaf) + " "                
            elif node.children[1].leaf and not node.children[0].type is "Lhs":
                if node.children[0].type in ["SEPre", "SEPost"]:
                    blk_str += " " + str(node.leaf) + " "
                    blk_str += str(node.children[1].leaf) + " "
                else:
                    blk_str += str(node.children[1].leaf) + " "
                    blk_str += str(node.leaf) + " "

        if node.children[1].type is "SEPre" or node.children[0].type is "SEPre":
            (str2, _) = blk_str.split('=', 2)
            blk_str += str2

        if node.children[1].type is "SEPost" or node.children[0].type is "SEPost":
            if node.type is "Binop":
                if '=' in blk_str:
                    (str2, _) = blk_str.split('=', 2)
                    (str3, str4) = blk_str.split('\n', 2)
                    str4 += " " + node.leaf + " " + str2 + "\n"
                else:
                    pass
                
            else:
                if '=' in blk_str:
                    (str2, _) = blk_str.split('=', 2)
                    (str3, str4) = blk_str.split('\n', 2)
                    str4 += str2 + "\n"
                    blk_str = str4 + str3
                else:
                    pass
                    

        elif node.children[1].type in ["Binop", "Unop"] or node.children[0].type in ["Binop", "Unop"] :
            blk_str += tVar + str(tID - 1)

        if node.children[1].type in ["Lhs", "AE", "SEPre", "SEPost"] or node.children[0].type in ["Lhs", "AE", "SEPre", "SEPost"]:
            pass

        else:
            if node.children[1].leaf:
                if node.children[1].type in ["IntConst", "ID"]:
                    blk_str += str(node.children[1].leaf)
            else:
                if node.children[0].type in ["IntConst", "ID"]:
                    blk_str += str(node.children[0].leaf)

        if "\n" in blk_str:
            if node.children[1].type is "SEPost" or node.children[0].type is "SEPost":
                if str4 and str3:
                    blk_str = tVar + str(tID) + ' = ' + str4 
                    blk_str = str3 + "\n" + blk_str
                    str4 = str3 = str()
                else:
                    blk_str = tVar + str(tID) + ' = ' + blk_str + "\n"

            else:
                idx = blk_str.rfind('\n', 0, len(blk_str))
                str1 = blk_str[idx+1:len(blk_str)]
                str2 = blk_str[0:idx+1]
                blk_str = str()
                str1 = tVar + str(tID) + " = " + str1 + "\n"
                blk_str = str2 + str1

        else:
            blk_str = tVar + str(tID) + " = " + blk_str + "\n"
        tID += 1

    else:
        blk_str = str(node.children[0].children[0])
        blk_str += str(node.children[0])
        blk_str += str(node.children[0].children[1])
        blk_str = tVar + str(tID) + " = " + blk_str
        tID += 1

    return blk_str

def lhs_extractor(node):
    global tID

    if node.type is "ID":
        return node.leaf

    if node.children[1].type is "Lhs":
        str1 = lhs_extractor(node.children[1])
    elif node.children[0].type is "Lhs":
        str1 = lhs_extractor(node.children[0])
    else:
        if node.children[1].type is "LSQR":
            ae_str = ae_extractor(node.children[2])
            arr_base = lhs_extractor(node.children[0])
            blk_str = tVar + str(tID) + " = " + str(ae_str) + " * 4\n"
            tID += 1
            blk_str += tVar + str(tID) + " = " + str(arr_base) + " + " + tVar + str(tID - 1) + "\n"
            str1 = blk_str + tVar + str(tID)
            tID += 1
        else:
            lhs_str = lhs_extractor(node.children[0])
            str1 = lhs_str + node.children[1].leaf
            blk_str = ae_extractor(node.children[2])
            str1 = str1 + blk_str + node.children[3].leaf + "\n"
            str1 += tVar + str(tID + 1) + " = " + lhs_str + "\n"
        
    return str1

def se_extractor(node):
    global post_dec_str
    global post_dec_list
 
    if node.type is "SEEq":
        blk_str = str(lhs_extractor(node.children[0])) + " "
        blk_str += str(node.children[1].leaf) + " " 
        if node.children[2].type in ["SEEq", "SEPre", "SEPost"]:
            str1 = str(se_extractor(node.children[2]))
        else:
            str1 = str(ae_extractor(node.children[2]))
        
        if "\n" in str1:
            if node.children[2] and node.children[2].type in ["SEPost", "SEPre"]:
                (var_str, _) = str1.split('=' , 2)
                blk_str += var_str

            #if node.children[2] and node.children[2].type is "SEEq":
            #    pass

            elif node.children[2].type is "Lhs":
                idx = str1.rfind('\n', 0, len(str1))
                str2 = str1[idx+1:len(str1)]
                str3 = str1[0:idx+1]
                blk_str += str2
                blk_str = str3 + blk_str + '\n'
                str1 = str()

            else:
                blk_str += str(tVar) + str(tID - 1) + "\n"

            if node.children[2].type is "SEPre":
                blk_str = str1 + blk_str
                
            else:
                if node.children[2].type is "Binop":
                    if post_dec_list:
                        blk_str = str1 + "\n" + str(post_dec_list.pop()) + "\n" + blk_str
                        str1 = str()
                    else:
                        blk_str = str1 + blk_str
                        str1 = str()
                        
                if node.children[2].type is "SEEq":
                    blk_str = str1 + "\n" + blk_str

                else:
                    blk_str += "\n" + str1
                    
            return blk_str

        else:
            blk_str += str1 + "\n"
        
        if post_dec_list:
            blk_str += str(post_dec_list.pop())
        return blk_str

    elif node.type is "SEOpt":
        if node.children:
            return se_extractor(node.children[0])

    else:
        if node.type is "SEPre":
            blk_str = lhs_extractor(node.children[1])
            if node.children[0].leaf is "++":
                blk_str = blk_str + " = " + blk_str + " + 1\n" 
            else:
                blk_str = blk_str + " = " + blk_str + " - 1\n"                
            return blk_str
        else:
            blk_str = lhs_extractor(node.children[0])
            if node.children[1].leaf == "++":
                post_dec_str = blk_str + " = " + blk_str + " + 1\n" 
                post_dec_list.append(post_dec_str)
                post_dec_str = str()
            else:
                post_dec_str = blk_str + " = " + blk_str + " - 1\n"                 
                post_dec_list.append(post_dec_str)
                post_dec_str = str()

            return blk_str


def place_seopt(blk_list, se_str):
    new_list = blk_list[::-1]
    if "}\n" in new_list:
        idx = new_list.index("}\n")
    elif "}" in new_list:
        idx = new_list.index("}")
    else:
        idx = 0
    if post_dec_list:
        new_list.insert(idx+1, post_dec_list.pop())
    else:
        new_list.insert(idx+1, se_str)
    return (new_list[::-1])
                                   

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
                
    elif node.type is "Binop":
        if node.children[0].type in ["IntConst", "ID"]:
            blk_str = str(node.children[0].leaf)
            blk_str += str(node.leaf)
            blk_str += str(node.children[1].leaf)
        else:
            blk_str = str(node.children[0].children[0])
            blk_str += str(node.children[0])
            blk_str += str(node.children[0].children[1])

        blk_str = tVar + str(tID) + " = " + blk_str
        tID += 1
        temp_blk.append(blk_str)
        temp_blk.append("\n")

    elif node.type is "Unop":
        blk_str = str(node.leaf)
        blk_str += str(ae_extractor(node.children[0]))
        temp_blk.append(blk_str)

    elif node.type is "Pgm":
        blk1 = gencode(node.children[0])
        blk2 = gencode(node.children[1])

    elif node.type is "StmtSeq":
        if node.children:
            blk1 = gencode(node.children[0])
            blk2 = gencode(node.children[1]) 

    elif node.type is "Stmt":
        blk1 = gencode(node.children[0])
        blk2 = gencode(node.children[1])
        if len(node.children) == 4:
            blk3 = gencode(node.children[2])
            blk4 = gencode(node.children[3]) 

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
            
    elif node.type is "LCURLY":
        blk_str = str(node.leaf) + "\n"
        temp_blk.append(blk_str)

    elif node.type is "SEEq":
        blk_str = se_extractor(node)
        temp_blk.append(blk_str)

    return temp_blk

def final_codegen(root):

    ir_blocks = gencode(root)
    return ir_blocks

if __name__ == "__main__":
    gencode(astRoot)
    print ir_blocks
    #return ir_blocks
