# Yacc example
#import pydot

import ply.yacc as yacc
from collections import *
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
    '''ClassDecl : CLASS ID Extends LCURLY MemberDeclSeq RCURLY
        | CLASS ID LCURLY MemberDeclSeq RCURLY '''
    if len(p) == 6:
        p[2] = Node("ID", leaf = p[2])
        p[3] = Node("LCURLY", leaf = p[3])
        p[5] = Node("RCURLY", leaf = p[5])
        p[0] = Node("ClassDecl", children = [p[2], p[3], p[4], p[5]])
    else:
        p[2] = Node("ID", leaf = p[2])
        p[4] = Node("LCURLY", leaf = p[4])
        p[6] = Node("RCURLY", leaf = p[6])
        p[0] = Node("ClassDecl", children = [p[2], p[3], p[4], p[5], p[6]])

def p_extends(p):
    'Extends : EXTENDS ID'
    p[2] = Node("ID", leaf = p[2])
    p[0] = Node("Extends", children = [p[2]])


def p_memberdeclseq_var(p):                                                # for Decl in classes
    'MemberDeclSeq : VarDecl MemberDeclSeq'
    p[0] = Node("MemberDeclSeq_Var", children = [p[1], p[2]])

def p_memberdeclseq_func(p):
    'MemberDeclSeq : FunDecl MemberDeclSeq'
    p[0] = Node("MemberDeclSeq_Func", children = [p[1], p[2]])

def p_memberdeclseq_null(p):
    'MemberDeclSeq : '
    p[0] = Node("MemberDeclSeq")


'''
    def p_vardeclseq(p):                                                # for Decl in classes
    'VarDeclSeq : VarDecl VarDeclSeq'
    p[0] = Node("VarDeclSeq", children = [p[1], p[2]])
    
    def p_vardeclseq_null(p):
    'VarDeclSeq : '
    p[0] = Node("VarDeclSeq")
    '''

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
        p[0] = Node("RetStmt", children = [p[1], p[2]])
    else:
        p[3] = Node("SEMI", leaf = p[3])
        p[1] = Node("RETURN", leaf = p[1])
        p[0] = Node("RetStmt", children = [p[1], p[2], p[3]])


def p_se(p):
    '''SE : Assign
        | MethodCall'''
    p[0] = Node("SE", children = [p[1]])

def p_assign(p):
    'Assign : Lhs EQ AE'
    p[2] = Node("EQ", leaf  = p[2])
    p[0] = Node("SEEq", children = [p[1], p[2], p[3]])

def p_se_post(p):
    '''Assign : Lhs INC
        | Lhs DEC'''
    p[2] = Node("POST", leaf = p[2])
    p[0] = Node("SEPost", children = [p[1], p[2]])

def p_se_pre(p):
    '''Assign : INC Lhs
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
        | MethodCall
        | NewObject '''
    p[0] = Node("Primary", children = [p[1]])

def p_primary_const(p):
    '''Primary : TRUE
        | FALSE
        | NUMBER
        | THIS
        | SUPER'''
    if ("true" in p):
        p[0] = Node("bool", leaf = p[1])
    elif ("false" in p):
        p[0] = Node("bool", leaf = p[1])
    elif ("this" in p):
        p[0] = Node("this", leaf = p[1])
    elif ("super" in p):
        p[0] = Node("super", leaf = p[1])
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

def p_methodcall(p):
    '''MethodCall : FieldAccess LPAREN Args RPAREN
        | FieldAccess LPAREN RPAREN'''
    p[2] = Node("LPAREN", leaf = p[2])
    if len(p) == 4:
        p[3] = Node("RPAREN", leaf = p[3])
        p[0] = Node("MethodCall", children = [p[1], p[2], p[3]])
    else:
        p[4] = Node("RPAREN", leaf = p[4])
        p[0] = Node("MethodCall", children = [p[1], p[2], p[3], p[4]])

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
    p[0] = Node("DimExpr", children = [p[1], p[2], p[3]])


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
fundict = defaultdict(list)
parent = None
done = [0]
vars = {}
found = [0]
inclass = 0
classdict = {}
inherit = {}
currentclass = None
classobj = {}
candidate = {}
func = []
returndict = {}
currentfunc = None
thisclass = None
arglist = []
field = 0
type = None

##############################################################################################

def wellformed(node,decl,defined,classobj,candidate):
    global currentclass
    global thisclass
    global inherit
    #print inclass
    #print currentclass
    #print node
    #print node.type
    iterable_list = node.children[:]
    
    
    # print node.type
    
    if node.type == "MethodCall":
        field = node.children[0]
        if len(field.children) > 1:
            primary = field.children[0]
            member = field.children[2].leaf
            if primary.type == "this":
                if (thisclass,member) not in fundict.keys():
                    print "Wellformed ERROR: INVALID FUNCTION CALL for"" + thisclass+ member +  for THIS"
                    sys.exit(-1)
                wellformed(node.children[2],decl,defined,classobj,candidate)
                return
            elif primary.type == "super":
                if thisclass not in inherit.keys():
                    print "Wellformed ERROR: CLASS\"" + thisclass + "\" DOES NOT INHERIT"
                    sys.exit(-1)
                classid = inherit[thisclass]
                if (classid,member) not in fundict.keys():
                    print "Wellformed ERROR: INVALID FUNCTION CALL for" + classid + member + " for SUPER"
                    sys.exit(-1)
                wellformed(node.children[2],decl,defined,classobj,candidate)
                return
            while primary.type != "ID":
                iterable_list = primary.children[1:]
                for child in iterable_list:
                    wellformed(child,decl,defined,classobj,candidate)
                primary = primary.children[0]
            varid = primary.leaf
            if varid not in classobj.keys():
                print "WellTyped ERROR: Variable  /" + varid +" Not a CLASS VARIABLE"
                sys.exit(-1)
            classid = classobj[varid]
            if (classid,member) in fundict.keys():
                wellformed(node.children[2],decl,defined,classobj,candidate)
                return
            while classid in inherit.keys():
                classid = inherit[classid]
                if (classid,member) in fundict.keys():
                    wellformed(node.children[2],decl,defined,classobj,candidate)
                    return
            print "Wellformed ERROR: INVALID FUNCTION CALL for" + classid + member + varid +" for METHODCALL for OBJECT"
            sys.exit(-1)



        wellformed(node.children[2],decl,defined,classobj,candidate)
        return

    if node.type == "NewObject":
        id = node.children[1].leaf
        if id not in classdict.keys():
            print "Wellformed ERROR: CLASS\"" + id + "\" NOT A valid CLASS [NOT DECLARED]"
            sys.exit(-1)
        return

    if node.type == "NewArray":
        wellformed(node.children[2],decl,defined,classobj,candidate)
        Type = node.children[1]
        if len(Type.children) > 0:
            id = Type.children[0].leaf
            if id not in classdict.keys():
                print "Wellformed ERROR: ARAAY TYPE\"" + id + "\" UNDEFINED"
                sys.exit(-1)
        return


    if node.type == "FunDecl":
        temp_decl = decl[:]
        temp_defined = defined[:]
        temp_classobj = classobj.copy()
        temp_candidate = candidate.copy()
        iterable_list = node.children[4:]
        for child in iterable_list:
            wellformed(child,temp_decl,temp_defined,temp_classobj,temp_candidate)
        return

    if node.type == "Formals":
        id = node.children[1].leaf
        typenode = node.children[0]
        if len(typenode.children) > 0:
            type = typenode.children[0].leaf
            classobj[id] = type
        else:
            type = typenode.leaf
            decl.append(id)
            defined.append(id)

        if len(node.children) > 3 :
            wellformed(node.children[4],decl,defined,classobj,candidate)
        return

    if node.type == "ClassDecl":
        thisclass = node.children[0].leaf
        iterable_list = node.children[2:]
        for child in iterable_list:
            wellformed(child,decl,defined,classobj,candidate)
        thisclass = None
        return


    if node.type == "MemberDeclSeq_Var":
        wellformed(node.children[1],decl,defined,classobj,candidate)
        return

    if node.type == "MemberDeclSeq_Func":
        fundecl = node.children[0]
        temp_decl = []
        temp_defined = []
        temp_classobj = {}
        temp_candidate = {}
        iterable_list = fundecl.children[4:]
        for child in iterable_list:
            wellformed(child,temp_decl,temp_defined,temp_classobj,temp_candidate)
        wellformed(node.children[1],decl,defined,classobj,candidate)
        return



    if(node.type == "if"):
        if(len(node.children) == 3):
            temp_decl = decl[:]
            temp_defined = defined[:]
            temp_classobj = classobj.copy()
            temp_candidate = candidate.copy()
            #temp_parent = node.type
            wellformed(node.children[0],temp_decl,temp_defined,temp_classobj,temp_candidate)
            wellformed(node.children[1],temp_decl,temp_defined,temp_classobj,temp_candidate)
            #print temp_decl
            #print temp_defined
            set_def = set(temp_defined).difference(set(defined))
            #print set_def
            #print temp_decl
            set_dec = set(temp_decl).difference(set(decl))
            #print set_dec
            set_1 = set_def.difference(set_dec)
            #print set_1
            
            wellformed(node.children[2],temp_decl,temp_defined,temp_classobj,temp_candidate)
            #print temp_decl
            #print temp_defined
            set_def2 = set(temp_defined).difference(set(defined))
            set_dec2 = set(temp_decl).difference(set(decl))
            set_2 = set_def2.difference(set_dec2)
        # print set_2
        
        else:
            temp_decl = decl[:]
            temp_defined = defined[:]
            temp_classobj = classobj.copy()
            temp_candidate = candidate.copy()
            #print decl[:]
            #temp_parent = node.type
            for child in iterable_list:
                #print child
                wellformed(child,temp_decl,temp_defined,temp_classobj,temp_candidate)
        #print decl[:]
        return


    elif(node.type == "while"):
        temp_decl = decl[:]
        temp_defined = defined[:]
        temp_classobj = classobj.copy()
        temp_candidate = candidate.copy()
        #print decl[:]
        #temp_parent = node.type
        for child in iterable_list:
            #print child
            wellformed(child,temp_decl,temp_defined,temp_classobj,temp_candidate)
        #print decl[:]
        return

    elif(node.type == "do"):
        #print "here"
        temp_decl = decl[:]
        temp_classobj = classobj.copy()
        temp_candidate = candidate.copy()
        #temp_parent = node.type
        for child in iterable_list:
            #print defined[:]
            wellformed(child,temp_decl,defined,temp_classobj,temp_candidate)
        # print defined[:]
        #print decl[:]
        #print defined[:]
        return

    elif(node.type == "for"):
        #temp_parent = node.type
        if(node.children[0].type == "SEOpt"):
            wellformed(node.children[0],decl,defined,classobj,candidate)
            iterable_list = node.children[1:]
        temp_decl = decl[:]
        temp_defined = defined[:]
        temp_classobj = classobj.copy()
        temp_candidate = candidate.copy()
        for child in iterable_list:
            #print child
            wellformed(child,temp_decl,temp_defined,temp_classobj,temp_candidate)
        #print decl[:]
        return

    
    elif(node.type == "Stmt"):
        #temp_parent = node.type
        if(node.children[0].type == "Block"):
            temp_decl = decl[:]
            temp_classobj = classobj.copy()
            temp_candidate = candidate.copy()
            #print decl[:]
            for child in iterable_list:
                wellformed(child,temp_decl,defined,temp_classobj,temp_candidate)
            
            return



    elif(node.type == "VarDecl"):
        Type = node.children[0]
        if len(Type.children) != 0:
            if Type.children[0].type == "ID":
                classid = Type.children[0].leaf
                if classid not in classdict.keys():
                    print "Wellformed ERROR: CLASS NAME \"" + classid + "\" NOT DECLARED before use"
                    sys.exit(-1)
                currentclass = classid
                iterable_list = node.children[1:]
                for child in iterable_list:
                    wellformed(child,decl,defined,classobj,candidate)
                currentclass = None
                return





    elif(node.type == "Var"):
        varid = node.children[0].leaf
        if currentclass != None:
            if varid not in classobj.keys():
                classobj[varid] = currentclass
            else:
                print "DeclareOnce ERROR: Class Variable \"" + varid + "\" Declared Twice in same scope"
                sys.exit(-1)
        else:
            decl.append(varid)
        iterable_list = node.children[1:]


    elif node.type == "FieldAccess":
        #print "here"
        #print len(node.children)
        if len(node.children) > 1:
            member = node.children[2].leaf
            primary = node.children[0]
            #print thisclass
            #print classdict
            if primary.type == "this":
                if not member in classdict[thisclass]:
                    print "Wellformed ERROR: Class Variable \"" + member + "\" NOT DECLARED before use"
                    sys.exit(-1)
                return
            if primary.type == "super":
                if thisclass not in inherit.keys():
                    print "Wellformed ERROR: CLASS\"" + thisclass + "\" DOES NOT INHERIT"
                    sys.exit(-1)
                superclass = inherit[thisclass]
                if not member in classdict[superclass]:
                    print "Wellformed ERROR: Class Variable \"" + member + "\" NOT DECLARED before use"
                    sys.exit(-1)
                return
            while primary.type != "ID":
                iterable_list = primary.children[1:]
                for child in iterable_list:
                    wellformed(child,decl,defined,classobj,candidate)
                primary = primary.children[0]
            varid = primary.leaf
            if varid not in classobj.keys():
                print "WellTyped ERROR: Variable" + varid +" Not a CLASS VARIABLE"
                sys.exit(-1)
            classname = classobj[varid]
            if member in classdict[classname]:
                return
            while classname in inherit.keys():
                classname = inherit[classname]
                if member in classdict[classname]:
                    return
            print "WellTyped ERROR: FieldAccess for CLASS MEMBER NOT PRESENT IN ANY SUPERCLASS"
            sys.exit(-1)
        else:
            #print node.children[0].leaf
            wellformed(node.children[0],decl,defined,classobj,candidate)
            return


    elif node.type == "ArrayAccess":
        iterable_list = node.children[1:]
        for child in iterable_list:
            wellformed(child,decl,defined,classobj,candidate)
        primary = node.children[0]
        while primary.type != "ID":
            iterable_list = primary.children[1:]
            for child in iterable_list:
                wellformed(child,decl,defined,classobj,candidate)
            
            primary = primary.children[0]
        id = primary.leaf
        if id not in classobj.keys() and id not in decl:
            print "Wellformed ERROR: Array Variable \"" + id + "\" NOT DECLARED before use"
            sys.exit(-1)
        return

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
            #print child.leaf
            wellformed(child,decl,defined,classobj,candidate)
        
        lhs = node.children[0]
        if lhs.children[0].type == "FieldAccess" and len(lhs.children[0].children)==1:
            field = lhs.children[0]
            if field.children[0].type == "ID":
                id = field.children[0].leaf
                if id in classobj.keys():
                    return
                if not id in decl:
                    print "Wellformed ERROR: Variable \"" + id + "\" NOT DECLARED before use"
                    sys.exit(-1)
                    return []
                elif id in defined:
                    pass
                else:
                    defined.append(id)
        else:
            wellformed(lhs,decl,defined,classobj,candidate)

    
    
    #print "-----" + id
    #print defined[:]
    
    
    #temp_parent = node.type
    for child in iterable_list:
        #print child.type
        wellformed(child,decl,defined,classobj,candidate)

    return
################################################################################

def ismain(node,done):
    iterable_list = node.children[:]
    
    if node.type == "ClassDecl":
        return
    
    if node.type == "FunDecl":
        if node.children[1].leaf == "main" and node.children[0].leaf == "void" and node.children[4].type == "RPAREN":
            
            done[0] = 1

    for child in iterable_list:
        #print child.type
        ismain(child,done)
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

    elif(node.type == "RetStmt"):
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
    
    
    if node.type == "MethodCall":
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
        if id in func or id in classdict.keys():
            print "Declare-Once ERROR: Variable \"" + id + "\" Alreay used as CLASS/FUNCTION name"
            sys.exit(-1)
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

def welltyped(node,vars,classobj):
    global field
    global currentclass
    global thisclass
    global arglist
    #print vars
    iterable_list = node.children[:]
    
    if node.type == "ClassDecl":
        thisclass = node.children[0].leaf
        iterable_list = node.children[2:]
        temp_vars = {}
        temp_classobj = {}
        for child in iterable_list:
            welltyped(child,temp_vars,temp_classobj)
        thisclass = None
        return
    
    
    elif node.type == "MemberDeclSeq_Var":
        return
    
    elif node.type == "MemberDeclSeq_Func":
        fundecl = node.children[0]
        temp_vars = {}
        temp_classobj = {}
        iterable_list = fundecl.children[4:]
        for child in iterable_list:
            welltyped(child,temp_vars,temp_classobj)
        return


    elif node.type == "MethodCall":
        #print "here"
        field = node.children[0]
        if len(field.children) > 1:
            primary = field.children[0]
            member = field.children[2].leaf
            arglist = []
            if node.children[2].type == "Args":
                welltyped(node.children[2],vars,classobj)
                extractarg(node.children[2],vars,classobj)
            #print arglist
            if primary.type == "this":
                size = len(arglist)
                for child in fundict[(thisclass,member)]:
                    if size == len(child):
                        comp = [i for i, j in zip(arglist,child) if i == j]
                        if len(comp) == size:
                            return
                print "WellTYped ERROR: METHODCALL CLASS\"" + thisclass + "\" THIS"
                sys.exit(-1)
        
            elif primary.type == "super":
                
                classid = inherit[thisclass]
                size = len(arglist)
                for child in fundict[(classid,member)]:
                    if size == len(child):
                        comp = [i for i, j in zip(arglist,child) if i == j]
                        if len(comp) == size:
                            return
                print "WellTYped ERROR: METHODCALL CLASS\"" + classid + "\" SUPER"
                sys.exit(-1)
            while primary.type != "ID":
                iterable_list = primary.children[1:]
                #for child in iterable_list:
                #wellformed(child,decl,defined,classobj,candidate)
                primary = primary.children[0]
            varid = primary.leaf
            classid = classobj[varid]
            if (classid,member) in fundict.keys():
                size = len(arglist)
                for child in fundict[(classid,member)]:
                    if size == len(child):
                        comp = [i for i, j in zip(arglist,child) if i == j]
                        if len(comp) == size:
                            return
            while classid in inherit.keys():
                classid = inherit[classid]
                if (classid,member) in fundict.keys():
                    wellformed(node.children[2],decl,defined,classobj,candidate)
                    return
            print "WellTYped ERROR: METHODCALL CLASS\"" + classid + "\" for ID"
            sys.exit(-1)
        return

    elif node.type == "IntConst":
        node.check = "int"
        return

    elif node.type == "bool":
        node.check = "bool"
        return

    elif node.type == "FunDecl":
        iterable_list = node.children[4:]



    elif node.type == "Formals":
        typenode = node.children[0]
        id = node.children[1].leaf
        if len(typenode.children) > 0:
            type = typenode.children[0].leaf
            classobj[id] = type
        else:
            type = typenode.leaf
            vars[id] = type
        
        if len(node.children) > 3 :
            welltyped(node.children[4],vars,classobj)
        return

    
    elif node.type == "VarDecl":
        if node.children[0].leaf == "int" or node.children[0].leaf == "bool":
            type = node.children[0].leaf
            varlist = node.children[1]
            while (len(varlist.children) != 1):
                varnode = varlist.children[0]
                vars[varnode.children[0].leaf] = type
                varlist = varlist.children[2]
            varnode = varlist.children[0]
            #print vars
            vars[varnode.children[0].leaf] = type
            node.check = type
        
        Type = node.children[0]
        if len(Type.children) != 0:
            if Type.children[0].type == "ID":
                classid = Type.children[0].leaf
                if classid not in classdict.keys():
                    print "Wellformed ERROR: CLASS NAME \"" + classid + "\" NOT DECLARED before use"
                    sys.exit(-1)
                currentclass = classid
                iterable_list = node.children[1:]
                for child in iterable_list:
                    welltyped(child,vars,classobj)
                currentclass = None
        return

    
    elif node.type == "var":
        varid = node.children[0].leaf
        if currentclass != None:
            if varid not in classobj.keys():
                classobj[varid] = currentclass
            else:
                print "DeclareOnce ERROR: Class Variable \"" + varid + "\" Declares Twice in same scope"
                sys.exit(-1)
        return

    
    elif node.type == "Unop":
        welltyped(node.children[0],vars,classobj)
        if node.leaf == "UMINUS":
            if node.children[0].check == "int":
                node.check = "int"
            else:
                print "WellTyped ERROR: Unop"
                sys.exit(-1)
        else:
            if node.children[0].check == "bool":
                node.check = "bool"
            else:
                print "WellTyped ERROR: Unop"
                sys.exit(-1)
        return

    elif node.type == "Binop":
        welltyped(node.children[0],vars,classobj)
        welltyped(node.children[1],vars,classobj)
        if node.leaf in ["+", "-", "*", "/", "%"]:
            if node.children[0].check == "int" and node.children[1].check == "int":
                node.check = "int"
            else:
                print "WellTyped ERROR: Binop"
                sys.exit(-1)

        elif node.leaf in ["==", "!="]:
            if node.children[0].check == "int" and node.children[1].check == "int":
                node.check = "bool"
            elif node.children[0].check == "bool" and node.children[1].check == "bool":
                node.check = "bool"
            else:
                print "WellTyped ERROR: Binop"
                sys.exit(-1)

        elif node.leaf in ["<", ">", "<=", ">="]:
            if node.children[0].check == "int" and node.children[1].check == "int":
                node.check = "bool"
            else:
                print "WellTyped ERROR: Binop"
                sys.exit(-1)

        elif node.leaf in ["||", "&&"]:
            if node.children[0].check == "bool" and node.children[1].check == "bool":
                node.check = "bool"
            else:
                print "WellTyped ERROR: binop"
                print node.children[0].check
                print node.children[1].check
                sys.exit(-1)
        return

    
    elif node.type == "SEEq":
        ae = node.children[2]
        lhs = node.children[0]
        if ae.children[0].type == "Primary" and ae.children[0].children[0].type == "NewObject":                  # Case for New obj Heap space
            classid = ae.children[0].children[0].children[1].leaf
            access = lhs.children[0]
            while access.type != "ID":
                access =  access.children[0]
            id = access.leaf
            if id not in classobj.keys():
                print "WellTyped ERROR: SEEq for NewObject"
                sys.exit(-1)
            classid1 = classobj[id]
            if classid != classid1:
                print "WellTyped ERROR: SEEq for NewObject"
                sys.exit(-1)
            return

        elif ae.children[0].type == "NewArray":                          # Case for New array Heap space
            new = ae.children[0]
            typenode = new.children[1]
            if len(typenode.children) == 0 :
                type = typenode.leaf
            else:
                type = typenode.children[0].leaf
            access = lhs.children[0]
            while access.type != "ID":
                access =  access.children[0]
            id = access.leaf
            if id in classobj.keys():
                type1 = classobj[id]
            else:
                type1 = vars[id]
            if type != type1:
                print "WellTyped ERROR: SEEq for NewArray"
                sys.exit(-1)
            
            welltyped(new.children[2].children[1],vars,classobj)
            return

        elif ae.children[0].type == "SE" or ae.children[0].type == "Primary":
            if ae.children[0].children[0].type == "MethodCall":                # for methodcall
                welltyped(ae.children[0].children[0],vars,classobj)
                return


        elif lhs.children[0].type == "FieldAccess" and len(lhs.children[0].children) > 1:
            welltyped(lhs.children[0],vars,classobj)
            return
        welltyped(node.children[0],vars,classobj)
        welltyped(node.children[2],vars,classobj)
        if node.children[0].check == node.children[2].check:
            node.check = node.children[2].check
        else:
            print "WellTyped ERROR: SEEq"
            sys.exit(-1)
        return


    elif node.type == "SEPost":
        welltyped(node.children[0],vars,classobj)
        if node.children[0].check == "int":
            node.check = "int"
        else:
            print "WellTyped ERROR: SEPost"
            sys.exit(-1)
        return

    elif node.type == "SEPre":
        welltyped(node.children[1],vars,classobj)
        if node.children[1].check == "int":
            node.check = "int"
        else:
            print "WellTyped ERROR: SEPre"
            sys.exit(-1)
        return

    elif node.type == "AEOpt":
        if len(node.children) > 0:
            welltyped(node.children[0],vars,classobj)
        node.check = node.children[0].check


    elif node.type == "print":
        welltyped(node.children[0],vars,classobj)
        if node.children[0].check != "int":
            print "WellTyped ERROR: print"
            sys.exit(-1)
        return

    elif node.type == "if":
        iterable_list = node.children[:]
        temp_classobj = classobj.copy()
        temp_vars = vars.copy()
        for child in iterable_list:
            welltyped(child,temp_vars,temp_classobj)
        if node.children[0].check != "bool":
            print "WellTyped ERROR: if"
            sys.exit(-1)

        return

    elif node.type == "while":
        iterable_list = node.children[:]
        temp_classobj = classobj.copy()
        temp_vars = vars.copy()
        for child in iterable_list:
            welltyped(child,temp_vars,temp_classobj)
        if node.children[0].check != "bool":
            print "WellTyped ERROR: while"
            sys.exit(-1)

        return

    elif node.type == "do":
        iterable_list = node.children[:]
        temp_classobj = classobj.copy()
        temp_vars = vars.copy()
        for child in iterable_list:
            welltyped(child,temp_vars,temp_classobj)
        if node.children[1].check != "bool":
            print "WellTyped ERROR: D0-while"
            sys.exit(-1)

        return

    elif(node.type == "for"):
        if(node.children[0].type == "SEOpt"):
            welltyped(node.children[0],vars,classobj)
            iterable_list = node.children[1:]
        temp_vars = vars.copy()
        temp_classobj = classobj.copy()
        for child in iterable_list:
            welltyped(child,temp_vars,temp_classobj)

        if node.children[2].check != "bool":
            print "WellTyped ERROR: for"
            sys.exit(-1)

        return
    
    
    elif node.type == "Lhs":
        welltyped(node.children[0],vars,classobj)
        node.check = node.children[0].check
        if node.check == "error":
            print "WellTyped ERROR: Lhs"
            sys.exit(-1)
        return

    elif node.type == "AE":
        welltyped(node.children[0],vars,classobj)
        #print node.children[0].type
        if node.children[0].type != "SE":
            #print node.children[0].check
            node.check = node.children[0].check
            if node.check == "error":
                print "WellTyped ERROR: AE"
                sys.exit(-1)
            return
        node.check = "int"
        return

    elif node.type == "Primary":
        #print node.children[0].type
        welltyped(node.children[0],vars,classobj)
        node.check = node.children[0].check
        if node.check == "error":
            print "WellTyped ERROR: Primary"
            sys.exit(-1)
        return

    
    elif node.type == "NewArray":
        welltyped(node.children[1],vars,classobj)
        #print node.children[1].type
        node.check = node.children[1].check
        return




    elif node.type == "FieldAccess":
        if len(node.children) > 1:
            member = node.children[2]
            node.check = "int"
            return
        else:
            welltyped(node.children[0],vars,classobj)
            node.check = node.children[0].check
            if node.check == "error":
                print "WellTyped ERROR: FieldAccess for ID"
                sys.exit(-1)

        return



    elif node.type == "ArrayAccess":
        x = 0
        if field == 1:
            field = 0
            x=1
        welltyped(node.children[1],vars,classobj)
        if node.children[1].check != "int":
            node.check = "error"
            if node.check == "error":
                print "WellTyped ERROR: ArrayAccess Part 1"
                sys.exit(-1)
            return
        if x == 1:
            field = 1
        welltyped(node.children[0],vars,classobj)
        node.check = node.children[0].check
        if node.check == "error":
            print "WellTyped ERROR: ArrayAccess"
            sys.exit(-1)

        return


    elif node.type == "NewObject":
        id = node.children[1].leaf
        if id not in classdict.keys():
            node.check = "error"
            if node.check == "error":
                print "WellTyped ERROR: NewObject"
                sys.exit(-1)
        else:
            node.check = node.children[1].leaf
        return


    elif node.type == "Type":
        if len(node.children)>0:
            welltyped(node.children[0],vars,classobj)
            node.check = node.children[0].check
        else:
            node.check = node.leaf
        return


    elif node.type == "ID":
        id = node.leaf
        if field == 1:
            if id in classobj.keys():
                node.check = classobj[id]
            else:
                node.check = "error"
                if node.check == "error":
                    print "WellTyped ERROR: Class ID" + id
                    sys.exit(-1)

            return
        else:
            if currentclass != None:
                classobj[id] = currentclass
                node.check = currentclass
                return
            if id in vars.keys():
                node.check = vars[id]
            else:
                node.check = "error"
                if node.check == "error":
                    print "WellTyped ERROR: ID in vars" + id
                    sys.exit(-1)

            return
    
    elif(node.type == "Stmt"):
        #temp_parent = node.type
        if(node.children[0].type == "Block"):
            temp_vars = vars.copy()
            temp_classobj = classobj.copy()
            #print decl[:]
            for child in iterable_list:
                welltyped(child,temp_vars,temp_classobj)
            
            return


    #temp_parent = node.type
    for child in iterable_list:
        #print child.type
        welltyped(child,vars,classobj)

    return


################################################################################


def find(node):
    global func
    global inclass
    global currentclass
    global classdict
    global type
    #print inclass
    #print currentclass
    #print node
    #print node.type
    iterable_list = node.children[:]
    
    
    if node.type == "FunDecl" and inclass == 0:
        funid = node.children[1].leaf
        func.append(funid)
        return
    
    elif node.type == "FunDecl" and inclass == 1:
        return
    
    elif node.type == "ClassDecl":
        iterable_list = node.children[2:]
        inclass = 1
        currentclass = node.children[0].leaf
        classdict[currentclass] = []
        for child in iterable_list:
            find(child)
        inclass = 0
        currentclass = None
        return

    elif node.type == "Type" and len(node.children) == 0:
        type = node.leaf
        return

    
    elif(node.type == "Var"):
        id = node.children[0].leaf
        if inclass == 1:
            if  currentclass not in classdict.keys():
                classdict[currentclass] = [type]
                classdict[currentclass].append(id)
            else:
                classdict[currentclass].append(type)
                classdict[currentclass].append(id)
        iterable_list = node.children[1:]

    #temp_parent = node.type
    for child in iterable_list:
        #print child.type
        find(child)

    return


################################################################################

def findfunc(node):
    global func
    global inclass
    global currentclass
    global fundict
    global type
    global inherit
    #print inclass
    #print currentclass
    #print node
    #print node.type
    iterable_list = node.children[:]
    
    '''
        if node.type == "FunDecl":
        funid = node.children[1].leaf
        func.append(funid)
        for child in iterable_list:
        find(child)
        return
        '''
    if node.type == "ClassDecl":
        iterable_list = node.children[2:]
        currentclass = node.children[0].leaf
        if node.children[1].type == "Extends":
            extend = node.children[1]
            super = extend.children[0].leaf
            inherit[currentclass] = super
        inclass = 1
        currentclass = node.children[0].leaf
        for child in iterable_list:
            findfunc(child)
        inclass = 0
        currentclass = None
        return
    
    
    elif node.type == "FunDecl" and inclass == 1:
        global arglist
        fundecl = node
        funid = fundecl.children[1].leaf
        del arglist[:]
        if fundecl.children[4].type == "Formals":
            findarg(fundecl.children[4])
        size = len(arglist)
        if (currentclass,funid) not in fundict.keys():
            temp_arglist = arglist[:]
            fundict[(currentclass,funid)] = [temp_arglist]
            return
        for child in fundict[(currentclass,funid)]:
            
            if size == len(child):
                comp = [i for i, j in zip(arglist,child) if i == j]
                if len(comp) == size:
                    print "DeclareOnce ERROR: FUNCTION \"" + funid + "\" Declared Twice in same CLASS"
                    exit(-1)
        
        temp_arglist = arglist[:]
        fundict[(currentclass,funid)].append(temp_arglist)
        

        return
    
    
    
    #temp_parent = node.type
    for child in iterable_list:
        #print child.type
        findfunc(child)
    
    return

################################################################################

def findarg(node):
    global arglist
    typenode = node.children[0]
    if len(typenode.children) > 0:
        type = typenode.children[0].leaf
    else:
        type = typenode.leaf
    arglist.append(type)
    if len(node.children) > 3:
        findarg(node.children[4])
    else:
        return

################################################################################

def extractarg(node,vars,classobj):
    global arglist
    welltyped(node.children[0],vars,classobj)
    arglist.append(node.children[0].check)
    
    if len(node.children) > 1:
        extractarg(node.children[2],vars,classobj)
    else:
        return


################################################################################

if __name__ == "__main__":
    s = '''
        void f1(int n)
        {
        int x, y, z;
        x = 4;
        y=1;
        z = n;
        
        n = n-1;
        
        if n > 0 then
		f1(n);
        
        print(n);
        z=x+y+z;
        print(z);
        
        return ;
        }
        
        void main()
        {
        int x, y, z;
        x = 4;	
        y=1;
        z = 1;
        
        f1(x);
        
        z=x+y+z;
        print(z);
        
        return;
        }



        '''
    result = yacc.parse(s)
    print 'Done with parsing'
    
    ismain(result,done)
    if done[0] == 0:
        print "Main function ERROR: Main Function Not WellFormed"
        sys.exit(-1)
    
    isreturn(result)
    


    find(result)
    findfunc(result)
    #print inherit
    #print fundict
    #print func
    #print classdict
    
    #print func[:]
    declareonce(result,decl,parent)
    
    wellformed(result,decl,defined,classobj,candidate)
    
    welltyped(result,vars,classobj)
