#! /usr/bin/env python3

from random import choice

class Dictionary:
    def __init__ (self, infile):
        with open (infile, 'rt') as inf:
            self.words = [ll.strip () for ll in inf]

    def choose (self, n=4):
        return [choice (self.words) for i in range (n)]

if __name__ == "__main__":
    dd = Dictionary ('/usr/share/dict/cracklib-small')
    print ('Random: {0:s}'.format (','.join (dd.choose ())))
