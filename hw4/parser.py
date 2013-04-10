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
    p[0] = Node("StmtSeq",children = [p[1],p[2]])

def p_stmtseq_null(p):
    'StmtSeq : '
    p[0] = Node("StmtSeq")

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
            p[0] = Node("if", [p[2], p[4]], p[1])
        else:
            p[0] = Node("while", [p[2], p[4]], p[1])
    elif len(p) == 6:
        p[5] = Node("SEMI", leaf = p[5])
        if p[1] == "do":
            p[0] = Node("do", [p[2], p[4], p[5]], p[1])
        else:
            p[0] = Node("print", [p[3],p[5]], p[1])
    elif len(p) == 7:
        p[0] = Node("if", [p[2], p[4], p[6]], p[1])
    elif len(p) == 10:
        p[4] = Node("SEMI", leaf = p[4])
        p[6] = Node("SEMI", leaf = p[6])
        p[0] = Node("for", [p[3], p[4], p[5], p[6], p[7], p[9]], p[1])


def p_stmt_curly(p):
    'Stmt : LCURLY DeclSeq StmtSeq RCURLY'
    p[1] = Node("LCURLY", leaf = p[1])
    p[4] = Node("RCURLY", leaf = p[4])
    p[0] = Node("Stmt", children = [p[1], p[2], p[3], p[4]])

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

def p_declseq(p):
    'DeclSeq : Decl DeclSeq'
    p[0] = Node("DeclSeq", children = [p[1], p[2]])

def p_declseq_null(p):
    'DeclSeq : '
    p[0] = Node("DeclSeq")

def p_decl(p):
    'Decl : Type VarList SCOLON'
    p[3] = Node("SEMI", leaf = p[3])
    p[0] = Node("Decl", children = [p[1], p[2], p[3]])

def p_type(p):
    '''Type : INT
        | BOOL'''
    p[0] = Node("Type", leaf = p[1])

def p_varlist(p):
    '''VarList : Var COMMA VarList
        VarList : Var'''
    if len(p) == 2:
        p[0] = Node("VarList", children = [p[1]])
    elif len(p) == 4:
        p[2] = Node("COMMA", leaf = p[2])
        p[0] = Node("VarList", children = [p[1], p[2], p[3]])

def p_var(p):
    'Var : ID DimStar'
    p[1] = Node("ID", leaf = p[1])
    p[0] = Node("Var", children = [p[1], p[2]])

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
    '''Lhs : ID
        | Lhs LSQR AE RSQR'''
    if len(p) == 2:
        p[0] = Node("ID", leaf = p[1])
    elif len(p) == 5:
        p[2] = Node("LSQR", leaf = p[2])
        p[4] = Node("RSQR", leaf = p[4])
        p[0] = Node("Lhs", children = [p[1], p[2], p[3], p[4]])

def p_dimexpr(p):
    'DimExpr : LSQR AE RSQR'
    p[1] = Node("LSQR", leaf = p[1])
    p[3] = Node("RSQR", leaf = p[3])
    p[0] = Node("DimExpr", children = [p[1], p[2], p[3]])

def p_dimstar(p):
    '''DimStar : LSQR RSQR DimStar
        DimStar : '''
    if len(p) == 1:
        p[0] = Node("DimStar", children = [])
    elif len(p) == 4:
        p[1] = Node("LSQR", leaf = p[1])
        p[2] = Node("RSQR", leaf = p[2])
        p[0] = Node("DimStar", children = [p[1], p[2], p[3]])

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
    p[0] = Node("Unop", children = [p[2]], leaf = "NOT")

def p_ae_lhs(p):
    'AE : Lhs'
    p[0] = p[1]

def p_ae_se(p):
    'AE : SE'
    p[0] = p[1]

def p_ae_ip(p):
    'AE : INPUT LPAREN RPAREN'
    p[0] = Node("Input", leaf = p[1])

def p_ae_aeparan(p):
    'AE : LPAREN AE RPAREN'
    p[0] = Node("AE", children = [p[2]])

def p_ae_new_expr(p):
    'AE : NEW Type DimExpr DimStar'
    p[1] = Node("NEW", leaf = p[1])
    p[0] = Node("AE", children = [p[1], p[2], p[3], p[4]])

def p_ae_misc(p):
    '''AE : TRUE
        | FALSE
        | NUMBER '''
    p[0] = Node("IntConst", leaf = p[1])

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



def wellformed(node,decl,defined):
    #print node
    #print node.type
    iterable_list = node.children[:]
    
    
    if(node.type == "if") or (node.type == "while"):
        temp_decl = decl[:]
        temp_defined = defined[:]
        #print decl[:]
        for child in iterable_list:
            #print child
            wellformed(child,temp_decl,temp_defined)
        #print decl[:]
        return
    
    elif(node.type == "do"):
        print "here"
        temp_decl = decl[:]
        for child in iterable_list:
            # print decl[:]
            wellformed(child,temp_decl,defined)
        # print defined[:]
        #print decl[:]
            #print defined[:]
        return

    elif(node.type == "for"):
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
        if(node.children[0].type == "LCURLY"):
            temp_decl = decl[:]
            temp_defined = defined[:]
            #print decl[:]
            for child in iterable_list:
                wellformed(child,temp_decl,temp_defined)
            #print decl[:]
            return


    
    elif(node.type == "Var"):
        id1 = node.children[0].leaf
        decl.append(id1)
        #print id
        iterable_list = node.children[1:]
    
    elif node.type == "ID":
        id1 = node.leaf
        if not id1 in decl:
            print "Wellformed ERROR: Variable \"" + str(id1) + "\" NOT DECLARED before use"
            sys.exit(-1)
            return []
        elif not id1 in defined:
            print "Wellformed ERROR: Variable \"" + str(id1) + "\" NOT DEFINED before use"
            sys.exit(-1)
            return []
    
    elif node.type == "SEEq":
        #print "here"
        id1 = node.children[0].leaf
        if not id1 in decl:
            print "Wellformed ERROR: Variable \"" + str(id1) + "\" NOT DECLARED before use"
            sys.exit(-1)
            return []
        elif id1 in defined:
            pass
        else:
            defined.append(id)
#print id
        iterable_list = node.children[1:]
    
    
    for child in iterable_list:
        print child.type
        wellformed(child,decl,defined)
    
    return




if __name__ == "__main__":
    s = ''' int a,b;
            int d,x;
        int i;
        int a[];
            b = 4;
        
        a = new int[10];
            if(b==5)
            then
            {
                if(b==5)
                then
                {
                int c;
            i=0;
                c = a[i];
                c=3;
                b=6;}
            
            }
        
       
        for (a = 1; a < b; a++)
        {
            int x;
            b++;
            
            x=1;
            x++;
        
        }
        
        do {
        int e;
        d = 1;
        //a++;
        e=1;
        e++;
        //l = 3;
        
        } while(b > 3);
       //x++;
        
        
        //dfsdfs
       // d++;
            '''
    result = parser.parse(s)
    astRoot = yacc.parse(s)
    print 'Done with parsing'
    wellformed(result,decl,defined)
