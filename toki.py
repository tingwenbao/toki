#!/usr/bin/python
import sys
import io
import cmd
import tokiLex
import sqlite3
import os

class TokiException(Exception):
    pass


def run(text_in):
    ## Function to run what input in command ##
    tokiLex.parser.parse(text_in)
    print(tokiLex)

def error(line_num, message):
    ## Function for Error Handling ##
    report(line_num, '', message)
    raise TokiException


def report(line_num, where, message):
    ## Function to print error message ##
    print('[line ' + str(line_num) + '] Error' + where + ': ' + message)

def maybe_init_db():
    if not os.path.isfile('tokidb.db'):
        conn= sqlite3.connect('tokidb.db')
        c = conn.cursor()
        c.execute(''' CREATE TABLE calendar
                (title, startTime, duration, repeat, person, Timestamp)''')

def main():

    maybe_init_db()

    while True:
        try:
            text_in = input(">>")
            run(text_in)
        except TokiException:
            print('error') #FIXME


if __name__ == '__main__':



    main()
