#! /usr/bin/env python3

"""Speech-based electric coach for seven-minute workout."""

import pyttsx3
from argparse import ArgumentParser
from itertools import chain
from random import shuffle
from sched import scheduler
import time

class Exercise:
    """"""

    def __init__(self, exercise, workout):
        """"""
        self._exercise = exercise
        self._workout = workout
        self._schedule = scheduler(time.time, time.sleep)
        self._tts = pyttsx3.init()

    def say(self, utter):
        """"""
        self._tts.say(str(utter))
        self._tts.runAndWait()

    def run(self):
        """"""
        self.say('Now, rest for 10 seconds.  Next up, ' + self._exercise)

        # Count down ten seconds of rest
        now = time.time() + 1
        for tick in range(1, 11):
            self._schedule.enterabs(now + 10 - tick, 1,
                                    self.say, argument=(tick,))
        self._schedule.run()

        self.say('Starting ' + self._exercise)

        # Count down thirty seconds of exercise
        now = time.time() + 1   # Extra second for initialization
        for tick in chain(range(30, 5, -5), range(5, 0, -1)):
            self._schedule.enterabs(now + 30 - tick, 1,
                                    self.say, argument=(tick,))
        self._schedule.enterabs(now + 15, 1,
                                self.say,
                                argument=('Half-way with ' + self._exercise,))
        self._schedule.run()

        self.say('Completed ' + self._exercise)

def main():
    """"""
    Exercises = [('Abdominal crunch', 'core'),
                 ('High knees/running in place', 'total body'),
                 ('Jumping jacks', 'total body'),
                 ('Lunge', 'lower body'),
                 ('Plank', 'core'),
                 ('Push-up and rotation', 'upper body'),
                 ('Push-up', 'upper body'),
                 ('Side plank', 'core'),
                 ('Squat', 'lower body'),
                 ('Step-up onto chair', 'total body'),
                 ('Triceps dip on chair', 'upper body'),
                 ('Wall sit', 'lower body')]

    shuffle(Exercises)

    for exercise, workout in Exercises:
        print('{0:s} ({1:s})'.format(exercise, workout))
        eee = Exercise(exercise, workout)
        eee.run()

if '__main__' == __name__:
    main()
