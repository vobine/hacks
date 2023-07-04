#! /usr/bin/env python3

"""Speech-based electric coach for seven-minute workout."""

import pyttsx3
from argparse import ArgumentParser
from itertools import chain
from random import shuffle
from sched import scheduler
from threading import Thread
import time
from tkinter import Tk, ttk
import tkthread

tkthread.patch()

class Exercise:
    """"""

    def __init__(self, exercise, workout, window):
        """"""
        self._exercise = exercise
        self._workout = workout
        self._schedule = scheduler(time.time, time.sleep)
        self._window = window

        self._window.header('Starting workout...')

        self._tts = pyttsx3.init()

    def say(self, utter):
        """"""
        self._tts.say(str(utter))
        self._tts.runAndWait()

    def show(self, head, count):
        """"""
        pass

    def run(self):
        """"""
        tkthread.call_nosync(self._window.header,
                             'Get ready for {0:s}'.format(self._exercise))
        self.say('Now, rest for 10 seconds.  Next up, ' + self._exercise)

        # Count down ten seconds of rest
        now = time.time() + 1
        for tick in range(1, 10):
            self._schedule.enterabs(now + 10 - tick, 1,
                                    self.say, argument=(tick,))
        self._schedule.run()

        self.say('Starting ' + self._exercise)
        tkthread.call_nosync(self._window.header, self._exercise)

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

class Prompt:
    """"""

    def __init__(self):
        """"""
        self._tk_root = Tk()
        self._tk_frame = ttk.Frame(self._tk_root)
        self._tk_frame.grid()
        self._tk_header = ttk.Label(self._tk_frame)
        self._tk_header.grid(column=0, row=0)
        self._tk_body = ttk.Label(self._tk_frame)
        self._tk_body.grid(column=0, row=1)

    def header(self, header):
        """"""
        self._tk_header.config(text=header)

    def body(self, body):
        """"""
        self._tk_body.config(text=str(body))

    def run(self):
        """"""
        self._tk_root.mainloop()

    def finish(self):
        """"""
        self._tk_root.destroy()

def run(exercises, window):
    """Run scheduled prompts.
    This is in a separate function to run in a separate thread."""
    for exercise, workout in exercises:
        print('{0:s} ({1:s})'.format(exercise, workout))
        eee = Exercise(exercise, workout, window)
        eee.run()
    window.finish()

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

    window = Prompt()
    ttt = Thread(target=run, args=(Exercises, window), daemon=True)
    ttt.start()
    window.run()

if '__main__' == __name__:
    main()
