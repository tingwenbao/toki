#!/usr/bin/python
import sys
import io
import cmd
import tokiLex

class TokiException(Exception):
    pass


def run(text_in):
    ## Function to run what input in command ##
    tokiLex.parser.parse(text_in)
    print(tokiLex.tokiResult.duration)

def error(line_num, message):
    ## Function for Error Handling ##
    report(line_num, '', message)
    raise TokiException


def report(line_num, where, message):
    ## Function to print error message ##
    print('[line ' + str(line_num) + '] Error' + where + ': ' + message)



def main():

    while True:
        try:
            text_in = input(">>")
            run(text_in)
        except TokiException:
            print('error') #FIXME


if __name__ == '__main__':

    main()
