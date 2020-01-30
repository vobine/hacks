#! /usr/bin/env python3

import argparse
import string
from random import choice, shuffle


class Pwgen:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.bets = []

    def add_alphabet(self, alf):
        if self.verbose:
            print('Adding alphabet "{0:s}"'.format(alf))
        self.bets.append(alf)

    def mnsure(self):
        self.add_alphabet(string.ascii_lowercase)
        self.add_alphabet(string.ascii_uppercase)
        self.add_alphabet(string.digits)
        self.add_alphabet("!#$%&'(),.:=?@ ")

    def paychex(self):
        self.add_alphabet(string.ascii_lowercase)
        self.add_alphabet(string.ascii_uppercase)
        self.add_alphabet(string.digits)
        self.add_alphabet('@.-_')

    def generate(self, length=8):
        result = []
        allbet = ''
        # 1: Make sure we have at least one from each alphabet
        for bet in self.bets:
            result.append(choice(bet))
            length -= 1
            allbet += bet

        # 2: Select additional characters at random
        for i in range(length):
            result.append(choice(allbet))

        # 3: Permute the result to remove artifacts from stage 1
        shuffle(result)

        return ''.join(result)


def main():
    parser = argparse.ArgumentParser(description='Password generator')
    parser.add_argument('-p', '--profile',
                        choices=('mnsure', 'paychex'))
    parser.add_argument('-a', '--alphabet', action='append')
    parser.add_argument('-d', '--digits', action='store_true')
    parser.add_argument('-l', '--lower', action='store_true')
    parser.add_argument('-u', '--upper', action='store_true')

    parser.add_argument('-n', '--length', action='store', default=16)
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()

    gen = Pwgen(args.verbose)

    if args.profile == 'mnsure':
        gen.mnsure()
    elif args.profile == 'paychex':
        gen.paychex()
    else:
        if args.alphabet:
            for arg in args.alphabet:
                gen.add_alphabet(arg)
        if args.digits:
            gen.add_alphabet(string.digits)
        if args.lower:
            gen.add_alphabet(string.ascii_lowercase)
        if args.upper:
            gen.add_alphabet(string.ascii_uppercase)

    try:
        print('"{0:s}"'.format(gen.generate(int(args.length))))
    except IndexError:
        print('Provide at least of --profile, --alphabet, --digits, --lower, --upper')


if __name__ == '__main__':
    main()
