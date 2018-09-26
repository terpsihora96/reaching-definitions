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
    '''condition : var_num LTGT var_num'''

def p_E(t):
    '''E : ID OPERATOR ID
        | ID OPERATOR NUMBER
        | NUMBER OPERATOR ID
        | NUMBER OPERATOR NUMBER
        | var_num'''

def p_var_num(t):
    '''var_num : NUMBER
                | ID'''

def p_error(t):
    print("Syntax error.")
    exit(0)

yacc.yacc()
