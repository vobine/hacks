#! /bin/bash

################################################################
# Wrapper for seven.py
# Disables screensaver during workout
# Re-enables when finished
################################################################

rootID=` xwininfo -root | awk '$2=="Window" && $3=="id:"{print $4}' `

xdg-screensaver suspend $rootID

./seven.py "$@"

xdg-screensaver resume $rootID
