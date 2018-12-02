#!/usr/bin/python
import re
from datetime import timedelta

from TokiClass import TokiTask

global tokiResult
tokiResult = TokiTask()

### Tokens ###
tokens = (
    'SCHEDULE', 'AT', 'FROM', 'TO', 'FOR', 'EVERY', 'EVERYOTHER', 'APPOINTMENT', 'WITH',
    'NUMBER', 'DATE', 'TIMES', 'WEEK','MONTH','YEAR','HOUR','MINUTE','DAY',
)

t_SCHEDULE = r'schedule'
t_AT = r'at'
t_FROM = r'from'
t_TO = r'to'
t_FOR = r'for'
t_EVERY = r'every'
t_EVERYOTHER = r'every other'
t_APPOINTMENT = r'appointment'
t_WITH = r'with'
t_DATE = r'[(\d+/\d+/\d+)|(\d+\-\d+\-\d+)]'  # 1/1/2018 or 2018-1-1
t_TIMES = r'times a'
t_WEEK = r'[week|weeks]'
t_MONTH = r'[month|months]'
t_YEAR = r'[year|years|yr|yrs]'
t_HOUR = r'[hour|hours|hr|hrs]'
t_DAY = r'[day|days|d]'

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# def t_MINUTE(t):
#     r'minute|minutes|min'
#     t.value = 1
#     return t
t_MINUTE = r'minute|minutes|min'
# Ignored characters
t_ignore = " \t"

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

### Parsing Rules ###
#
# precedence = (
#
# )


# def p_expression_frequency(t):
#     '''expression: EVERY expression
#         | EVERY OTHER expressioin
#         | NUMBER TIMES WEEK
#         | NUMBER TIMES MONTH
#         | NUMBER TIMES YEAR
#         | EVERY NUMBER WEEK
#         | EVERY NUMBER MONTH
#         | EVERY NUMBER YEAR'''



def p_expression_duration(t):
    '''experssion : FOR NUMBER MINUTE
        | FOR NUMBER HOUR
        | FOR NUMBER DAY
        | FOR NUMBER WEEK
        | FOR NUMBER MONTH
        | FOR NUMBER YEAR'''
    print(t[1])
    print(t[2])
    print(t[3])
    print(t_MINUTE)
    print(re.match(t_MINUTE, t[3]))
    #duration = timedelta(minutes = t[2] * t[3])
    if t[1] == 'for' and re.match(t_MINUTE, t[3]):
        duration = timedelta(minutes = int(t[2]))
    # elif t[1]=='for' and t_HOUR.match(t[3]):
    #     duration = timedelta(hours = number[t[2]])
    # elif t[1]=='for' and t_DAY.match(t[3]):
    #     duration = timedelta(days = number[t[2]])
    # elif t[1]=='for' and t_MONTH.match(t[3]):
    #     duration = timedelta(months = number[t[2]])
    # elif t[1]=='for' and t_YEAR.match(t[3]):
    #     duration = timedelta(years = number[t[2]])
    tokiResult.duration = duration
    return duration


def p_error(t):
    print("Syntax error at '%s'" % t.value)
    print(t)


# Build the parser
import ply.yacc as yacc
parser = yacc.yacc()
