class PBF:
    # pass

    def isNNF(self):
        postfix_str = self.__str__()
        postfix_str = postfix_str.replace(' ', '')
        for idx in range(len(postfix_str)):
            if(postfix_str[idx] == '!'):
                if(not postfix_str[idx - 1].isalpha()):
                    return False
        
        return True

    def __apply_demorgans__(self, t1):
        t2 = str()
        for it in t1:
            if (it.isalpha()):
                t2 += it + ' !'
            elif(it == '|'):
                t2 += '&'
            elif(it == '&'):
                t2 += '|'       
            else:
                t2 += '!'
             
            t2 += ' '
        t2 = t2.replace("! !", "")

        return t2

    def toNNF(self):
        nnfObj = PBF()
        postfix_str = self.__str__()
        postfix_str = postfix_str.replace(' ', '')
        temp_stack = []
        for idx in range(len(postfix_str)):
            if(postfix_str[idx] == '!'):
                t1 = str(temp_stack.pop())
                t1 = t1.replace(' ' , '')
                if(len(t1) >= 3):
                    t2 = self.__apply_demorgans__(t1)
                    temp_stack.append(t2)
                    if(t1[1] == '&'):
                        nnfObj = AND(NOT(PROP(t1[0])), NOT(PROP(t1[2])))
                    else:
                        nnfObj = OR(NOT(PROP(t1[0])), NOT(PROP(t1[2])))
                    
                else:
                    if('!' in t1):
                        t1 = t1[0] + ' '
                        nnfObj = PROP(t1)
                        temp_stack.append(t1)
                    else:
                        t1 = t1 + " ! "
                        nnfObj = NOT(PROP(t1))
                        temp_stack.append(t1)
            elif(postfix_str[idx] == '&'):
                t1 = temp_stack.pop()
                t2 = temp_stack.pop()
                nnfObj = AND(PROP(t2), PROP(t1))
                t1 = t2 + ' ' + t1 + " &"
                temp_stack.append(t1)
            
            elif (postfix_str[idx] == '|'):
                t1 = temp_stack.pop()
                t2 = temp_stack.pop()
                nnfObj = OR(PROP(t2), PROP(t1))
                t1 = t2 + ' ' + t1 + " |"
                temp_stack.append(t1)

            else:
                temp_stack.append(postfix_str[idx])

        return nnfObj        

class OR(PBF):
    
    def __init__(self, f1, f2):
        self.lchild = f1
        self.rchild = f2

    def __str__(self):
        return str(self.lchild) + " " + str(self.rchild) + " |"

class AND(PBF):

    def __init__(self, f1, f2):
        self.lchild = f1
        self.rchild = f2

    def __str__(self):
        return str(self.lchild) + " " + str(self.rchild) + " &"

class NOT(PBF):

    def __init__(self, f):
        self.child = f

    def __str__(self):
        return str(self.child) + " !"

class PROP(PBF):

    def __init__(self, p):
        self.prop = p

    def __str__(self):
        return self.prop


def parse(postfix_str):
    PBFObj = PBF()
    temp_stack = []
    postfix_str = postfix_str.replace(' ', '')

    for it in range(len(postfix_str)):
        if (postfix_str[it].isalpha()):
            temp_stack.append(postfix_str[it])

        elif (postfix_str[it] == '!'):
            t1 = temp_stack.pop()
            PBFObj = NOT(PROP(t1))
            t1 = t1 + " " + '!'
            temp_stack.append(t1)

        elif (postfix_str[it] == '&'):
            t1 = temp_stack.pop()
            t2 = temp_stack.pop()
            PBFObj = AND(PROP(t2), PROP(t1))
            t1 = t2 + " " + t1 + " " + '&'
            temp_stack.append(t1)

        elif (postfix_str[it] == '|'):
            t1 = temp_stack.pop()
            t2 = temp_stack.pop()
            PBFObj = OR(PROP(t2), PROP(t1))
            t1 = t2 + " " + t1 + " " + '|'
            temp_stack.append(t1)

        else:
            print "Error - Unexpected character: " + postfix_str[it]
            return None

    del temp_stack[:]
    return PBFObj


#PBFObj = AND(PROP("x"), NOT(OR(PROP("y"), PROP("z"))))
#PBFObj = AND(PROP("x"), AND(NOT(PROP("y")), NOT(PROP("z"))))
#PBFObj = AND(PROP("w"), NOT(AND(NOT(OR(PROP("x"), PROP("y"))), PROP("z"))))
#PBFObj = AND(PROP("w"), OR(PROP("x"), OR(PROP("y"), NOT(PROP("z")))))
PBFObj = OR(NOT(NOT(PROP("x"))), NOT(AND(PROP("y"), PROP("z"))))
print "Defined PBF Object: "
print PBFObj
res = PBFObj.isNNF()

if(res == True):
    print "Given PBF is in NNF"
else:
    print "Given PBF is not in NNF"

if(PBFObj.isNNF()):
    print "NNF string = " + PBFObj.__str__()
else:
    nnfObj = PBFObj.toNNF()
    print "NNF string = " + nnfObj.__str__()

expr_str = "x y ! z ! | &"
print "String to parse function = " + expr_str
PBFObj = parse(expr_str)
if (not PBFObj is None):
    print "PBFObj from parse function: " + PBFObj.__str__()
