#! /usr/bin/env python3

from random import choice
from argparse import ArgumentParser

class Dictionary:
    def __init__ (self, infile):
        with open (infile, 'rt') as inf:
            self.words = [ll.strip () for ll in inf]

    def choose (self, n=4):
        return [choice (self.words) for i in range (n)]

def main (argv):
    """CLI."""
    parser = ArgumentParser (
        'CHBS:  generate a passphrase from random words.')
    parser.add_argument ('--dictionary', '-d',
                         action='store',
                         default='/usr/share/dict/cracklib-small',
                         help='List of words to choose from')
    parser.add_argument ('--length', '-l',
                         action='store',
                         type=int,
                         default=4,
                         help='Number of words in passphrase')

    args = parser.parse_args (argv)

    dd = Dictionary (args.dictionary)
    print ('Random: {0:s}'.format (','.join (dd.choose (args.length))))

if __name__ == "__main__":
    from sys import argv
    main (argv[1:])
