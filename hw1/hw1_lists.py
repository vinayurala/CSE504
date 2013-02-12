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
def ssa(stmts):
    scratch_dict = dict()
    ssa_stmts = []
    temp_list = []
    rhs_list = []
    new_def = 0
    for innerList in stmts:
        del temp_list[:]
        for var in innerList:
            if(not isinstance(var, list)):
                if (var in scratch_dict):
                    lhs_var = var + str(scratch_dict[var])
                    new_def = 1
                    new_def_var = var
                else:
                    scratch_dict[var] = 1
                    lhs_var = var

            else:
                del rhs_list[:]
                for rhs in var:
                    new_rhs = rhs
                    if (rhs in scratch_dict):
                        temp = scratch_dict[rhs] - 1
                        if (temp > 0):
                            new_rhs = rhs + str(temp)
                    
                    rhs_list.append(new_rhs)

        if(new_def):
            scratch_dict[new_def_var] = scratch_dict[new_def_var] + 1
            new_def = 0

        temp_list.append(lhs_var)
        temp_list.append(rhs_list[:])
    
        ssa_stmts.append(temp_list[:])
                    
    return ssa_stmts

#a = [1, 3, 5, 2, 4]
#a = [1, 2, 3, 5, 2, 4]
a = []
res = dup(a) 
print res
#stmts = [ ["x", []], ["y", ["x"]], ["z", ["x", "y"]], ["x", ["z", "y"]] ]
stmts = [ ["x", []], ["y", ["y", "x"]], ["z", ["x", "w"]], ["x", ["x", "z"]] ]
unused_vars = def_use(stmts)
print "Unused variables = " + str(unused_vars)

stmts = [ ["x", []], ["y", ["x"]], ["x", ["x", "y"]], ["z", ["x", "y"]], ["y", ["z", "x"]] ]
#stmts = [ ["x", []], ["y", ["x"]], ["x", ["x", "y"]], ["x", ["y", "x"]], ["y", ["y", "x"]] ]
ssa_stmts = ssa(stmts)
print ssa_stmts
