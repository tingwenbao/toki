#!/usr/bin/python

### Tokens ###
tokens = (
    'SCHEDULE', 'AT', 'FROM', 'TO', 'FOR', 'EVERY', 'TASK', 'FREQUENCY',
    'TIME_RANGE', 'TIME_POINT', 'ABSOLUTE_DATE', 'RELATIVE_DATE', 'DURATION',
    'APPOINTMENT', 'WITH', 'PERSON', 'NUMBER',
)

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

### Parsing Rules ###

def

# Build the parser
import ply.yacc as yacc
parser = yacc.yacc()
