#!/usr/bin/python
import re
import datetime
import pandas as pd
import sqlite3

from TokiClass import TokiTask

#create toki class
global tokiResult
tokiResult = TokiTask()
tokiResult.startTime = datetime.datetime.combine(datetime.date.today(), datetime.time.min)

#connect to db
c = conn.cursor()

### Tokens ###
tokens = (
    'SCHEDULE', 'AT', 'FROM', 'TO', 'FOR', 'EVERY', 'EVERYOTHER', 'APPOINTMENT', 'WITH',
    'DATE', 'TIMES', 'WEEK','MONTH','YEAR','HOUR','MINUTE','DAY', 'WEEKDAY',
    'ON', 'NUMBER','AM','PM','OCLOCK', 'PERSON'
)

def t_SCHEDULE(t):
    r'schedule'
    return t

def t_AT(t):
    r'at'
    return t

def t_FROM(t):
    r'from'
    return t

def t_TO(t):
    r'to'
    return t

def t_FOR(t):
    r'for'
    return t

def t_EVERY(t):
    r'every'
    return t

def t_EVERYOTHER(t):
    r'every other'
    return t

def t_APPOINTMENT(t):
    r'appointment'
    return t

def t_WITH(t):
    r'with'
    return t

def t_TIMES(t):
    r'times a'
    return t

def t_WEEK(t):
    r'week|weeks'
    return t

def t_MONTH(t):
    r'month|months'
    return t

def t_YEAR(t):
    r'year|years|yr|yrs'
    return t

def t_HOUR(t):
    r'hour|hours|hr|hrs'
    return t

def t_DAY(t):
    r'day|days|d'
    return t

def t_MINUTE(t):
    r'minute|minutes|min'
    return t

def t_ON(t):
    r'on'
    return t

def t_AM(t):
    r'AM'
    return t

def t_PM(t):
    r'PM'
    return t

#t_WEEKDAY = r'MONDAY|'

def t_DATE(t):
    r'(\d{2})[/.-](\d{2})[/.-](\d{4})' # 1/1/2018 or 1-1-2018
    return t

def t_OCLOCK(t):
    r'(\d+)\:(\d{2})'  # 11:00
    return t

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_PERSON(t):
    r'([A-Z][a-z]*)([\\s\\\'-][A-Z][a-z]*)*'
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

# def p_expression_frequency(t):
#     '''expression: EVERY expression
#         | EVERY OTHER expressioin
#         | NUMBER TIMES WEEK
#         | NUMBER TIMES MONTH
#         | NUMBER TIMES YEAR
#         | EVERY NUMBER WEEK
#         | EVERY NUMBER MONTH
#         | EVERY NUMBER YEAR'''

start = 'schedule'

def p_expression_schedule(t):
    '''schedule : SCHEDULE appointment ondate
        | SCHEDULE appointment ondate attime
        | SCHEDULE appointment ondate attime duration'''
    print(tokiResult)


def p_expression_duration(t):
    '''duration : FOR NUMBER MINUTE
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


def p_expression_ondate(t):
    'ondate : ON DATE'
    if t[1] == 'on':
        d = pd.to_datetime(t[2])
    tokiResult.startTime = d


def p_expression_attime(t):
    '''attime : AT NUMBER AM
        | AT NUMBER PM
        | AT OCLOCK'''
    if t[1]=='at' and t[3]=='AM':
        h = datetime.timedelta(hours = t[2])
    elif t[1]=='at' and t[3]=='PM':
        h =datetime.timedelta(hours = 12 + int(t[2]))
    else:
        h =  pd.to_datetime(t[2]).time()
    tokiResult.startTime = tokiResult.startTime + h


def p_expression_appointment(t):
    '''appointment : APPOINTMENT WITH PERSON
        | APPOINTMENT'''
    if len(t)>2:
        if t[2] == 'with':
            tokiResult.person = t[3]


def p_error(t):
    print("Syntax error at '%s'" % t.value)
    print(t)


# Build the parser
import ply.yacc as yacc
parser = yacc.yacc()
