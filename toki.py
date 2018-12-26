#!/usr/bin/python
import sys
import io
import cmd
import tokiLex
import sqlite3
import os
import datetime
import pandas as pd

from TokiClass import TokiTask
from TokiClass import TokiShowToday
from TokiClass import TokiShowWeek

class TokiException(Exception):
    pass


def run(text_in):
    ## Function to run what input in command ##
    parsed_input = tokiLex.parser.parse(text_in)
    print(parsed_input)
    return parsed_input

def error(line_num, message):
    ## Function for Error Handling ##
    report(line_num, '', message)
    raise TokiException


def report(line_num, where, message):
    ## Function to print error message ##
    print('[line ' + str(line_num) + '] Error' + where + ': ' + message)

def write_to_db(c, data):
    if data.endTime==None: #FIXME: need to consider more none types
        c.execute("INSERT INTO calendar VALUES (?,?,?,?,?,?)", (data.title,data.startTime
        ,data.endTime,data.repeat,data.person,datetime.datetime.now() ))
    else:
        c.execute("INSERT INTO calendar(title, startTime, endTime, repeat, person, ts) VALUES (?,?,?,?,?,?)", (data.title,data.startTime
        ,data.endTime,data.repeat,data.person,datetime.datetime.now() ))
    #, ?, ?, ?, ?, ?
    # ,data.startTime,data.duration,data.repeat,data.person,datetime.datetime.now()

def show_today(c):
    today = datetime.datetime.today().date()
    startT = pd.to_datetime(today + datetime.timedelta(seconds=0)).to_pydatetime()
    endT = pd.to_datetime(today + datetime.timedelta(hours=24)).to_pydatetime()
    print(c.execute('SELECT * FROM calendar WHERE startTime BETWEEN ? AND ? ORDER BY startTime', (startT, endT)).fetchall())



def show_this_week(c):
    today = datetime.datetime.today().date()
    startT = dt - timedelta(days=today.weekday())
    endT = start + timedelta(days=6)
    print(c.execute('SELECT * FROM calendar WHERE startTime BETWEEN ? AND ? ORDER BY startTime', (startT, endT)).fetchall())



def main():
    if not os.path.isfile('tokidb.db'):
        conn= sqlite3.connect('tokidb.db',detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        c.execute("CREATE TABLE calendar(title, startTime timestamp, endTime timestamp, repeat,\
        person, ts timestamp)")
        conn.commit()
    else:
        conn= sqlite3.connect('tokidb.db')
    c = conn.cursor()
    while True:
        try:
            text_in = input(">>")
            parsed_input = run(text_in)
            if isinstance(parsed_input, TokiTask):
                write_to_db(c, parsed_input)
                conn.commit()
            elif isinstance(parsed_input,TokiShowToday):
                show_today(c)
            elif isinstance(parsed_input,TokiShowWeek):
                show_this_week(c)
        except TokiException:
            print('error') #FIXME
    conn.close()

if __name__ == '__main__':



    main()
