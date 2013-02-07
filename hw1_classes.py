class PBF:
    # pass

    def isNNF(self):
        postfix_str = self.__str__()
        for idx in range(len(postfix_str)):
            if(postfix_str[idx] == '!'):
                if(postfix_str[idx - 2] == '&' or postfix_str[idx - 2] == '|'):
                    return False
        
        return True

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


#PBFObj = AND(PROP("x"), NOT(OR(PROP("y"), PROP("z"))))
PBFObj = AND(PROP("x"), OR(NOT(PROP("y")), NOT(PROP("z"))))
print PBFObj
res = PBFObj.isNNF()
if(res == True):
    print "Given PBF is in NNF"
else:
    print "Given PBF is not in NNF"

