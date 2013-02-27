Compiler for Proto (HW2)
================================================================
				Vinay Krishnamurthy (108800980)
			  	Siddharth Chaudhary (108797835)
================================================================
Usage: 
python protoplasm.py <Protofilename>.

The output will be written to a file with the same name as
Proto file, but with a '.asm' extension.
=================================================================
Assumptions:

i) As stated in the HW page, divison by zero/overflow
   is not handled in MIPS code and are ignored.
ii) If a there is a new-line between the expression and
    semi-colon, it would still be accepted. However a 
    blank semi-colon will fail.

==================================================================
Classes and Functions:

a) Classes:
   There are only 2 classes defined: one to store token
   related data (Token), and the other for AST(Node). 
   Class 'Token' has the following members: Value, Type 
   and Line number. Class 'Node' has the following 
   members: Level, List of child nodes, and Level of the 
   node. Functionality of member functions of class 'Node' 
   is given below:
   i) 'add': Adds a node to the tree with 'Token' object as
      a parameter. It basically calls 'addNode' function.
   ii) 'addNode': Adds a node to the tree at a level below
        the current node, and adds the node to the list of
    	child nodes of the current node.
   iii) 'wellFormed': Similar to 'defuse' function in HW1.
   	 Checks if all variables have been defined before
     	 being used.
   iv) '__parseAST__': Parses thru the AST bottom to get a 
        list of expression on one stack.
    v) '__getPostfix__': Works on the stack returned by
       '__parseAST__' to return all expressions present in	
       the AST in postfix form.
   vi) 'gencode': Generates the Intermediate code based on
       the postfix expressions returned by __getPostfix__
       and returns a list of strings (each string is a line
       in the Intermediate code).

b) Functions:
   There are number of functions defined for parsing. Our 
   parser is predictive Recursive descent parser, and does
   not backtrack.

   There are other functions to perform the Liveness Analysis,
   building an Interference Graph, and register allocation based
   on Graph Coloring. We've added support to store spilled 
   variables in memory, but there is no support for start over 
   yet.
======================================================================
Datastructures:

There are a lot of dictionaries defined, such as 'token_map' which
maps the token type returned by tokenize.generate_tokens to actual
tokens, 'op_map' to map the operators, and also for MIPS code 
equivalent for mathematical operators supported in Proto. There is
another dictionary which stores the template of MIPS code, such as
code to print a new line, or to print a value contained in a register

Additonally, a map of variables to its allocated registers is also
maintained, called 'coloredList'. There is a list to hold the spilled
variables.
=======================================================================
Git related info:

The code is on branch hw2 annotated with tag 'hw2-handin'
=======================================================================