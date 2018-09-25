import yacc
import lex
import lexer
from sys import exit

tokens = lexer.tokens

precedence = (
    ('nonassoc', 'LTGT'),
    ('left', 'OPERATOR')
)

def p_instruction(t):
    '''instruction : NUMBER ':' assign_instruction NEWLINE
                    | NUMBER ':' RETURN E NEWLINE
                    | NUMBER ':' goto_instruction NEWLINE'''

def p_assign_instruction(t):
    '''assign_instruction : ID ASSIGN E'''

def p_goto_instruction(t):
    '''goto_instruction : IF condition GOTO LPAR NUMBER RPAR
                        | GOTO LPAR NUMBER RPAR'''

def p_condition(t):
    '''condition : E LTGT E'''

def p_E(t):
    '''E : E OPERATOR E
        | LPAR E RPAR
        | ID
        | NUMBER'''

def p_error(p):
    print("Syntax error")
    exit(0)

yacc.yacc()
