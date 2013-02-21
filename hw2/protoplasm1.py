import cStringIO, tokenize
import sys
import re

class Token:
    def __init__(self, tok_type, tok_val, line_num):
        self.value = tok_val
        self.line_num = line_num
        if(tok_val == "input"):
            self.type = "INPUT"
        elif (tok_val == "print"):
            self.type = "PRINT"
        else:
            self.type = tok_type

token = Token(None, None, None)
token_list = []
line_num = 1
asts = []
binop = ["+", "-", "*", "/", "%"]
unop = ["-"]
token_map = {0: "ENDMARKER", 1:"NAME", 2:"NUMBER", 3:"STRING", 4:"NEWLINE", 5:"INDENT", 6:"DEDENT", 51:"OP"}
op_map = {"+":"PLUS", "-":"MINUS", "*":"MULT", "/":"DIV", "%":"MOD", ";":"SEMI", "(": "LPAR", ")":"RPAR", "=": "ASSIGN"}
rev_op_map = {"PLUS": "+", "MINUS": "-", "MULT": "*", "DIV": "/", "MOD":"%", "SEMI": ";", "LPAR": "(", "RPAR": ")", "ASSIGN": "="}

NAME            = "NAME"
NUMBER          = "NUMBER"
PLUS            = "PLUS"
MINUS           = "MINUS"
MULT            = "MULT"
DIV             = "DIV"
MOD             = "MOD"
EQUAL           = "ASSIGN"
SEMI            = "SEMI"
LPAR            = "LPAR"
RPAR            = "RPAR"
ENDMARKER       = "ENDMARKER"
NEWLINE         = "NEWLINE"
INPUT           = "INPUT"
PRINT           = "PRINT"

class Node:
    def __init__(self, token = None):
        self.token = token
        self.level = 0
        self.children = []

    def addNode(self, token):
        node.level = self.level + 1
        self.children.append(node)

def getToken():
    global token_idx, token
    token_idx += 1
    try:
        token = token_list[token_idx]
    except IndexError:
        token.type = "ENDMARKER"

def found(tokType):
    if(token.type == tokType):
        getToken()
        return True
    return False

def expect(tok_type):
    if found(tok_type):
        return
    else:
        print "Expected %s not found" + rev_op_map[tok_type] + " in line: " + token.line_num
        sys.exit(-1)

def parse():
    getToken()
    pgm()
    print "Program parsed successfully"

def pgm():
    global ast

    stmt()
    while not found(ENDMARKER):
        stmt()

    expect(ENDMARKER)

def stmt(node = None):
    if(found(PRINT)):
        printStmt()
    else:
        assignStmt()

def printStmt(node = None):
    # stmtNode = Node(token)
    expect(LPAR)
    # node.addNode(stmtNode)
    ae()
    expect(RPAR)
    expect(SEMI)

def assignStmt(node = None):
    # varNode = Node(token)
    if(found(NAME)):
        # opNode = Node(token)
        expect(EQUAL)
        # node.addNode(opNode)
        # opNode.addNode(varNode)
        rhs()
        expect(SEMI)
    else:
        print "Unexpected symbol: " + str(token.type) + "in line: " + str(token.line_num) + ". Expecting either %s %s or an expression" % NAME  % NUMBER
        sys.exit(-1)

def rhs(node = None):
    if(found(INPUT)):
        expect(LPAR)
        expect(RPAR)
    else:
        ae()


def ae(node = None):
    term()
    if(found(PLUS) or found(MINUS)):
        ae()

def term(node = None):
    factor()
    if (found(MULT) or found(DIV) or found(MOD)):
        term()

def factor(node = None):
    if(found(MINUS)):
        factor()
    elif(found(NUMBER)):
        pass
    elif(found(NAME)):
        pass
    elif (found(LPAR)):
        ae()
        expect(RPAR)
    else:
        print "Unexpected symbol: \"" + rev_op_map[token.type] + "\" in line: " + str(token.line_num) + ". Expecting either a variable or number or an expression."
        sys.exit(-1)
    

def get_tokens(lines):
    token_list = []
    token_list = tokenize.generate_tokens(cStringIO.StringIO(lines).readline)

    return token_list        

with open('example1.proto') as f:
    token_idx = -1
    lines = f.readlines()
for line in lines:
    tokens = get_tokens(line)
    for t in tokens:
        if (t[0] == 4):
            line_num += 1
            continue
        elif (t[0] == 0):
            continue
        if(t[0] == 51):
            # print op_map[t[1]] + "\t" + str(t[1])
            if(not t[1] in op_map):
                print "Unexpected symbol \'" + str(t[1]) + "\' in line: " + str(line_num)
                sys.exit(-1)
            token_list.append(Token(op_map[t[1]], str(t[1]), line_num))
        else:
            # print token_map[t[0]] + "\t" + str(t[1])
            token_list.append(Token(token_map[t[0]], str(t[1]), line_num))

parse()
