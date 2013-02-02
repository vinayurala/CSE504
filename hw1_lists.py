def dup(a):
    a.sort()
    for i1, i2 in zip(a, a[1:]):
        if (i1 == i2):
            return True
    return False

def def_use(stmts):
    defined_vars = []
    unused_vars = []
    for inner_l in stmts:
        for vars in inner_l:
            if((not isinstance(vars, list))):
                lhs_var = vars
            elif((isinstance(vars, list)) and vars):
                for rhs_vars in vars:
                    if(not rhs_vars in defined_vars):
                            unused_vars.append(rhs_vars)
        defined_vars.append(lhs_var)

    return unused_vars
    
#a = [1, 3, 5, 2, 4]
a = [1, 2, 3, 5, 2, 4]
#stmts = [ ["x", []], ["y", ["x"]], ["z", ["x", "y"]], ["x", ["z", "y"]] ]
stmts = [ ["x", []], ["y", ["y", "x"]], ["z", ["x", "w"]], ["x", ["x", "z"]] ]
res = dup(a)
print res
unused_vars = def_use(stmts)
print "Unused variables = " + str(unused_vars)

