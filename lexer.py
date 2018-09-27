import lex
from sys import exit

tokens = [
    'NUMBER', 'ID',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LTGT',
    'LPAR','RPAR', 'ASSIGN',
    'NEWLINE', 'IF', 'GOTO', 'RETURN'
]

def t_GOTO(t):
    r'(goto)|(GOTO)'
    t.value = t.value.lower()
    return t

def t_IF(t):
    r'(if)|(IF)'
    t.value = t.value.lower()
    return t

def t_RETURN(t):
    r'(return)|(RETURN)'
    t.value = t.value.lower()
    return t

def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_PLUS(t):
    r'[+]'
    return t

def t_MINUS(t):
    r'[-]'
    return t

def t_TIMES(t):
    r'[*]'
    return t

def t_DIVIDE(t):
    r'[/]'
    return t

def t_LTGT(t):
    r'(<=)|(>=)|[<>]'
    return t

def t_ASSIGN(t):
    r':='
    return t

def t_ID(t):
    r'([a-zA-Z]\w*\[\w+\])|([a-zA-Z]\w*)'
    return t

t_LPAR    = r'\('
t_RPAR    = r'\)'
t_NEWLINE = r'\n'

literals = [':']

t_ignore = " \t"

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    exit(0)

lex.lex()
