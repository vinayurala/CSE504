# Yacc example
#import pydot

import ply.yacc as yacc

import sys

# Get the token map from the lexer.  This is required.
from lexer import tokens

precedence = (('left', 'OR'),
              ('left', 'AND'),
              ('nonassoc', 'EQUALS', 'NOTEQ', 'LTEQ','LT', 'GT','GTEQ'),
              ('left', 'PLUS', 'MINUS'),
              ('left', 'TIMES', 'DIVIDE', 'MOD'),
              ('right', 'NOT'),
              ('right', 'UMINUS'),
              )


#binop_list = ["+","-","*","/","%","||","&&","==","!=","<","<=",">",">="]
#unop_list = ["-","!"]


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
    'Pgm : Stmtseq '
    p[0] = p[1]


def p_stmtseq_stmt(p):
    'Stmtseq : Stmt'
    p[0] = p[1]

def p_stmtseq_stmt_stmtseq(p):
    'Stmtseq : Stmt Stmtseq'
    p[0] = Node("stmtseq",children = [p[1],p[2]])


def p_stmt_assign(p):
    '''Stmt : Assign
            | Print
            | If
            | While
            | Block''' 
    p[0] = p[1]

def p_assign_rhs(p):
    ' Assign : ID EQ Rhs SCOLON'
    p[1] = Node("ID",leaf = p[1])
    p[4] = Node("SEMI", leaf = p[4])
    p[0] = Node("eq",[p[1],p[3], p[4]],p[2])

def p_assign_rhs_error(p):                        #ERROR
    ' Assign : ID EQ Rhs'
    print "Syntax error :: Semicolon Missing in Line number %d"% (p.lineno(1))
    sys.exit()

def p_no_rhs_error(p):                            #ERROR
    'Assign : ID EQ SCOLON'
    print "Expected an expression or number after \"=\" in line: " + str(p.lineno(1))
    sys.exit(-1)

def p_missing_eq_error(p):                        #ERROR
    'Assign : ID Rhs SCOLON'
    print "\"=\" missing in assignment statement in line: " + str(p.lineno(1))

def p_print_ae(p):
    ' Print : PRINT LPAREN AE RPAREN SCOLON'  # Only one child for print
    p[5] = Node("SEMI", leaf = p[5])
    p[0] = Node("print",[p[3], p[5]],p[1])


def p_print_ae_error(p):                          #ERROR
    ' Print : PRINT LPAREN AE RPAREN '
    print "Syntax error :: Semicolon Missing in Line number %d"% (p.lineno(1))
    sys.exit()

def p_lparen_error(p):                            #ERROR
    'Print : PRINT AE RPAREN SCOLON'
    print "Synatx error: Missing \"(\" in line: " + str(p.lineno(1))
    sys.exit(-1)
    
def p_rparen_error(p):                            #ERROR
    'Print : PRINT LPAREN AE SCOLON'
    print "Synatx error: Missing \")\" in line: " + str(p.lineno(1))
    sys.exit(-1)

def p_block_stmtseq(p):
    'Block : LCURLY Stmtseq RCURLY'
    p[1] = Node("LCURLY",leaf = p[1])
    p[3] = Node("RCURLY",leaf = p[3])
    p[0] = Node("block",children = [p[1],p[2],p[3]])

def p_if(p):
    '''If : IF AE THEN Stmt
           | IF AE THEN Stmt ELSE Stmt'''
    if len(p) == 5:
        p[0] = Node("if",[p[2],p[4]],p[1])
    else:
        p[0] = Node("if",[p[2],p[4],p[6]],p[1])

def p_if_error(p):                               #ERROR
    'If : IF AE Stmt'
    print "Missing keyword \"then\" in line: " + str(p.lineno(1))
    sys.exit(-1)

def p_while(p):
    'While : WHILE AE DO Stmt'
    p[0] = Node("while",[p[2],p[4]],p[1])

def p_while_error(p):                            #ERROR
    'While : WHILE AE Stmt'
    print "Missing keyword \"do\" in line: " + str(p.lineno(1))
    sys.exit(-1)

def p_rhs(p):
    '''Rhs : AE
           | INPUT LPAREN RPAREN'''
    if len(p)>2:
        p[0] = Node("input",leaf = p[1])
    else:
        p[0] = p[1]

def rhs_ip_lparen_error(p):                      #ERROR
    'Rhs : INPUT RPAREN'
    print "Missing \"(\" after keyword \"input\" in line: " + str(p.lineno(1))
    sys.exit(-1) 

def rhs_ip_rparen_error(p):                      #ERROR
    'Rhs : INPUT LPAREN'
    print "Missing \")\" after keyword \"input\" in line: " + str(p.lineno(1))
    sys.exit(-1)


def p_ae_binaryop(p):
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
          | AE LTEQ AE
          | AE GT AE
          | AE GTEQ AE'''
    p[0] = Node("binop",[p[1],p[3]],p[2])


def p_ae_binop_error(p):                        #ERROR
    'AE : AE AE '
    print "Expecting an operator in line: " + str(p.lineno(1))
    sys.exit(-1)

def p_ae_uminus(p):
    'AE : MINUS AE %prec UMINUS'
    p[0] = Node("unop",[p[2]],"UMINUS")


def p_ae_unop(p):
    ' AE : NOT AE'
    p[0] = Node("unop",[p[2]],"NOT")

def p_ae_parentheses(p):
    ' AE : LPAREN AE RPAREN'
    p[0] = p[2]

def p_ae_lparen_error(p):
    ' AE : AE RPAREN'
    print "Syntax error: Missing \"(\" in line: " + str(p.lineno(1))
    sys.exit(-1)

def p_ae_rparen_error(p):
    ' AE : LPAREN AE'
    print "Syntax error: Missing \")\" in line: " + str(p.lineno(1))
    sys.exit(-1)


def p_ae_intconst(p):
    ' AE : NUMBER'
    p[0] = Node("NUMBER",leaf = p[1])

def p_ae_id(p):
    ' AE : ID'
    p[0] = Node("ID",leaf = p[1])


def p_error(p):
    if p==None:
       print "Syntax error found at 'End Of File' Probably because of missing right curly brace"
       sys.exit()
    else :
        print "Syntax error in line number %d just before token '%s' of value '%s' " % (p.lineno,p.type,p.value)
	sys.exit()

parser = yacc.yacc()

global_defined_var = list()
found_in_loop = list()

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
    s = ''' {if(3-4) then 
            {if(a==5)
            then a=5;}}
            {b= 2+-4;}
            c= b+2;
            {s=3;}
            print (c);'''
    result = parser.parse(s)
    wellformed(result)
