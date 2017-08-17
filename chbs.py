#! /usr/bin/env python3

from random import choice
from argparse import ArgumentParser

class Dictionary:
    def __init__ (self, infile, limit=100):
        with open (infile, 'rt') as inf:
            self.words = tuple (ll.strip () for ll in inf if len (ll) <= limit + 1)

    def choose (self, n=4, total=1000):
        result = []
        for _ in range (n):
            word = choice (self.words)
            total -= len (word) + 1
            result.append (word)

        return result

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
                         default=100,
                         help='Maximum length of each word in passphrase')
    parser.add_argument ('--total', '-t',
                         action='store',
                         type=int,
                         default=1000,
                         help='Maximum number of characters in passphrase')
    parser.add_argument ('--words', '-w',
                         action='store',
                         type=int,
                         default=4,
                         help='Number of words in passphrase')

    args = parser.parse_args (argv)

    dd = Dictionary (args.dictionary, args.length)
    print ('Random: {0:s}'.format (','.join (dd.choose (args.words, args.total))))

if __name__ == "__main__":
    from sys import argv
    main (argv[1:])
