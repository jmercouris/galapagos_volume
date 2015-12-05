# Galapagos Volume
Program used to control the volume in a Curses like interface for OSX.

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

## How to create new distributions with Pyinstaller?
http://www.pyinstaller.org

pyinstaller -F program.py



## Shell Commands to Change the Volume (This program executes/wraps these commands)

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
