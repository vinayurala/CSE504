import cStringIO, tokenize
import sys
import re
import itertools

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
defined_var = []
expr_stacks = []
inSets = []
outSets = []
intGraph = dict()
binop = ["+", "-", "*", "/", "%"]
unop = ["-"]
token_map = {0: "ENDMARKER", 1:"NAME", 2:"NUMBER", 3:"STRING", 4:"NEWLINE", 5:"INDENT", 6:"DEDENT", 51:"OP"}
op_map = {"+":"PLUS", "-":"MINUS", "*":"MULT", "/":"DIV", "%":"MOD", ";":"SEMI", "(": "LPAR", ")":"RPAR", "=": "ASSIGN"}
rev_op_map = {"PLUS": "+", "MINUS": "-", "MULT": "*", "DIV": "/", "MOD":"%", "SEMI": ";", "LPAR": "(", "RPAR": ")", "ASSIGN": "="}
in_code_op_map = {"+": "add", "-": "sub", "*": "mul", "/": "div", "%": "mod", "=": ":="}

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
EOF             = "EOF"
NEWLINE         = "NEWLINE"
INPUT           = "INPUT"
PRINT           = "PRINT"
ZERO            = Token(None, "0", None)
PLACEHOLDER     = Token(None, "PLACEHOLDER", None)
uMinusToken     = Token(None, "UMINUS", None)

class Node:
    def __init__(self, token = None):
        self.token = token
        self.level = 0
        self.children = []

    def add(self, token):
        self.addNode(Node(token))

    def addNode(self, node):
        node.level = self.level + 1
        self.children.append(node)

    def wellFormed(self):
        global newly_defined_var
        iterable_list = self.children[:]

        if (self.token == None):
            pass
        elif (self.token.value == "PLACEHOLDER"):
            pass
        else:
            if self.token.type == EQUAL:
                lhs_var = self.children[0].token.value
                if lhs_var in defined_var:
                    pass
                else:
                    defined_var.append(lhs_var)
                newly_defined_var = lhs_var
                iterable_list = self.children[1:]
            elif self.token.type == NAME:
                if not self.token.value in defined_var or self.token.value == newly_defined_var:
                    print "Variable \"" + self.token.value + "\" used before its definition"
                    sys.exit(-1)
            elif self.token.type == SEMI:
                newly_defined_var = None
        
        for child in iterable_list:
            child.wellFormed()
                    
        return                    

     
    def __parseAST__(self):
        if self.token == None or self.token.value == "PLACEHOLDER":
            pass
        else:
            expr_stacks.append(self.token.value)

        for child in reversed(self.children):
            child.__parseAST__()
        return 

    def __getPostfix__(self, expr_stack):
        postfix_exprs = []
        temp_stack = []
        for t in expr_stack:
            if t == "(" or t == ")":
                pass
            elif t == ";":
                if "print" in temp_stack:
                    temp_stack.insert(len(temp_stack) - 1, temp_stack.pop(0))
                    postfix_exprs.append(temp_stack[:])
                    del temp_stack[:]
                else:
                    pass
            elif t == "=":
                temp_stack.append(t)
                postfix_exprs.append(temp_stack[:])
                del temp_stack[:]
            else:
                temp_stack.append(t)
                
        return postfix_exprs


    def gencode(self):
        self.__parseAST__()
        postfix_exprs = self.__getPostfix__(reversed(expr_stacks))
        temp_stack = []
        ic_lines = []
        line = str()
        
        tvar = "t"
        idx = 0

        for expr in postfix_exprs:
            del temp_stack[:]
            atom_expr = []

            for t in expr:
                line = str()                
                if not t in ["+", "-", "*", "/", "%", "=", "UMINUS", "print"]:
                    temp_stack.append(t)
                else:
                    if t == "=":
                        t1 = temp_stack.pop()
                        t2 = temp_stack.pop()
                        line += t2 + " " + t + " " + str(t1)
                            
                    elif t == "UMINUS":
                        t1 = temp_stack.pop()
                        line += tvar
                        idx += 1
                        line += str(idx) + " = " + " 0 - " + t1
                        temp_stack.append(tvar + str(idx))

                    elif t == "print":
                        t1 = temp_stack.pop()
                        line += t + " " + str(t1)

                    else:
                        t1 = temp_stack.pop()
                        t2 = temp_stack.pop()
                        line += tvar 
                        idx += 1
                        line += str(idx) + " = " + str(t2) + " " +  t + " " + str(t1)
                        temp_stack.append(tvar + str(idx))

                    atom_expr.append(line)
                    
            ic_lines.extend(atom_expr[:])
                    
        return ic_lines

def livenessAnalysis(icLines):
    useSet = set()
    defSet = set()
    inSet = set()
    outSet = set()
    rhsVars = []
    tList = []

    for line in icLines:
        if not inSet:
            pass
        else:
            outSet = inSet
        useSet = set()
        inSet = set()
        defSet = set()
        if not "print" in line:
            (lhs, rhs) = line.split('=', 2)
            lhs = lhs.replace(" ", "")
            defSet.add(lhs)
            rhsVars = rhs.split()
            for var in rhsVars:
                if not var in ["+", "-", "*", "/", "%"] and not var.isdigit() and var != "input":
                    var = var.replace(" ", "")
                    useSet.add(var)
        else:
            tList = tokenize.generate_tokens(cStringIO.StringIO(line).readline)
            for t in tList:
                if t[0] == 1 and t[1] != "print":
                    useSet.add(t[1])
        
        inSet = useSet.union(outSet.difference(defSet))
        inSets.append(inSet)
        outSets.append(outSet)  
        
def buildInterferenceGraph():
    varSet = set()
    for inSet in inSets:
        for var in inSet:
            if var:
                varSet.add(var)
    for outSet in outSets:
        for var in inSet:
            if var:
                varSet.add(var)
        
    intGraph = dict.fromkeys(list(varSet))
    varList = list(varSet)
    for i1, i2 in itertools.combinations(varList, 2):
        tSet = set((i1, i2))
        for set1 in inSets:
            if (tSet.issubset(set1)):
                if intGraph[i1] is None:
                    intGraph[i1] = set()
                intGraph[i1].add(i2)
                if intGraph[i2] is None:
                    intGraph[i2] = set()
                intGraph[i2].add(i1)
                    
    intGraph = dict((k, v) for k, v in intGraph.iteritems() 
                    if v != None)
                    
def getToken():
    global token_idx, token
    token_idx += 1
    try:
        token = token_list[token_idx]
    except IndexError:
        token.type = "EOF"

def found(tokType):
    if(token.type == tokType):
        prev_token = token
        return True
    return False

def consume(tok_type):
    if token.type == tok_type:
        getToken()
        return
    else:
        print "Expected %s not found" % rev_op_map[tok_type] + " in line: " + str(token.line_num)
        sys.exit(-1)

def parse():
    getToken()
    pgm()
    print "Program parsed successfully"

    return ast

def pgm():
    global ast
    node = Node()
    
    stmt(node)
    while not found(EOF):
        stmt(node)

    consume(EOF)

    ast = node

def stmt(node):

    if(found(PRINT)):
        node.add(token)
        consume(PRINT)
        printStmt(node)
    else:
        assignStmt(node)


def printStmt(node):
    stmtNode = Node(token)
    consume(LPAR)
    node.addNode(stmtNode)
    ae(stmtNode)
    rparNode = Node(token)
    node.addNode(rparNode)
    consume(RPAR)
    node.add(token)
    consume(SEMI)

def assignStmt(node):
    varNode = Node(token)
    if(found(NAME)):
        consume(NAME)
        opNode = Node(token)
        consume(EQUAL)
        node.addNode(opNode)
        opNode.addNode(varNode)
        rhs(opNode)
        opNode.add(token)
        consume(SEMI)
    else:
        print "Unexpected symbol: \"" + str(token.value) + "\" in line: " + str(token.line_num) + ". Expecting a variable on LHS" 
        sys.exit(-1)

def rhs(node):
    if(found(INPUT)):
        node.add(token)
        consume(INPUT)
        node.add(token)        
        consume(LPAR)
        node.add(token)
        consume(RPAR)
    else:
        ae(node)

def ae(node):
    term(node)
    if(found(PLUS)):
        opNode = Node(token)
        node.addNode(opNode)
        consume(PLUS)
        ae(opNode)
    elif found(MINUS):
        opNode = Node(token)
        node.addNode(opNode)
        consume(MINUS)
        ae(opNode)

def term(node):
    factor(node)
    if found(MULT):
        opNode = Node(token)
        node.addNode(opNode)
        consume(MULT)
        term(opNode)
    elif found(DIV):
        opNode = Node(token)
        node.addNode(opNode)
        consume(DIV)
        term(opNode)
    elif found(MOD):
        opNode = Node(token)
        node.addNode(opNode)
        consume(MOD)
        term(opNode)

def factor(node):
    factorNode = Node(PLACEHOLDER)
    node.addNode(factorNode)
    if(found(MINUS)):
        unSubNode = Node(uMinusToken)
        factorNode.addNode(unSubNode)
        consume(MINUS)
        factor(unSubNode)
    elif(found(NUMBER)):
        factorNode.add(token)
        consume(NUMBER)
    elif(found(NAME)):
        factorNode.add(token)
        consume(NAME)
    elif (found(LPAR)):
        lparNode = Node(token)
        node.addNode(lparNode)
        consume(LPAR)
        ae(lparNode)
        rparNode = Node(token)
        node.addNode(rparNode)
        consume(RPAR)
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
    try:
        for t in tokens:
            if (t[0] == 4):
                line_num += 1
                continue
            elif (t[0] == 0):
                continue
            if(t[0] == 51):
                if(not t[1] in op_map):
                    print "Unexpected symbol \'" + str(t[1]) + "\' in line: " + str(line_num)
                    sys.exit(-1)
                token_list.append(Token(op_map[t[1]], str(t[1]), line_num))
            else:
                token_list.append(Token(token_map[t[0]], str(t[1]), line_num))
    except:
        print "Error while tokenizing the program. Possibly because of a missing open/close paranthesis in line: " + str(line_num - 1)
        sys.exit(-1)

ast = parse()
ast.wellFormed()
print "AST well formed"
print "Intermediate code: "
ic_lines = ast.gencode()
for line in ic_lines:
    print line

livenessAnalysis(reversed(ic_lines))
inSets = inSets[::-1]
outSets = outSets[::-1]
buildInterferenceGraph()    
