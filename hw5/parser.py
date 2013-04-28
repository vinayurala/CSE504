# Yacc example
#import pydot

import ply.yacc as yacc

import sys

# Get the token map from the lexer.  This is required.
from lexer import tokens

precedence = (('left', 'OR'),
              ('left', 'AND'),
              ('nonassoc', 'EQUALS', 'NOTEQ'),
              ('nonassoc', 'LTEQ','LT', 'GT','GTEQ'),
              ('left', 'PLUS', 'MINUS'),
              ('left', 'TIMES', 'DIVIDE', 'MOD'),
              ('right', 'NOT'),
              ('right', 'UMINUS'),
              )


class Node:
    def __init__(self,type,children=None,leaf=None,check = None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = [ ]
        self.leaf = leaf

"""
    def graph(node):
    edges = descend(node)
    g=pydot.graph_from_edges(edges)
    f = "graph.png"
    g.write_png(f, prog='dot')
    
    
    def descend(node):
    edges = []
    
    if node.__class__ != Node:
    return []
    
    for i in node.children:
    edges.append(((node.type,node.leaf),(i.type,i.leaf)))
    edges = edges + descend(i)
    return edges
    """
###########################################################################
def p_pgm_decl(p):
    'Pgm : DeclSeq'             # For *
    p[0] = Node("Pgm", children = [p[1]])

def p_declseq(p):
    'DeclSeq : Decl DeclSeq'
    p[0] = Node("DeclSeq", children = [p[1], p[2]])

def p_declseq_null(p):
    'DeclSeq : '
    p[0] = Node("DeclSeq")

def p_decl(p):
    '''Decl : VarDecl
          | FunDecl
          | ClassDecl'''
    p[0] = Node("Decl", children = [p[1]])

def p_vardecl(p):
    'VarDecl : Type VarList SCOLON'
    p[3] = Node("SEMI", leaf = p[3])
    p[0] = Node("VarDecl", children = [p[1], p[2], p[3]])

def p_fundecl(p):                                                   #Used for ?
    '''FunDecl : Type ID DimStar LPAREN Formals RPAREN Stmt                     
               | Type ID DimStar LPAREN RPAREN Stmt'''
    p[2] = Node("ID", leaf = p[2])
    p[4] = Node("LPAREN", leaf = p[4])
    if len(p) == 8:
        p[6] = Node("RPAREN", leaf = p[6])
        p[0] = Node("FunDecl", children = [p[1], p[2], p[3], p[4], p[5], p[6], p[7]])
    else:
        p[5] = Node("RPAREN", leaf = p[5])
        p[0] = Node("FunDecl", children = [p[1], p[2], p[3], p[4], p[5], p[6]])           # Need to differentiate?


def p_classdecl(p):
    'ClassDecl : CLASS ID LCURLY VarDeclSeq RCURLY '
    p[2] = Node("ID", leaf = p[2])
    p[3] = Node("LCURLY", leaf = p[3])
    p[5] = Node("RCURLY", leaf = p[5])
    p[0] = Node("ClassDecl", children = [p[2], p[3], p[4], p[5]])


def p_vardeclseq(p):                                                # for Decl in classes
    'VarDeclSeq : VarDecl VarDeclSeq'
    p[0] = Node("VarDeclSeq", children = [p[1], p[2]])

def p_vardeclseq_null(p):
    'VarDeclSeq : '
    p[0] = Node("VarDeclSeq")

def p_type(p):
    '''Type : INT
            | BOOL
            | VOID'''
    if len(p) == 2:
        p[0] = Node("Type", leaf = p[1])

def p_type_id(p):
    'Type : ID'
    p[1] = Node("ID", leaf = p[1])
    p[0] = Node("Type", children = [p[1]])

#def p_err(p):
#'Err :'


def p_varlist(p):
    '''VarList : Var COMMA VarList
               | Var '''
    if len(p) == 2:
        p[0] = Node("VarList", children = [p[1]])
    else:
        p[2] = Node("COMMA", leaf = p[2])
        p[0] = Node("VarList", children = [p[1], p[2], p[3]])

def p_var(p):
    ''' Var : ID DimStar'''
    p[1] = Node("ID", leaf = p[1])
    p[0] = Node("Var", children = [p[1], p[2]])

def p_dimstar(p):
    '''DimStar : LSQR RSQR DimStar
        DimStar : '''
    if len(p) == 1:
        p[0] = Node("DimStar", children = [])
    elif len(p) == 4:
        p[1] = Node("LSQR", leaf = p[1])
        p[2] = Node("RSQR", leaf = p[2])
        p[0] = Node("DimStar", children = [p[1], p[2], p[3]])


def p_formals(p):
    '''Formals : Type ID DimStar COMMA Formals
               | Type ID DimStar'''
    p[2] = Node("ID", leaf = p[2])
    if len(p) == 4:
        p[0] = Node("Formals", children = [p[1], p[2], p[3]])
    else:
        p[4] = Node("COMMA", leaf = p[4])
        p[0] = Node("Formals", children = [p[1], p[2], p[3], p[4], p[5]])

def p_stmt(p):
    '''Stmt : SE SCOLON
        Stmt : PRINT LPAREN AE RPAREN SCOLON
        Stmt : IF AE THEN Stmt ELSE Stmt
        Stmt : IF AE THEN Stmt
        Stmt : WHILE AE DO Stmt
        Stmt : FOR LPAREN SEOpt SCOLON AEOpt SCOLON SEOpt RPAREN Stmt
        Stmt : DO Stmt WHILE AE SCOLON'''
    if len(p) == 3:
        p[2] = Node("SEMI", leaf = p[2])
        p[0] = Node("Stmt", children = [p[1], p[2]])
    elif len(p) == 5:
        if ("if" in p):
            p[0] = Node("if", children = [p[2], p[4]], leaf = p[1])
        else:
            p[0] = Node("while", children = [p[2], p[4]], leaf = p[1])
    elif len(p) == 6:
        p[5] = Node("SEMI", leaf = p[5])
        if p[1] == "do":
            p[0] = Node("do", children = [p[2], p[4], p[5]],leaf =  p[1])
        else:
            p[0] = Node("print", children = [p[3],p[5]], leaf = p[1])
    elif len(p) == 7:
        p[0] = Node("if", children = [p[2], p[4], p[6]], leaf = p[1])
    elif len(p) == 10:
        p[4] = Node("SEMI", leaf = p[4])
        p[6] = Node("SEMI", leaf = p[6])
        p[0] = Node("for", children = [p[3], p[4], p[5], p[6], p[7], p[9]], leaf = p[1])

def p_seopt(p):
    '''SEOpt : SE
        SEOpt : '''
    if len(p) == 1:
        p[0] = Node("SEOpt")
    else:
        p[0] = Node("SEOpt", children = [p[1]])


def p_aeopt(p):
    '''AEOpt : AE
        AEOpt : '''
    if len(p) == 1:
        p[0] = Node("AEOpt")
    else:
        p[0] = Node("AEOpt", children = [p[1]])



def p_stmtseq(p):
    'StmtSeq : Stmt StmtSeq'
    p[0] = Node("StmtSeq",children = [p[1],p[2]])

def p_stmtseq_null(p):
    'StmtSeq : '
    p[0] = Node("StmtSeq")

def p_stmt_block(p):
    'Stmt : Block'
    p[0] = Node("Stmt", children = [p[1]])

def p_block(p):
    'Block : LCURLY BlockExt RCURLY'
    p[1] = Node("LCURLY", leaf = p[1])
    p[3] = Node("RCURLY", leaf = p[3])
    p[0] = Node("Block", children = [p[1], p[2], p[3]])

def p_blockext(p):
    '''BlockExt : VarDecl BlockExt
                | StmtSeq'''
    if len(p) == 2:
        p[0] = Node("BlockExt", children = [p[1]])
    else:
        p[0] = Node("BlockExt", children = [p[1], p[2]])
    

def p_stmt_return(p):
    '''Stmt : RETURN AE SCOLON
            | RETURN SCOLON'''
    if len(p) == 3:
        p[2] = Node("SEMI", leaf = p[2])
        p[1] = Node("RETURN", leaf = p[1])
        p[0] = Node("Stmt", children = [p[1], p[2]])
    else:
        p[3] = Node("SEMI", leaf = p[3])
        p[1] = Node("RETURN", leaf = p[1])
        p[0] = Node("Stmt", children = [p[1], p[2], p[3]])


def p_se(p):
    'SE : Lhs EQ AE'
    p[2] = Node("EQ", leaf  = p[2])
    p[0] = Node("SEEq", children = [p[1], p[2], p[3]])

def p_se_post(p):
    '''SE : Lhs INC
        | Lhs DEC'''
    p[2] = Node("POST", leaf = p[2])
    p[0] = Node("SEPost", children = [p[1], p[2]])

def p_se_pre(p):
    '''SE : INC Lhs
        | DEC Lhs '''
    p[1] = Node("Pre", leaf = p[1])
    p[0] = Node("SEPre", children = [p[1], p[2]])

def p_lhs(p):
    '''Lhs : FieldAccess
           | ArrayAccess'''
    p[0] = Node("Lhs", children = [p[1]])

def p_ae(p):
    '''AE : Primary
          | SE
          | NewArray'''
    p[0] = Node("AE", children = [p[1]])


def p_ae_binop(p):
    '''AE : AE PLUS AE
        | AE MINUS AE
        | AE TIMES AE
        | AE DIVIDE AE
        | AE MOD AE
        | AE AND AE
        | AE OR AE
        | AE EQUALS AE
        | AE NOTEQ AE
        | AE LT AE
        | AE GT AE
        | AE GTEQ AE
        | AE LTEQ AE '''
    p[0] = Node("Binop", children = [p[1], p[3]], leaf = p[2])

def p_ae_uminus(p):
    'AE : MINUS AE %prec UMINUS'
    p[0] = Node("Unop", children = [p[2]],leaf = "UMINUS")

def p_ae_not(p):
    'AE : NOT AE'
    p[0] = Node("Unop", children = [p[2]], leaf = "NOT")

def p_primary_ip(p):
    'Primary : INPUT LPAREN RPAREN'
    p[0] = Node("Input", leaf = p[1])

def p_primary_aeparan(p):                           ###########need Parentheses?
    'Primary : LPAREN AE RPAREN'
    p[0] = Node("Primary", children = [p[2]])

def p_primary_misc(p):
    '''Primary : FieldAccess
                | ArrayAccess
                | FunctionCall
                | NewObject '''
    p[0] = Node("Primary", children = [p[1]])

def p_primary_const(p):
    '''Primary : TRUE
        | FALSE
        | NUMBER '''
    if ("true" in p):
        p[0] = Node("bool", leaf = p[1])    
    elif ("false" in p):
        p[0] = Node("bool", leaf = p[1])
    else:
        p[0] = Node("IntConst", leaf = p[1])

def p_arrayaccess(p):                           ##### Need Square Brackets?
    'ArrayAccess : Primary LSQR AE RSQR'
    p[0] = Node("ArrayAccess", children = [p[1], p[3]])

def p_FieldAccess(p):
    '''FieldAccess : Primary DOT ID
                    | ID '''
    if len(p) == 2:
        p[1] = Node("ID", leaf = p[1])
        p[0] = Node("FieldAccess", children = [p[1]])
    else:
        p[3] = Node("ID", leaf = p[3])
        p[2] = Node("DOT", leaf = p[2])
        p[0] = Node("FieldAccess", children = [p[1], p[2], p[3]])

def p_functioncall(p):
    '''FunctionCall : ID LPAREN Args RPAREN
                    | ID LPAREN RPAREN'''
    p[1] = Node("ID", leaf = p[1])
    p[2] = Node("LPAREN", leaf = p[2])
    if len(p) == 4:
        p[3] = Node("RPAREN", leaf = p[3])
        p[0] = Node("FunctionCall", children = [p[1], p[2], p[3]])
    else:
        p[4] = Node("RPAREN", leaf = p[4])
        p[0] = Node("FunctionCall", children = [p[1], p[2], p[3], p[4]])

def p_args(p):
    '''Args : AE COMMA Args
            | AE'''
    if len(p) == 2:
        p[0] = Node("Args", children = [p[1]])
    else:
        p[2] = Node("COMMA", leaf = p[2])
        p[0] = Node("Args", children = [p[1], p[2], p[3]])

def p_newobject(p):
    'NewObject : NEW ID LPAREN RPAREN'              ##### Do I need it?
    p[1] = Node("NEW", leaf = p[1])
    p[2] = Node("ID", leaf = p[2])
    p[3] = Node("LPAREN", leaf = p[3])
    p[4] = Node("RPAREN", leaf = p[4])
    p[0] = Node("NewObject", children = [p[1], p[2], p[3], p[4]])

def p_newarray(p):
    'NewArray : NEW Type DimExpr DimStar'                    # For DimSeq  #???????????????????????
    p[1] = Node("NEW", leaf = p[1])
    p[0] = Node("NewArray", children = [p[1], p[2], p[3], p[4]])



def p_dimexpr(p):
    'DimExpr : LSQR AE RSQR'
    p[1] = Node("LSQR", leaf = p[1])
    p[3] = Node("RSQR", leaf = p[3])
    p[0] = node("DimExpr", children = [p[1], p[2], p[3]])


def p_error(p):
    if p==None:
        print "Syntax error found at 'End Of File' Probably because of missing right curly brace"
        sys.exit()
    else :
        print "Syntax error in line number %d just before token '%s' of value '%s' " % (p.lineno,p.type,p.value)
        sys.exit()

parser = yacc.yacc()


decl = list()
defined = list()
parent = None
done = 0
vars = {}
found = [0]
inclass = 0
classdict = {}
currentclass = None
classobj = {}

##############################################################################################

def wellformed(node,decl,defined):
    global inclass
    global currentclass
    global classobj
    #print inclass
    #print currentclass
    #print node
    #print node.type
    iterable_list = node.children[:]
    
    
    if node.type == "FunctionCall":
        wellformed(node.children[2],decl,defined)
        return
    
    if node.type == "NewObject":
        return

    
    
    if node.type == "FunDecl":
        temp_decl = decl[:]
        temp_defined = defined[:]
        iterable_list = node.children[4:]
        for child in iterable_list:
            wellformed(child,temp_decl,temp_defined)
        return

    if node.type == "Formals":
        id = node.children[1]
        decl.append(id)
        defined.append(id)
        if len(node.children) > 3 :
            wellformed(node.children[4],decl,defined)
        return

    if node.type == "ClassDecl":
        iterable_list = node.children[2:]
        temp_decl = decl[:]
        temp_defined = defined[:]
        inclass = 1
        currentclass = node.children[0].leaf
        for child in iterable_list:
            print "in"
            wellformed(child,temp_decl,temp_defined)
        inclass = 0
        currentclass = None
        return

    
    
    
    
    if(node.type == "if"):
        if(len(node.children) == 3):
            temp_decl = decl[:]
            temp_defined = defined[:]
            #temp_parent = node.type
            wellformed(node.children[0],temp_decl,temp_defined)
            wellformed(node.children[1],temp_decl,temp_defined)
            #print temp_decl
            #print temp_defined
            set_def = set(temp_defined).difference(set(defined))
            #print set_def
            #print temp_decl
            set_dec = set(temp_decl).difference(set(decl))
            #print set_dec
            set_1 = set_def.difference(set_dec)
            #print set_1
        
            wellformed(node.children[2],temp_decl,temp_defined)
            #print temp_decl
            #print temp_defined
            set_def2 = set(temp_defined).difference(set(defined))
            set_dec2 = set(temp_decl).difference(set(decl))
            set_2 = set_def2.difference(set_dec2)
        # print set_2
        
        else:
            temp_decl = decl[:]
            temp_defined = defined[:]
            #print decl[:]
            #temp_parent = node.type
            for child in iterable_list:
                #print child
                wellformed(child,temp_decl,temp_defined)
            #print decl[:]
        return
    
    
    elif(node.type == "while"):
        temp_decl = decl[:]
        temp_defined = defined[:]
        #print decl[:]
        #temp_parent = node.type
        for child in iterable_list:
            #print child
            wellformed(child,temp_decl,temp_defined)
        #print decl[:]
        return
    
    elif(node.type == "do"):
        #print "here"
        temp_decl = decl[:]
        #temp_parent = node.type
        for child in iterable_list:
            #print defined[:]
            wellformed(child,temp_decl,defined)
        # print defined[:]
        #print decl[:]
            #print defined[:]
        return

    elif(node.type == "for"):
        #temp_parent = node.type
        if(node.children[0].type == "SEOpt"):
            wellformed(node.children[0],decl,defined)
            iterable_list = node.children[1:]
        temp_decl = decl[:]
        temp_defined = defined[:]
        for child in iterable_list:
            #print child
            wellformed(child,temp_decl,temp_defined)
        #print decl[:]
        return


    elif(node.type == "Stmt"):
        #temp_parent = node.type
        if(node.children[0].type == "Block"):
            temp_decl = decl[:]
          
            #print decl[:]
            for child in iterable_list:
                wellformed(child,temp_decl,defined)

            return



    elif(node.type == "VarDecl"):
        Type = node.children[0]
        if Type.children[0].type == "ID":
            classid = Type.children[0].leaf
            if classid not in classdict.keys():
                print "Wellformed ERROR: CLASS NAME \"" + id + "\" NOT DECLARED before use"
                sys.exit(-1)
            var = node.children[1]
            while var.type != "ID":
                var = var.children[0]
            varid = var.leaf
            if classid not in classobj.keys():
                classobj[classid] = [varid]
            else:
                classobj[classid].append(varid)
                
                


    elif(node.type == "Var"):
        id = node.children[0].leaf
        if inclass == 1:
            if  currentclass not in classdict.keys():
                classdict[currentclass] = [id]
            else:
                classdict[currentclass].append(id)
        else:
            decl.append(id)
        iterable_list = node.children[1:]

    
    elif node.type == "ID":
        id = node.leaf
        #print id
        if not id in decl:
            print "Wellformed ERROR: Variable \"" + id + "\" NOT DECLARED before use"
            sys.exit(-1)
            return []
        elif not id in defined:
            print "Wellformed ERROR: Variable \"" + id + "\" NOT DEFINED before use"
            sys.exit(-1)
            return []
    
    elif node.type == "SEEq":
        #temp_parent = node.type
        iterable_list = node.children[1:]
        for child in iterable_list:
            #print child.type
            wellformed(child,decl,defined)

        lhs = node.children[0]
        if lhs.children[0].type == "FieldAccess":
            field = lhs.children[0]
            if field.children[0].type == "ID":
                id = field.children[0].leaf
                if not id in decl:
                    print "Wellformed ERROR: Variable \"" + id + "\" NOT DECLARED before use"
                    sys.exit(-1)
                    return []
                elif id in defined:
                    pass
                else:
                    defined.append(id)

        
        return
        #print "-----" + id
        #print defined[:]
        
    
    #temp_parent = node.type
    for child in iterable_list:
        #print child.type
        wellformed(child,decl,defined)
    
    return
################################################################################

def ismain(node):
    iterable_list = node.children[:]
    if node.type == "FunDecl":
        if node.children[1].leaf == "main" and node.children[0].leaf == "void" and node.children[4].type == "RPAREN":
            global done
            done = 1
        elif node.children[1].leaf != "main" and node.children[0].leaf == "void":
            print "function ERROR: Function found which is not MAIN and return type is VOID"
            sys.exit(-1)

    for child in iterable_list:
        #print child.type
        ismain(child)
    return
################################################################################

def isreturn(node):
    iterable_list = node.children[:]
    if node.type == "FunDecl":
        found = [0]
        checkreturn(node,found)
        if found[0] == 0:
            print "function ERROR: Return Not Found in every control flow path"
            sys.exit(-1)
        return
    for child in iterable_list:
        #print child.type
        isreturn(child)
    return
################################################################################

def checkreturn(node,found):
    iterable_list = node.children[:]
    
    if(node.type == "if"):
        if(len(node.children) == 3):
            temp_found = found[:]
            checkreturn(node.children[1],temp_found)
            if temp_found[0] == 0:
                return
            temp_found = found[:]
            checkreturn(node.children[2],temp_found)
            if temp_found[0] == 0:
                return
            found[0] = 1
            return
        else:
            return

    elif(node.type == "while" or node.type == "for"):
        return
    
    elif(node.type == "do"):
        #print "here"
        for child in iterable_list:
            checkreturn(child,found)
        # print defined[:]
        #print decl[:]
        #print defined[:]
        return
                
    elif(node.type == "Stmt" and node.children[0].leaf == "return"):
        #print "Here"
        found[0] = 1
        return



    
    elif(node.type == "Block"):
        if(node.children[0].type == "LCURLY"):
            for child in iterable_list:
                checkreturn(child,found)
            
        return

    for child in iterable_list:
        checkreturn(child,found)
    
    return

################################################################################


##############################################################################################

def declareonce(node,decl,parent):
    #print node
    #print node.type
    iterable_list = node.children[:]
    
    
    if node.type == "FunctionCall":
        declareonce(node.children[2],decl,parent)
        return
    
    if node.type == "NewObject":
        return
    
    
    
    if node.type == "FunDecl":
        temp_decl = []
        iterable_list = node.children[3:]
        parent = "FunDecl"
        for child in iterable_list:
            declareonce(child,temp_decl,parent)
        return
    
    if node.type == "Formals":
        id = node.children[1].leaf
        if id in decl:
            print "Declare-Once ERROR: Variable \"" + id + "\" DECLARED Multiple Times in a scope"
            sys.exit(-1)
        decl.append(id)
        if len(node.children) > 3 :
            declareonce(node.children[4],decl,parent)
        return
    
    if node.type == "ClassDecl":
        temp_decl = []
        for child in iterable_list:
            declareonce(child,temp_decl,parent)
        return
    
  
    
    elif(node.type == "Stmt"):
        if parent == "FunDecl" and node.children[0].type == "Block":
            for child in iterable_list:
                declareonce(child,decl,None)
            
            return
        
        if(node.children[0].type == "Block"):
            temp_decl = []
            for child in iterable_list:
                declareonce(child,temp_decl,parent)
            
            return
    
    
    
    elif(node.type == "Var"):
        id = node.children[0].leaf
        if id in decl:
            print "Declare-Once ERROR: Variable \"" + id + "\" DECLARED Multiple Times in a scope"
            sys.exit(-1)
        decl.append(id)
        #print decl[:]
        iterable_list = node.children[1:]

    
    #temp_parent = node.type
    for child in iterable_list:
        #print child.type
        declareonce(child,decl,parent)
    
    return



##############################################################################################

def welltyped(node,vars):

    if node.type == "IntConst":
        node.check = "int"
        return

    elif node.type == "bool":
        node.check = "bool"
        return

    elif node.type == "VarDecl":
        if node.children[0].leaf == "int" or node.children[0].leaf == "bool":
            type = node.children[0].leaf
            varnode = node.children[1]
            while (len(varnode.children) != 1):
                vars[varnode.children[0].leaf] = type
                varnode = varnode.children[2]
            vars[varnode.children[0].leaf] = type
            node.check = type
        return

    elif node.type == "Unop":
        welltyped(node.children[0],vars)
        if node.leaf == "UMINUS":
            if node.children[0].check == "int":
                node.check = "int"
            else:
                node.check = "error"
        else:
            if node.children[0].check == "bool":
                node.check = "bool"
            else:
                node.check = "error"
        return

    elif node.type == "Binop":
        welltyped(node.children[0],vars)
        welltyped(node.children[1],vars)
        if node.leaf in ["+", "-", "*", "/", "%"]:
            if node.children[0].check == "int" and node.children[1].check == "int":
                node.check = "int"
            else:
                node.check = "error"

        elif node.leaf in ["==", "!="]:
            if node.children[0].check == "int" and node.children[1].check == "int":
                node.check = "bool"
            elif node.children[0].check == "bool" and node.children[1].check == "bool":
                node.check = "bool"
            else:
                node.check = "error"

        elif node.leaf in ["<", ">", "<=", ">="]:
            if node.children[0].check == "int" and node.children[1].check == "int":
                node.check = "bool"
            else:
                node.check = "error"

        elif node.leaf in ["||", "&&"]:
            if node.children[0].check == "bool" and node.children[1].check == "bool":
                node.check = "bool"
            else:
                node.check = "error"
        return


    elif node.type == "SEEq":
        welltyped(node.children[0],vars)
        welltyped(node.children[2],vars)
        if node.children[0].check == node.children[2].check:
            node.check = node.children[2].check
        else:
            node.check = "error"
        return


    elif node.type == "SEPost":
        welltyped(node.children[0],vars)
        if node.children[0].check == "int":
            node.check = "int"
        else:
            node.check = "error"
        return

    elif node.type == "SEPre":
        welltyped(node.children[1],vars)
        if node.children[1].check == "int":
            node.check = "int"
        else:
            node.check = "error"
        return

    elif node.type == "print":
        welltyped(node.children[0],vars)
        if node.children[0].check != "int":
            node.check = "error"
        return

    elif node.type == "if":
        iterable_list = node.children[:]
        for child in iterable_list:
            welltyped(child,vars)
        if node.children[0].check != "bool":
            node.check = "error"
        for child in iterable_list:
            if child.check == "error":
                node.check = "error"
        return

    elif node.type == "while":
        iterable_list = node.children[:]
        for child in iterable_list:
            welltyped(child,vars)
        if node.children[0].check != "bool":
            node.check = "error"
        for child in iterable_list:
            if child.check == "error":
                node.check = "error"
        return

    elif node.type == "do":
        iterable_list = node.children[:]
        for child in iterable_list:
            welltyped(child,vars)
        if node.children[1].check != "bool":
            node.check = "error"
        for child in iterable_list:
            if child.check == "error":
                node.check = "error"
        return



################################################################################

if __name__ == "__main__":
    s = '''
        int a,b,i,c,d;
        bool y,z;
        
        
        class a 
        {
            int a,x;
        }
        void main()
        {
            //int a[];
            //a obj;
            
            bool fg;
            //int a;
            //obj.a = 3;
            a=4;
             a[b] = 4;
            c=2;
        {
            int fg;
        
        
        
        }
            d=1;
            b=c*d;
            a = temp(3,4);
            return;
           
        }
        
        int temp( int a,int b)
        {
            
            //bool b;
            //x=2;
            {
            int b;
            }
           
            return 3;
        
        }
        
            '''
    result = parser.parse(s)
    astRoot = yacc.parse(s)
    print 'Done with parsing'
    
    ismain(result)
    if done == 0:
        print "Main function ERROR: Main Function Not WellFormed"
        sys.exit(-1)
    
    isreturn(result)

    declareonce(result,decl,parent)
    
    wellformed(result,decl,defined)
    '''
    welltyped(result,vars)'''
