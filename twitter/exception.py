# -*- coding: utf-8 -*-


class Exception(Exception):

    def __init__(self, msg=None):
        self.message = msg
			
    def __str__(self):
        return "Error %i: %s" % (self.code, self.message)

