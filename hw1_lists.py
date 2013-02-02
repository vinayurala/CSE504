# Part A, exercise 1
def dup(a):
    a.sort()
    for i1, i2 in zip(a, a[1:]):
        if (i1 == i2):
            return True
    return False

# Part A, exercise 2
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

# Part A, exercise 3
# Assumptions:
#  1) All variables are defined
#  2) Variable names do not end with numbers (confirm with Prof if this is alright)
def ssa(stmts):
    ssa_stmts = []
    defined_vars = []
    for inner_l in stmts:
        for var in inner_l:
            if((not isinstance(var, list))):
                if(not var in defined_vars):
                    defined_vars.append(var)
                else:
                   suffix_num = var[-1:]
                   if(not suffix_num.isdigit()):
                       suffix_num = 1
                   else:
                       suffix_num += 1
                   var += str(suffix_num)
            ssa_stmts.append(var)

    return ssa_stmts     

#a = [1, 3, 5, 2, 4]
a = [1, 2, 3, 5, 2, 4]
#stmts = [ ["x", []], ["y", ["x"]], ["z", ["x", "y"]], ["x", ["z", "y"]] ]
#stmts = [ ["x", []], ["y", ["y", "x"]], ["z", ["x", "w"]], ["x", ["x", "z"]] ]
stmts = [ ["x", []], ["y", ["x"]], ["x", ["x", "y"]], ["z", ["x", "y"]], ["y", ["z", "x"]] ]
res = dup(a) 
print res
unused_vars = def_use(stmts)
print "Unused variables = " + str(unused_vars)
ssa_stmts = ssa(stmts)
print ssa_stmts
