#!/usr/bin/env python
# Original algorithm by Xavier Defrang.
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/81330
# This implementation by alane@sourceforge.net.

import re
import UserDict

class multi_replace(UserDict.UserDict):
    """ An all-in-one multiple string substitution class """
    def __init__(self, dict = None):
        self.re = None
        self.regex = None
        UserDict.UserDict.__init__(self, dict)
        self.compile()

    def compile(self):
        """ Build a regular expression object based on the keys of
            the current dictionary """
        if len(self.data) > 0:
            tmp = "(%s)" % "|".join(map(re.escape,
                                        self.data.keys()))
            if self.re != tmp:
                self.re = tmp
                self.regex = re.compile(self.re)

    def __call__(self, match):
        """ This handler will be invoked for each regex match """
        return self.data[match.string[match.start():match.end()]]

    def sub(self, s):
        """ Translate text, returns the modified text. """
        if len(self.data) == 0:
            return s
        return self.regex.sub(self, s)

#
# Test
#
if __name__ == "__main__":
    text = "Larry Wall is the creator of Perl"

    dict = {
        r"Larry Wall" : "Guido van Rossum",
        "creator" : "Benevolent Dictator for Life",
        "Perl" : "Python",
    }

    sub = multi_replace(dict)
    new = sub.sub(text)
    print new
