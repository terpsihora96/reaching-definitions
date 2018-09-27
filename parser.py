import yacc
import lexer
from sys import exit

tokens = lexer.tokens

precedence = (
    ('nonassoc', 'LTGT'),
    ('left', 'PLUS', 'MINUS', 'TIMES','DIVIDE')
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
    '''E : var_num PLUS var_num
        | var_num MINUS var_num
        | var_num DIVIDE var_num
        | var_num TIMES var_num
        | var_num'''

def p_var_num(t):
    '''var_num : NUMBER
                | ID
                | MINUS ID
                | MINUS NUMBER'''

def p_error(t):
    print("Syntax error.")
    exit(0)

yacc.yacc()
