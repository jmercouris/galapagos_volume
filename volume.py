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
        draw_bar(default_padding, (bar_height * index) + default_padding, bar_height, device)

def draw_bar(x, y, bar_height, device):
    device.set_volume(29)
    box = curses.newwin(bar_height, 50, y, x)
    box.bkgd(' ', curses.color_pair(1))
    box.immedok(True)
    box.box()
    box.addstr("{} Volume:{}".format(device.name, device.get_volume()))

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
        return out

if __name__ == "__main__":
    main()

# osascript -e "set Volume 0"
# osascript -e 'set ovol to output volume of (get volume settings)'
# osascript -e "set volume input volume 100"
