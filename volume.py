#!/usr/bin/env python
# Imports
import os
import subprocess
import urwid

class AudioDevice:
    """
    A class responsible for representing OSX audio devices
    """
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

class VolumeModel:
    """
    A class responsible for storing the data that will be displayed
    on the graph, and keeping track of which mode is enabled.
    """
    def __init__(self):
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
        
    def get_devices(self):
        return audio_devices

class VolumeView(urwid.WidgetWrap):
    """
    A class responsible for providing the application's interface and
    volume display.
    """
    def __init__(self, controller):
        self.controller = controller
        urwid.WidgetWrap.__init__(self, self.main_window())

    def main(self):
        pass

class VolumeController:
    """
    A class responsible for setting up the model and view and running
    the application.
    """
    def __init__(self):
        self.model = VolumeModel()
        self.view = VolumeView( self )

    def main(self):
        self.loop = urwid.MainLoop(self.view, self.view.palette)
        self.loop.run()

def main():
    VolumeController().main()

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
