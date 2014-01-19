#!/usr/bin/env python

import re
import types

class MultiReplace(object):
    """An all-in-one multiple string substitution class."""
    def __init__(self, config):
        self.config = config
        self.from_to = []
        self.compile()

    def compile(self):
        """ Build a regular expression object based on the keys of
            the current dictionary."""
        self.from_to = []
        for ft in self.config['from_to']:
            self.from_to.append((re.compile(ft['from']), ft['to']))

    def replacer(self, to):
        """Function closure to create handle all replace text."""
        def rep(match):
            if not isinstance(to, basestring):
                # could do something with groups here.
                return to(match.group(0))
            return match.expand(to)
        return rep

    def sub(self, s):
        """Translate text, returns the modified text."""
        for re_from, to in self.from_to:
            s = re_from.sub(self.replacer(to), s)
        return s
