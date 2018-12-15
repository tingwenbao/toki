#!/usr/bin/python
import sys
import io
import cmd
import tokiLex
import sqlite3
import os
import datetime

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

# def maybe_init_db():
#     if not os.path.isfile('tokidb.db'):
#         conn= sqlite3.connect('tokidb.db')
#         c = conn.cursor()
#         c.execute("CREATE TABLE calendar(title TEXT, test TEXT)")
                #, startTime timestamp, duration, repeat, person, Timestamp timestamp

def write_to_db(conn, data):
    c = conn.cursor()
    if data.endTime==None: #FIXME: need to consider more none types
        c.execute("INSERT INTO calendar VALUES (?,?,?,?,?,?)", (data.title,data.startTime.strftime('%m-%d-%Y %H:%M:%S.%f')
        ,data.endTime,data.repeat,data.person,datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S.%f') ))
    else:
        c.execute("INSERT INTO calendar VALUES (?,?,?,?,?,?)", (data.title,data.startTime.strftime('%m-%d-%Y %H:%M:%S.%f')
        ,data.endTime.strftime('%m-%d-%Y %H:%M:%S.%f'),data.repeat,data.person,datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S.%f') ))
    conn.commit()
    #, ?, ?, ?, ?, ?
    # ,data.startTime,data.duration,data.repeat,data.person,datetime.datetime.now()

def main():
    if not os.path.isfile('tokidb.db'):
        conn= sqlite3.connect('tokidb.db')
        c = conn.cursor()
        c.execute("CREATE TABLE calendar(title, startTime, endTime, repeat,\
        person, Timestamp)")
        conn.commit()
    else:
        conn= sqlite3.connect('tokidb.db')

    while True:
        try:
            text_in = input(">>")
            parsed_input = run(text_in)
            write_to_db(conn, parsed_input)
        except TokiException:
            print('error') #FIXME
    conn.close()

if __name__ == '__main__':



    main()
