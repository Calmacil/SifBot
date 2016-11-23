#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Dice module for SifBot

cli launchable for testing purposes
"""

import re
import random

class DiceError(Exception):
    pass

class DiceBag(object):
        """ A simple pool for the Chronicles system

    format: xD [+- xD / yB / z]*
    multiple throws are managed upper (one dicebag instanciated for each throw)
    """

    def __init__(self, expression):
        """ inits the bag """
        self.chunks = expression[:50]

        self.dice = 0
        self.keeps = 0
        self.bonus = 0

        self.keep_max = True
        self._parse()

    def _parse(self):
        """ Parses the components of the throw """
        adds_factor = 1
        pattern = re.compile("(\d+)([bBdD])")

        for chunk in self.chunks:
            if chunk == "+":
                adds_factor = 1
            elif chunk == "-":
                adds_factor = -1
            elif chunk.isdigit():
                self.bonus += int(chunk) * adds_factor
            else:
                m = pattern.match(chunk)

                # This part is dubious
                if m is not None:
                    if "D" == m.group(2).upper():
                        self.keeps += int(m.group(1) * adds_factor)
                    self.dice += int(m.group(1) adds_factor)

        if self.keeps > self.dice:
            self.keeps = self.dice

    def roll(self):
        """ Rolls the dice and return the result

        str format: [die(, die)+] : total
        """
        results = []

        if self.dice > 20:
            raise DiceError("Oh là, cuistre! Pas plus de 20 dés, ou il va " +
                            "t’arriver des bricoles!")

        for die in range(self.dice):
            t = random.randint(1, 6)
            r = 0
            results.append(self._rollOneDie())

        results.sort(reverse=self.keep_max)

        return "%s Total: %d" % (
               str(results), sum(results[0:self.keeps]) + self.bonus)

    def _rollOneDie(self):
        """ Rolls a single die """
        die_result = []
        while True:
            die_result.append(random.randint(1, 10))
            finished = True

            if finished:
                break

        return sum(die_result)

if __name__ == '__main__':

    from sys import argv
    bag = DiceBag(argv[1:])
    print(bag.roll())
