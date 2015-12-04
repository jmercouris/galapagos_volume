#!/usr/bin/env python
# Imports
import os
import subprocess

# Main Function
def main():
    # List of audio devices
    audio_devices = []

    # AudioDevice Output
    get_volume_command = ['osascript', '-e', 'output volume of (get volume settings)']
    set_volume_command = ['osascript', '-e', 'set volume output volume {}']
    device = AudioDevice("Output", set_volume_command, get_volume_command)
    audio_devices.append(device)

    device.set_volume(85)

    # AudioDevice Input
    get_volume_command = ['osascript', '-e', 'input volume of (get volume settings)']
    set_volume_command = ['osascript', '-e', 'set volume input volume {}']
    device = AudioDevice("Input", set_volume_command, get_volume_command)
    audio_devices.append(device)
    

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
    main()

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
