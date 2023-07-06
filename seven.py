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
    """Represents current state of an individual exercise,
    including prompting in progress."""

    def __init__(self, exercise, workout, window, i, n):
        """Takes the name of an exercise, workout area (core, full-body, etc.)
        a tkinter object for visual prompts, and context in the workout
        (exercise #i of #n)."""
        self._exercise = 'Exercise {0:d} of {1:d}: {2:s}'.format(i, n, exercise)
        self._workout = workout
        self._schedule = scheduler(time.time, time.sleep)
        self._window = window

        self._tts = pyttsx3.init()

    def say(self, utter):
        """Blurt a string via TTS."""
        self._tts.say(utter)
        self._tts.runAndWait()

    def show(self, widget, value):
        """Display text in one of the tkinter widgets."""
        tkthread.call_nosync(widget, str(value))

    def tick(self, value):
        """Announce time remaining in countdown."""
        self.show(self._window.body, str(value))
        self.say(str(value))

    def run(self):
        """Prompt for the exercise on a schedule:
         - 10 seconds rest/prep;
         - 30 seconds exercising.
        With a countdown and reminders along the way."""
        self.show(self._window.header,
                  'Get ready for {0:s}'.format(self._exercise))
        self.show(self._window.body, '')

        start = time.time()
        self.show(self._window.body, 10)
        self.say('Now, rest for 10 seconds.  Next up, ' + self._exercise)

        # Count down ten seconds of rest
        for tick in range(1, 5):
            self._schedule.enterabs(start + 10 - tick, 1,
                                    self.tick, argument=(tick,))
        self._schedule.run()

        self.show(self._window.header, self._exercise)
        self.show(self._window.body, '30')
        self.say('Starting ' + self._exercise)

        # Count down thirty seconds of exercise
        for tick in chain(range(25, 5, -5), range(5, 0, -1)):
            self._schedule.enterabs(start + 40 - tick, 1,
                                    self.tick, argument=(tick,))
        self._schedule.enterabs(start + 25.1, 1,
                                self.say,
                                argument=('Half-way with ' + self._exercise,))
        self._schedule.run()

        self.show(self._window.body, '')
        self.say('Completed.')

class Prompt:
    """Visual reminder of exercise in progress, including countdown."""

    def __init__(self, title='Seven-minute workout prompts'):
        """Initialize the window, give it a title."""
        self._tk_root = Tk()
        self._tk_root.title(title)
        self._tk_frame = ttk.Frame(self._tk_root)
        self._tk_frame.grid()

        ttk.Style().configure('TLabel',
                              font='helvetica 60',
                              width=-50,
                              justify='center')

        self._tk_header = ttk.Label(self._tk_frame)
        self._tk_header.grid(column=0, row=0)
        self._tk_body = ttk.Label(self._tk_frame)
        self._tk_body.grid(column=0, row=1)

    def header(self, header):
        """Set text in the upper Label:  typically exercise name."""
        self._tk_header.config(text=header)

    def body(self, body):
        """Set text in the lower Label:  typically the countdown."""
        self._tk_body.config(text=str(body))

    def run(self):
        """Run the tkinter application."""
        self._tk_root.mainloop()

    def finish(self):
        """Destroy the tkinter application."""
        self._tk_root.destroy()

def run(exercises, window):
    """Run scheduled prompts.
    This is in a separate function to run in a separate thread."""
    for iii, (exercise, workout) in enumerate(exercises):
        print('{0:s} ({1:s})'.format(exercise, workout))
        eee = Exercise(exercise, workout, window, iii + 1, len(exercises))
        eee.run()
    eee.say('Finished the full workout.')
    window.finish()

def main():
    """Command-line interface, defaults, and driver."""
    Exercises = [('Abdominal crunch', 'core'),
                 ('High knees running in place', 'total body'),
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
