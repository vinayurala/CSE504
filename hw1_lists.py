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
    temp_list = []
    for inner_l in stmts:
        for var in inner_l:
            if((not isinstance(var, list))):
                del temp_list[:]
                if(not var in defined_vars):
                    defined_vars.append(var)
                else:
                   for t_item in defined_vars:
                       if t_item.startswith(var):
                           temp_list.append(t_item)
                   
                   # var = temp_list[-1:]
                   tmp_var = temp_list[-1:].pop()
                   suffix_num = tmp_var[-1:]
                   print suffix_num
                   if(not suffix_num.isdigit()):
                       suffix_num = 1
                       tmp_var += `suffix_num`
                   else:
                       suffix_num = int(suffix_num)
                       suffix_num += 1
                       tmp_var = tmp_var.replace(tmp_var[len(tmp_var) - 1], str(suffix_num))
                   var = tmp_var
                   defined_vars.append(var)
                   # TODO: Append is not what we're looking for, I'm not able to embed the rhsvars list properly;
            ssa_stmts.append(var)

    return ssa_stmts     

#a = [1, 3, 5, 2, 4]
a = [1, 2, 3, 5, 2, 4]
#stmts = [ ["x", []], ["y", ["x"]], ["z", ["x", "y"]], ["x", ["z", "y"]] ]
#stmts = [ ["x", []], ["y", ["y", "x"]], ["z", ["x", "w"]], ["x", ["x", "z"]] ]
stmts = [ ["x", []], ["y", ["x"]], ["x", ["x", "y"]], ["z", ["x", "y"]], ["y", ["z", "x"]] ]
#stmts = [ ["x", []], ["y", ["x"]], ["x", ["x", "y"]], ["x", ["y", "x"]], ["y", ["y", "x"]] ]
res = dup(a) 
print res
unused_vars = def_use(stmts)
print "Unused variables = " + str(unused_vars)
ssa_stmts = ssa(stmts)
print ssa_stmts
