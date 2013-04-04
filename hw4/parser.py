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
    def __init__(self,type,children=None,leaf=None):
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

##################
def p_pgm_stmtseq(p):
    'Pgm : DeclSeq StmtSeq '
    p[0] = Node("Pgm", children = [p[1], p[2]])


def p_stmtseq_stmt_stmtseq(p):
    'StmtSeq : Stmt StmtSeq'
    p[0] = Node("stmtseq",children = [p[1],p[2]])

def p_stmtseq_null(p):
    'StmtSeq : '
    p[0] = Node("stmtseq", [])

def p_stmt(p):
    '''Stmt : SE SCOLON
       Stmt : PRINT LPAREN AE RPAREN SCOLON
       Stmt : LCURLY DeclSeq StmtSeq RCURLY
       Stmt : IF AE THEN Stmt ELSE Stmt
       Stmt : IF AE THEN Stmt
       Stmt : WHILE AE DO Stmt
       Stmt : FOR LPAREN SEOpt SCOLON AEOpt SCOLON SEOpt RPAREN Stmt
       Stmt : DO Stmt WHILE AE SCOLON'''
    if len(p) == 3:
        p[2] = Node("SEMI", leaf = p[2])
        p[0] = Node("Stmt", children = [p[1], p[2]])
    elif len(p) == 5:
        p[0] = Node("Stmt", children = [p[1], p[2], p[3], p[4]])
    elif len(p) == 6:
        p[0] = Node("Stmt", children = [p[1], p[2], p[3], p[4], p[5]])
    elif len(p) == 7:
        p[0] = Node("Stmt", children = [p[1], p[2], p[3], p[4], p[5], p[6]])
    elif len(p) == 10:
        p[0] = Node("Stmt", children = [p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9]])

def p_seopt(p):
    '''SEOpt : SE
       SEOpt : '''
    if len(p) == 1:
        p[0] = Node("SEOpt", [])
    else:
        p[0] = Node("SEOpt", p[1])

def p_aeopt(p):
    '''AEOpt : AE
       AEOpt : '''
    if len(p) == 1:
        p[0] = Node("AEOpt", [])
    else:
        p[0] = Node("AEOpt", p[1])

def p_declseq(p):
    'DeclSeq : Decl DeclSeq'
    p[0] = Node("DeclSeq", children = [p[1], p[2]])

def p_declseq_null(p):
    'DeclSeq : '
    p[0] = Node("DeclSeq", [])

def p_decl(p):
    'Decl : Type VarList SCOLON'
    p[0] = Node("Decl", children = [p[1], p[2], p[3]])

def p_type(p):
    '''Type : INT
          | BOOL'''
    p[0] = Node("Type", p[1])

def p_varlist(p):
    '''VarList : Var COMMA VarList
       VarList : Var'''
    if len(p) == 2:
        p[0] = Node("VarList", p[1])
    elif len(p) == 4:
        p[0] = Node("VarList", p[1])

def p_var(p):
    'Var : ID DimStar'
    p[0] = Node("Var", children = [p[0], p[1]])

def p_se(p):
    '''SE : Lhs EQ AE
       SE : Lhs INC
       SE : Lhs DEC
       SE : INC Lhs
       SE : DEC Lhs '''
    if len(p) == 3:
        p[0] = Node("SE", children = [p[1], p[2]])
    elif len(p) == 4:
        p[0] = Node("SE", children = [p[1], p[2], p[3]])

def p_lhs(p):
    '''Lhs : ID
           | Lhs LSQR AE RSQR'''
    if len(p) == 2:
        p[0] = Node("Lhs", p[1])
    elif len(p) == 5:
        p[0] = Node("Lhs", children = [p[1], p[2], p[3], p[4]])         
     
def p_dimexpr(p):
    'DimExpr : LSQR AE RSQR'
    p[0] = Node("DimExpr", children = [p[0], p[1], p[2]])

def p_dimstar(p):
    '''DimStar : LSQR RSQR DimStar
       DimStar : '''
    if len(p) == 1:
        p[0] = Node("DimStar", [])
    elif len(p) == 3:
        p[0] = Node("DimStar", children = [p[0], p[1], p[2]])

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
    p[0] = Node("Binop", [p[1], p[3]], p[2])

def p_ae_uminus(p):
    'AE : MINUS AE %prec UMINUS'
    p[0] = Node("Unop", [p[2]], "UMINUS")

def p_ae_not(p):
    'AE : NOT AE'
    p[0] = Node("Unop", [p[2]], "NOT")

def p_ae_lhs(p):
    'AE : Lhs'
    p[0] = p[1]

def p_ae_se(p):
    'AE : SE'
    p[0] = p[1]

def p_ae_ip(p):
    'AE : INPUT LPAREN RPAREN'
    p[0] = Node("AE", children = [p[1], p[2], p[3]])

def p_ae_aeparan(p):
    'AE : LPAREN AE RPAREN'
    p[0] = Node("AE", children = [p[1], p[2], p[3]])

def p_ae_new_expr(p):
    'AE : NEW Type DimExpr DimStar'
    p[0] = Node("AE", children = [p[1], p[2], p[3], p[4]])

def p_ae_misc(p):
    '''AE : TRUE
          | FALSE
          | NUMBER '''
    p[0] = Node("AE", p[1])

def p_error(p):
    if p==None:
       print "Syntax error found at 'End Of File' Probably because of missing right curly brace"
       sys.exit()
    else :
        print "Syntax error in line number %d just before token '%s' of value '%s' " % (p.lineno,p.type,p.value)
	sys.exit()

parser = yacc.yacc()

def inside_loop(node):
    left_list = []
    right_list = []
    list_1 = []
    list_2 = []
    list = []
    list_child = []
    global found_in_loop
    iterable_list = node.children[:]
    if node.type == "if":
        if (len(node.children) == 2):
            for i in node.children:
                list_1 = inside_loop(i)
                if i == node.children[1]:
                    del found_in_loop[:]
                list_child = list_child + list_1
        else:
            right_list = inside_loop(node.children[2])
            del found_in_loop[:]
            list_1 = inside_loop(node.children[0])
            list_2 = inside_loop(node.children[1])
            del found_in_loop[:]
            left_list = list_1 + list_2
            for i in left_list:
                if i in right_list:
                    list_child.append(i)
                    
        return list_child
    elif node.type == "eq":
        lhs_var = node.children[0].leaf
        if lhs_var in list:
            pass
        else:
            list.append(lhs_var)
            found_in_loop.append(lhs_var)
        iterable_list = node.children[1:]
    elif node.type == "while":
        for i in node.children:
            list_1 = inside_loop(i)
            if i == node.children[1]:
                del found_in_loop[:]
            list_child = list_child + list_1
        return list_child
    elif node.type == "ID":
        var = node.leaf
        if not var in global_defined_var and not var in found_in_loop:
            print "Wellformed ERROR: Variable \"" + var + "\" not defined in every path"
            sys.exit(-1)
            return []
    for child in iterable_list:
        list_child = inside_loop(child)
        list = list + list_child
    return list

def wellformed(node):
    global global_defined_var
    list = []
    
    iterable_list = node.children[:]
    if(node.type == "if") or (node.type == "while"):
        list = inside_loop(node)
        if(node.type == "if"):
            global_defined_var = global_defined_var + list
        return
    elif node.type == "eq":
        lhs_var = node.children[0].leaf
        if lhs_var in global_defined_var:
            pass
        else:

            global_defined_var.append(lhs_var)

        iterable_list = node.children[1:]
    elif node.type == "ID":
        var = node.leaf
        if not var in global_defined_var:
            print "Wellformed ERROR :: Variable \"" + var + "\" not defined in every control flow path"
            sys.exit(-1)
        return
    for child in iterable_list:
        wellformed(child)
    
    return

if __name__ == "__main__":
    s = ''' int a, b, c, d[];
            d = new int [10];
            {if(3-4) then 
            {if(a==5)
            then a=5;}}
            {b= 2+-4;}
            for(a = 0; a < b; a++)
              b = c + 2;
            c= ++b + 2;
            {s=3;}
            print (c);'''
    result = parser.parse(s)
    astRoot = yacc.parse(s)
    print 'Done with parsing'
    wellformed(result)
