import ply.lex as lex


reserved = {
    'if' : 'IF',
    'then' : 'THEN',
    'while' : 'WHILE',
    'else' : 'ELSE',
    'do' : 'DO',
    'input' : 'INPUT',
    'print' : 'PRINT',
}

# List of token names.   
tokens = [
          'NUMBER',
          'PLUS',
          'MINUS',
          'TIMES',
          'DIVIDE',
          'LPAREN',
          'RPAREN',
          'ID',
          'LCURLY',
          'RCURLY',
          'SCOLON',
          'MOD',
          'AND',
          'OR',
          'EQ',
          'EQUALS',
          'NOTEQ',
          'NOT',
          'GTEQ',
          'LTEQ',
          'GT',
          'LT',
          'COMMENT'
          
          ] + list(reserved.values())

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LCURLY  = r'\{'
t_RCURLY  = r'\}'
t_SCOLON  = r';'
t_MOD     = r'%'
t_AND     = r'&&'
t_OR      = r'\|\|'
t_EQUALS  = r'=='
t_EQ      = r'='

t_NOTEQ= r'!='

t_NOT     = r'!'
t_LT= r'<'
t_GT = r'>'
t_LTEQ = r'<='
t_GTEQ = r'>='


# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# for comments
def t_COMMENT(t):
    r'\/\/.*'
    pass

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print "Illegal character '%s' " % (t.value[0])             #Should we exit here?
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

#input ='''a = input();
#b = a || !2;
#c = a + b;
#d = 2 + -a;
#print(d - 4 * a);'''
'''
# Give the lexer some input
lexer.input(input)

# Tokenize
for tok in lexer:    
    print tok.type,tok.value'''