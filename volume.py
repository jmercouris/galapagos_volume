#!/usr/bin/env python
# Imports
import curses
from curses import wrapper
import curses.ascii
import os
import subprocess

# Global Variables
screen = None
dimensions = None
default_padding = 5
escape_character = 27
audio_devices = []

# Main Function
def main(stdscr):
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

    # AudioDevice Output
    get_volume_command = ['osascript', '-e', 'output volume of (get volume settings)']
    set_volume_command = ['osascript', '-e', 'set volume output volume {}']
    device = AudioDevice("Output", set_volume_command, get_volume_command)
    audio_devices.append(device)

    # AudioDevice Input
    get_volume_command = ['osascript', '-e', 'input volume of (get volume settings)']
    set_volume_command = ['osascript', '-e', 'set volume input volume {}']
    device = AudioDevice("Input", set_volume_command, get_volume_command)
    audio_devices.append(device)
    
    # Initialize Default Bar State
    bar_height = (dimensions[0] - default_padding * 2) / len(audio_devices)
    for index, device in enumerate(audio_devices):
        height = bar_height
        width = int(float(device.get_volume())/100 * float(dimensions[1] - (default_padding * 2)))
        x = default_padding
        y = index * bar_height + default_padding
        
        device.bar = curses.newwin(height, width, y, x)
        device.bar.bkgd(' ', curses.color_pair(1))
        device.bar.immedok(True)
        device.bar.box()
    
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

    for device in audio_devices:
        draw_bar(device)

def draw_bar(device):
    # Retrieve Important information
    volume = device.get_volume()
    name = device.name
    # Global
    global dimensions
    global default_padding
    width = int(float(volume)/100 * float(dimensions[1] - (default_padding * 2)))
    device.bar.resize(10, width)
    device.bar.addstr("{} Volume:{}".format(name, volume))

class AudioDevice:
    def __init__(self, name, set_volume_command, get_volume_command):
        self.name = name
        self.set_volume_command = set_volume_command
        self.get_volume_command = get_volume_command
    def set_volume(self, volume):
        local_command = self.set_volume_command
        local_command[2] = self.set_volume_command[2].format(volume)
        process = subprocess.Popen(self.set_volume_command, stdout = subprocess.PIPE)
        out, err = process.communicate('')
    def get_volume(self):
        process = subprocess.Popen(self.get_volume_command, stdout = subprocess.PIPE)
        out, err = process.communicate('')
        return int(out)

if __name__ == "__main__":
    wrapper(main)

# Original Source: https://coderwall.com/p/22p0ja/set-get-osx-volume-mute-from-the-command-line
# Get volume
# # Echos a number from 0 to 100
# osascript -e 'output volume of (get volume settings)'
# Set volume
# # Where 50 is a number from 0 to 100
# osascript -e 'set volume output volume 50'
# Get mute state
# # Echos a string of 'true' or 'false'
# osascript -e 'output muted of (get volume settings)'
# Set mute state
# # Where 'true' can be 'true' or 'false'
# osascript -e 'set volume output muted true'
