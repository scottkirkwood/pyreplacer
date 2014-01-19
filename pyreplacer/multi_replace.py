#!/usr/bin/env python

import re

class MultiReplace(object):
    """An all-in-one multiple string substitution class."""
    def __init__(self, config):
        self.re = None
        self.regex = None
        self.config = config
        self.compile()

    def compile(self):
        """ Build a regular expression object based on the keys of
            the current dictionary."""
        for index, from_to in enumerate(self.config['from_to']):
            from_to['compiled_from'] = re.compile(from_to['from'])

    def sub(self, s):
        """Translate text, returns the modified text."""
        for from_to in self.config['from_to']:
            s = from_to['compiled_from'].sub(from_to['to'], s)
        return s

#
# Test
#
if __name__ == '__main__':
    text = 'Larry Wall is the creator of Perl'
    config = {
        'from_to': [
            {
                'from': r'L.+ W.l+',
                'to': 'Guido van Rossum',
            }, {
                'from': 'creator',
                'to':'Benevolent Dictator for Life'
            }, {
                'from': 'Perl',
                'to': 'Python'
            },
        ],
    }
    sub = MultiReplace(config)
    new = sub.sub(text)
    print new
