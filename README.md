# Galapagos Volume
Program used to control the volume in a Curses like interface for OSX.

Named galapagos after the voyage of Charles Darwin. Named after Darwin """Darwin is an open source Unix operating system released by Apple Inc. in 2000. It is composed of code developed by Apple, as well as code derived from NeXTSTEP, BSD, and other free software projects."""
https://en.wikipedia.org/wiki/Darwin_(operating_system)

pyinstaller -F program.py



## Shell Commands to Change the Volume (This program executes/wraps these commands)

Src: https://coderwall.com/p/22p0ja/set-get-osx-volume-mute-from-the-command-line

+Get volume
+Echos a number from 0 to 100
+`osascript -e 'output volume of (get volume settings)'`
+Set volume
+Where 50 is a number from 0 to 100
+`osascript -e 'set volume output volume 50'`
+Get mute state
+Echos a string of 'true' or 'false'
+`osascript -e 'output muted of (get volume settings)'`
+Set mute state
+Where 'true' can be 'true' or 'false'
+`osascript -e 'set volume output muted true'`
