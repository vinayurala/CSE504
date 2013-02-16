import ast

bin_op_map = {'Add': '+', 'Sub': '-', 'Mult': '*', 'Div': '/', 'Assign': '='}
un_op_map = {'USub': '-'}
precedence = {'+': 0, '-': 0, '*': 1, '/': 1}

class customParser(ast.NodeVisitor):
    
    def __init__(self):
        pass

    def generic_visit(self, node):
        node_type = type(node).__name__

        if(node_type in bin_op_map):
            print bin_op_map[node_type]

        elif (node_type in un_op_map):
            print un_op_map[node_type]

        else:
            """ Do nothing """

        ast.NodeVisitor.generic_visit(self, node)

    def visit_Load(self, node):
        pass

    def visit_Name(self, node):
        print node.id

    def visit_Num(self, node):
        print str(node.__dict__['n'])

"""
def well_formed(ast_obj, expr_ast):
    def_var = []
    use_var = []
    ast_obj.visit(expr_ast, def_var, use_var)
"""

pobj = customParser()
expr = str()
io = str()
with open('example1.proto') as f:
    lines = f.readlines()
for line in lines:
    if(not "input" in line and not "print" in line):
        expr += str(line)
    else:
        io += str(line)

expr_ast = ast.parse(expr)
print "Expressions: "
pobj.visit(expr_ast)
print "I/O statements: "
print io
