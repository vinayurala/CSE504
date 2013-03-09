# Yacc example

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


binop_list = ["+","-","*","/","%","||","&&","==","!=","<","<=",">",">="]
unop_list = ["-","!"]


class Node:
    def __init__(self,type,children=None,leaf=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = [ ]
        self.leaf = leaf

def p_pgm_stmtseq(p):
    'Pgm : Stmtseq '
    p[0] = p[1]


def p_stmtseq_stmt(p):
    'Stmtseq : Stmt'
	p[0] = p[1]

def p_stmtseq_stmt_stmtseq(p):
        'Stmtseq : Stmt Stmtseq'
        p[0] = Node("stmtseq",[p[1],p[2]],None)


def p_stmt_assign(p):
    'stmt : Assign | Print | If | While | Block'
    p[0] = p[1]

def p_assign_rhs(p):
    ' Assign : ID EQ Rhs SCOLON'
    p[0] = Node("eq",[p[1],p[3]],p[2])

def p_print_ae(p):
    ' Print : PRINT LPAREN AE RPAREN SCOLON'
    p[0] = p[3]

def p_block_stmtseq(p):
    if len(p) == 3:
        p[0] = p[2]


def p_if(p):
    if len(p) == 5:
        p[0] = Node("if",[p[2],p[4]],p[1])
    else:
        p[0] = Node("if",[p[2],p[4],p[6]],p[1])

def p_while(p):
    p[0] = Node("while",[p[2],p[4]],p[1])

def p_rhs(p):
    if p.len()>2:
        p[0] = Node("input",None,p[1])
    else:
        p[0] = p[1]



def p_ae_binaryop(p):
    if p[2] in binop_list:
        p[0] = Node("binop",[p[1],p[3]],p[2])

def p_ae_unaryop(p):
    if len(p) == 3:
        if p[1] == "!":##
            pass#p[0] = !p[2]
        else:
            p[0] = -p[2]

def p_ae_parentheses(p):
    if p[1] == "(" and p[3] == ")":
        p[0] = p[2]

def p_ae_intconst(p):
    p[0] = Node("NUMBER",None,p[1])

def p_ae_id(p):
    p[0] = Node("ID",None,p[1])

def p_error(p):
	print "Syntax error in line number %d" % t.lineno
	sys.exit()

parser = yacc.yacc()

while True:
    try:
        s = raw_input('calc > ')
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    


    
