# Galapagos Volume
Program used to control the volume in a Curses like interface for OSX.

## Getting Galapagos
### Easy Install
Download from [GALAPAGOS DOWNLOAD](dist/volume). You may need to run `chmod +x volume`. Then, Simply execute volume.
You can add it to your path if you like for easier execution. Or add it where you keep your other programs
in your path. 
### Difficult Install with the possibility to change code
You can choose to download this entire repository, install URWID (http://urwid.org) and then run
python volume.py as you would any other program.

## Usage
+ `volume`
  + When started from the command line with no arguments, volume will produce a terminal GUI

+ `volume -v 80`
  + set the volume to 80/100

+ `volume -v 65 -d input`
  + set the input volume to 65/100

+ `volume -d input`
  + show the input volume

## What is Galapagos?
Galapagos Volume is a wrapper utility for setting the volume in OSX.
It works by calling applescript commands in a subprocess to set the volume. There are a couple
of ways to use Galapagos Volume, the first is by just running the program without any parameters
this will produce a GUI that allows you to increase or decrease the volume for input and output.
The second is with the flags -d -device, and -v -volume. If you specify a "-d output" or a "-d input" 
the system will return the volume for that device. For example, "volume -d output" will return the output volume. 
If you specify a device and a volume, the system will SET the volume for that device. Therefore a sample
command to set the output would be "volume -d output -v 85", this would set the output volume to 85.

## Why is it named Galapagos?
Named galapagos after the voyage of Charles Darwin. Named after Darwin """Darwin is an open source Unix operating system released by Apple Inc. in 2000. It is composed of code developed by Apple, as well as code derived from NeXTSTEP, BSD, and other free software projects."""
https://en.wikipedia.org/wiki/Darwin_(operating_system)

## Why did you make Galapagos?
I made Galapagos because I like doing things from the command line, sometimes I am just SSH'd into my machine, or I
have a full screen terminal open. I don't like going away from it and using the mouse.

## How to create new distributions with Pyinstaller?
http://www.pyinstaller.org

+ `rm -rf dist`
+ `pyinstaller -F volume.py`

## Shell Commands to Change the Volume
### (This program executes/wraps these commands)

Src: https://coderwall.com/p/22p0ja/set-get-osx-volume-mute-from-the-command-line

+ Get volume
  + Echos a number from 0 to 100
  + `osascript -e 'output volume of (get volume settings)'`
+ Set volume
  + Where 50 is a number from 0 to 100
  + `osascript -e 'set volume output volume 50'`
+ Get mute state
  + Echos a string of 'true' or 'false'
  + `osascript -e 'output muted of (get volume settings)'`
+ Set mute state
  + Where 'true' can be 'true' or 'false'
  + `osascript -e 'set volume output muted true'`
