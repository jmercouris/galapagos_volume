#!/usr/bin/env python
# Imports
import curses 
import curses.ascii
import os
import subprocess

# Global Variables
screen = None
dimensions = None
# Padding between bars
default_padding = 5
# Getch escape representation
escape_character = 27
# List of audio devices
audio_devices = []

# Main Function
def main():
    global screen
    global dimensions
    global audio_devices

    # Disable output to terminal
    screen = curses.initscr()
    curses.noecho()
    screen.keypad(True)
    screen.immedok(True)
    screen.border(0)
    screen.addstr("System Volume Control")
    dimensions = screen.getmaxyx()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # AudioDevice List Initialization
    device = AudioDevice("osascript -e 'set volume output volume 50' &> /dev/null")
    audio_devices.append(device)
    audio_devices.append(device)
    audio_devices.append(device)
    audio_devices.append(device)
    audio_devices.append(device)

    # Main Input Loop
    user_input = ''
    # Break if user enters 'esc' or 'q'
    while ((user_input != escape_character) and (user_input != ord('q'))):
        user_input = screen.getch()
        draw_bars()
        screen.refresh()
    
    # Break out of main loop, end program
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()

def draw_bars():
    global audio_devices
    global dimensions
    global default_padding

    bar_height = (dimensions[0] - default_padding * 2) / len(audio_devices)

    for index, device in enumerate(audio_devices):
        draw_bar(default_padding, (bar_height * index) + default_padding, bar_height)

def draw_bar(x, y, bar_height):
    box = curses.newwin(bar_height, 5, y, x)
    box.addstr("Volume")
    box.bkgd(' ', curses.color_pair(1))
    box.immedok(True)
    box.box()
    box.addstr("Bar")

class AudioDevice:
    def __init__(self, system_command):
        self.system_command = system_command
    def execute_command(self):
        os.system(self.system_command)

if __name__ == "__main__":
    main()

# osascript -e "set Volume 0"
# osascript -e 'set ovol to output volume of (get volume settings)'
# osascript -e "set volume input volume 100"
