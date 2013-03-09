# Yacc example
import pydot

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
    p[0] = Node("eq",[p[1],p[3]],p[2])

def p_print_ae(p):
    ' Print : PRINT LPAREN AE RPAREN SCOLON'  # Only one child for print
    p[0] = Node("print",[p[3]],p[1])

def p_block_stmtseq(p):
    'Block : LCURLY Stmtseq RCURLY'
    p[1] = Node("LCURLY",leaf = p[1])
    p[3] = Node("RCURLY",leaf = p[3])
    p[0] = Node("block",children = [p[1],p[2],p[3]])

def p_if(p):
    'If : IF AE THEN Stmt'                                          # No Else
    p[0] = Node("if",[p[2],p[4]],p[1])
        # else:
#p[0] = Node("if",[p[2],p[4],p[6]],p[1])

def p_while(p):
    'While : WHILE AE DO Stmt'
    p[0] = Node("while",[p[2],p[4]],p[1])

def p_rhs(p):
    '''Rhs : AE
           | INPUT LPAREN RPAREN'''
    if len(p)>2:
        p[0] = Node("input",leaf = p[1])
    else:
        p[0] = p[1]

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

def p_ae_uminus(p):
    'AE : MINUS AE %prec UMINUS'
    p[0] = Node("unop",[p[2]],"-")


def p_ae_unop(p):
    ' AE : NOT AE'
    p[0] = Node("unop",[p[2]],"!")

def p_ae_parentheses(p):
    ' AE : LPAREN AE RPAREN'
    p[0] = p[2]

def p_ae_intconst(p):
    ' AE : NUMBER'
    p[0] = Node("NUMBER",leaf = p[1])

def p_ae_id(p):
    ' AE : ID'
    p[0] = Node("ID",leaf = p[1])


def p_error(p):
	print "Syntax error in line number XXX (need to figure this out)"
	sys.exit()

parser = yacc.yacc()

s = ''' {if(3-4) then 
            {if(a==5)
            then a=5;}}
{b= 2+-4;}
c= b+2;
{s=3;}
print (c);'''

result = parser.parse(s)
graph(result)


global_defined_var = []
found_in_loop = []
inside = 0


def wellformed(node):
    global found_in_loop
    global inside
    global global_defined_var
    iterable_list = node.children[:]
    if node.type == "eq":
        if inside == 0:
            lhs_var = node.children[0].leaf
            if lhs_var in global_defined_var:
                pass
            else:
                global_defined_var.append(lhs_var)
        else:
            lhs_var = node.children[0].leaf
            if lhs_var in global_defined_var:
                pass
            else:
                found_in_loop.append(lhs_var)
        iterable_list = node.children[1:]
    elif(node.type == "if") or (node.type == "while"):
            inside = 1
            node1 = node.children[1]
            wellformed(node1)
            inside = 0
            for var in found_in_loop:
                if var in global_defined_var:
                    found_in_loop.remove(var)
#return
    elif node.type == "ID":
        var = node.leaf
        print var
        print "global" ,global_defined_var[:]
        print "loop",found_in_loop[:]
        if not var in global_defined_var:
            if not var in found_in_loop:
                print "ERROR: Variable \"" + var + "\" used before its definition"
                sys.exit(-1)
            else:
                print "ERROR: Variable \"" + var + "\" not defined in every path"
                sys.exit(-1)
    for child in iterable_list:
        wellformed(child)
    
    return


wellformed(result)

