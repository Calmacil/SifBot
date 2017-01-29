#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Dice module for SifBot

cli launchable for testing purposes
"""

import re
import random
from math import floor

class DiceError(Exception):
    pass

class DiceBag(object):
    """ A simple pool for the Chronicles system

    format: x?[dk]y? + z > t
    multiple throws are managed upper (one dicebag instanciated for each throw)
    """

    def __init__(self, expression):
        """ inits the bag """
        self.chunks = expression[:50]

        self.dice = 0
        self.keeps = 0
        self.bonus = 0
        self.target = 9 # default difficulty is 9

        self.keep_max = True
        self._parse()

    def _parse(self):
        """ Parses the components of the throw """
        adds_factor = 1
        pattern = re.compile("(\d+)?([kKdDbB])(\d+)?")

        for chunk in self.chunks:
            if chunk == "+":
                adds_factor = 1
            elif chunk == "-":
                adds_factor = -1
            elif chunk == ">":
                # next factor will be target difficulty!
                adds_factor = 0
            elif chunk.isdigit():
                self.bonus += int(chunk) * adds_factor # anything + 0 remains unchanged
                if adds_factor == 0:
                    self.target = 0
                    break # difficulty always be the last chunk!
            else:
                m = pattern.match(chunk)

                # This part is dubious
                if m is not None:
                    t_die_letter = m.group(2).upper()
                    t_dice = 0
                    t_keep = 0
                    if m.group(1) is not None:
                        t_dice = int(m.group(1))
                    if m.group(3) is not None:
                        t_keep = int(m.group(3))

                    if "D" == t_die_letter:
                        if adds_factor == 1:
                            self.dice += t_dice
                            self.keeps += t_dice
                        elif adds_factor == -1:
                            self.keeps -= t_dice
                    elif "B" == t_die_letter :
                        if adds_factor == 1:
                            self.dice += t_dice
                            # you cannot do -xB
                    else: #well, that's a Keep
                        self.dice += t_dice * adds_factor
                        self.keeps += t_keep * adds_factor

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
            results.append(self._rollOneDie())

        results.sort(reverse=self.keep_max)

        total = sum(results[0:self.keeps])
        successes = floor((total - self.target) / 5)

        # something occures bad here
        return "%s Total: %d" % (
               str(results), sum(results[0:self.keeps]) + self.bonus), successes

    def _rollOneDie(self):
        """ Rolls a single die
        No need for explosivity here, just a single randint will do
        """
        return random.randint(1, 6)

    def __str__(self):
        return "%sD + %sB + %s (seuil %s)" % (self.keeps, self.dice - self.keeps, self.bonus, self.target)

if __name__ == '__main__':

    from sys import argv
    bag = DiceBag(argv[1:])
    print(bag)
    print(bag.roll())
