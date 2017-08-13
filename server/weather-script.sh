#!/bin/sh

cd "$(dirname "$0")"

python3 weather-script.py
rsvg-convert --background-color=white -w 758 -h 1024 -o weather-script-output.png weather-script-output.svg
pngcrush -c 0 -ow weather-script-output.png
cp -f weather-script-output.png /var/www/html/bg.png
