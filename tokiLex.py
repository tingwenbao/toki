#!/usr/bin/python
import re
import datetime
import pandas as pd

from TokiClass import TokiTask

global tokiResult
tokiResult = TokiTask()

### Tokens ###
tokens = (
    'SCHEDULE', 'AT', 'FROM', 'TO', 'FOR', 'EVERY', 'EVERYOTHER', 'APPOINTMENT', 'WITH',
    'DATE', 'TIMES', 'WEEK','MONTH','YEAR','HOUR','MINUTE','DAY', 'WEEKDAY',
    'ON', 'NUMBER'
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
t_TIMES = r'times a'
t_WEEK = r'week|weeks'
t_MONTH = r'month|months'
t_YEAR = r'year|years|yr|yrs'
t_HOUR = r'hour|hours|hr|hrs'
t_DAY = r'day|days|d'
t_MINUTE = r'minute|minutes|min'
t_ON = r'on'
#t_WEEKDAY = r'MONDAY|'

def t_DATE(t):
    r'(\d{2})[\/.-](\d{2})[/.-](\d{4})' # 1/1/2018 or 1-1-2018
    return t

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


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
start = 'ondate'


def p_expression_duration(t):
    '''experssion : FOR NUMBER MINUTE
        | FOR NUMBER HOUR
        | FOR NUMBER DAY
        | FOR NUMBER WEEK
        | FOR NUMBER MONTH
        | FOR NUMBER YEAR'''

    if t[1] == 'for' and re.match(t_MINUTE, t[3]):
        duration = datetime.timedelta(minutes = int(t[2]))
    elif t[1]=='for' and re.match(t_HOUR, t[3]):
        duration = datetime.timedelta(hours = number[t[2]])
    elif t[1]=='for' and re.match(t_DAY, t[3]):
        duration = datetime.timedelta(days = number[t[2]])
    elif t[1]=='for' and re.match(t_MONTH, t[3]):
        duration = datetime.timedelta(months = number[t[2]])
    elif t[1]=='for' and re.match(t_YEAR, t[3]):
        duration = datetime.timedelta(years = number[t[2]])
    tokiResult.duration = duration
    return duration

def p_expression_ondate(t):
    'ondate : ON DATE'
    if t[1] == 'on':
        d = pd.to_datetime(t[2])
    tokiResult.startTime = d
    return d

def p_error(t):
    print("Syntax error at '%s'" % t.value)
    print(t)


# Build the parser
import ply.yacc as yacc
parser = yacc.yacc()
