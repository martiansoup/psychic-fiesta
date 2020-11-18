#!/bin/bash
cd `dirname "$0"`

echo "Starting command"
cmd=`python3 lights.py 2>&1`
echo "Command done"

echo "Output:"
echo $cmd

env DISPLAY=:0.0 zenity --warning --title="Error" --text="$cmd" --no-markup --width=400 &
echo "Starting fallback"
python3 fallback.py
