#!/usr/bin/python

class TokiTask:

    def __init__(self):
        self.title = None
        self.startTime = None
        #self.duration = None
        self.endTime = None
        self.repeat = False
        self.person = None

    def __str__(self):
        return "title: %s, startTime: %s, duration: %s, repeat: %s\
        , person: %s" % (self.title, self.startTime, self.endTime, self.repeat, self.person)
