from parser import *
from lexer import tokens

ir_blocks = list()
temp_blk = list()
tID = 1
tVar = "t"
labelID = 1

def unop_extractor(node):
    global tVar
    global tID

    unop_str = ()
    unop_str = node.leaf + " "
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

    elif node.type is "AEOpt":
        if node.children:
            return (ae_extractor(node.children[0]))

    elif node.type in ["IntConst", "ID"]:
        blk_str = node.leaf

    elif node.type is "Binop":
        if node.children[1].type is "Binop":
            blk_str += ae_extractor(node.children[1])
        
        elif node.children[1].type is "Unop":
            blk_str += unop_extractor(node.children[1])

        blk_str += str(node.children[0].leaf) + " "
        blk_str += str(node.leaf) + " "
        if node.children[1].type in ["Binop", "Unop"]:
            blk_str += tVar + str(tID - 1)
        else:
            blk_str += str(node.children[1].leaf)
        if "\n" in blk_str:
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
    if node.type is "ID":
        return node.leaf
    else:
        lhs_str = lhs_extractor(node.children[0])
        str1 = lhs_str + node.children[1].leaf
        blk_str = ae_extractor(node.children[2])
        str1 = str1 + blk_str + node.children[3].leaf + "\n"
        str1 += tVar + str(tID + 1) + " = " + lhs_str + "\n"
        
    return str1

def se_extractor(node):
    if node.type is "SEEq":
       
        blk_str = str(lhs_extractor(node.children[0])) + " "
        blk_str += str(node.children[1].leaf) + " " 
        str1 = str(ae_extractor(node.children[2]))
        
        if "\n" in str1:
            blk_str += str(tVar) + str(tID - 1) + "\n"
            blk_str = str1 + blk_str
        else:
            blk_str += str1
        
        return blk_str

    elif node.type is "SEOpt":
        if node.children:
            return se_extractor(node.children[0])

    else:
        if node.type is "SEPre":
            blk_str = node.children[0].leaf
            blk_str += lhs_extractor(node.children[1])
            return blk_str
        else:
            blk_str = node.children[1].leaf
            blk_str += lhs_extractor(node.children[0])
            return blk_str

def place_seopt(blk_list, se_str):
    new_list = blk_list[::-1]
    idx = new_list.index("}")
    new_list.insert(idx+1, se_str)
    return (new_list[::-1])
                                   

def gencode(node):
    global ir_blocks
    global temp_blk
    global tID
    global tVar
    global labelID

    blk1 = list()
    blk2 = list()
    blk3 = list()
    blk4 = list()

    if node.type is "if":
        blk_str = ae_extractor(node.children[0])
        temp_blk.append(blk_str)
        label_str = "if not " + tVar + str(tID - 1) + " goto label " + "\n"
        temp_blk.append(label_str)
        blk2 = gencode(node.children[1])
        label_str = "label " + str(labelID) + ":\n"
        temp_blk.append(label_str)
        if len(node.children) == 3:
            blk3 = gencode(node.children[2])
            label_str = "label" + str(labelID) + ":\n"
            temp_blk.append(label_str)
            labelID += 1
        
    elif node.type is "while":             
        blk_str = ae_extractor(node.children[0])
        label_str = "if not " + tVar + str(tID - 1) + " goto label " + "\n"
        temp_blk.append(blk_str)
        temp_blk.append(label_str)
        blk2 = gencode(node.children[1])
        labelID += 1
        label_str = "goto label " 
        temp_blk.append(label_str)

    elif node.type is "do":
        label_str = "label " + str(labelID) + ":\n"
        temp_blk.append(label_str)
        blk1 = gencode(node.children[0])
        blk_str = ae_extractor(node.children[1])
        label_str = "if " + tVar + str(tID - 1) + " goto label " + str(labelID) + "\n"
        labelID += 1
        temp_blk.append(blk_str)
        temp_blk.append(label_str)

    elif node.type is "for":
        blk_str = se_extractor(node.children[0])
        temp_blk.append(blk_str)
        blk_str = ae_extractor(node.children[2])
        label_str = "if not " + tVar + str(tID - 1) + " goto label " + "\n"
        temp_blk.append(label_str)
        labelID += 1
        blk2 = gencode(node.children[5])
        blk_str = se_extractor(node.children[4])
        if not blk_str is None:
            temp_blk = place_seopt(blk2, blk_str)
        #temp_blk.append(blk_str)
        label_str = "goto label "
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

    elif node.type is "RCURLY":
        temp_blk.append(node.leaf)

    elif node.type is "SEMI":
        pass
            
    elif node.type is "LCURLY":
        temp_blk.append(node.leaf)

    elif node.type is "SEEq":
        blk_str = se_extractor(node)
        temp_blk.append(blk_str)

    return temp_blk

def get_idx(blocks, brace):
    br_list = list()
    for idx in range(len(blocks)):
        if blocks[idx] == brace:
            br_list.append(idx)

    return br_list

def second_pass(blocks):
    ir_blocks = list()
    open_brace_list = get_idx(blocks, "{")
    #close_brace_list = get_idx(blocks, "}")

    print close_brace_list

    idx = 0
    new_blk = list()
    while idx in range(len(blocks)):
        if "if" in blocks[idx]:
            new_blk.append(blocks[idx : min(close_brace_list)])
            idx = min(close_brace_list) + 1
            close_brace_list.pop(0)
        else:
            new_blk.append(blocks[idx])
            idx += 1

        ir_blocks.append(new_blk[:])
        del new_blk[:]

    return ir_blocks

def final_codegen(root):
    #block_list = gencode(root)
    #ir_blocks = second_pass(block_list)
    ir_blocks = gencode(root)
    return ir_blocks

if __name__ == "__main__":
    gencode(astRoot)
    print ir_blocks
    #return ir_blocks
