#!/usr/bin/env python
# Imports
import os
import subprocess  # Python execute sub process, in this case to send osascript commands
import urwid       # Replacement for curses, used in the Terminal GUI
import argparse    # Easily parse command line arguments

description_string = """Galapagos Volume is a wrapper utility for setting the volume in OSX.
It works by calling applescript commands in a subprocess to set the volume. There are a couple
of ways to use Galapagos Volume, the first is by just running the program without any parameters
this will produce a GUI that allows you to increase or decrease the volume for input and output.
The second is with the flags -d -device, and -v -volume. If you specify a "-d output" or a "-d input" 
the system will return the volume for that device. For example, "volume -d output" will return the output volume. 
If you specify a device and a volume, the system will SET the volume for that device. Therefore a sample
command to set the output would be "volume -d output -v 85", this would set the output volume to 85."""

# Represents an OSX audio device, e.g. input, output


class AudioDevice:
    """
    A class responsible for representing & manipulating OSX audio devices
    """

    def __init__(self, name, set_volume_command, get_volume_command):
        self.name = name
        self.set_volume_command = set_volume_command
        self.get_volume_command = get_volume_command
        self.volume = self.get_volume()

    def set_volume(self, volume):
        # Constrain Volume to Valid Range
        if (volume > 100):
            volume = 100
        if (volume < 0):
            volume = 0
        # Copy Command arguments list into local version for modification
        local_command = self.set_volume_command[:]
        local_command[2] = self.set_volume_command[2].format(volume)
        process = subprocess.Popen(local_command, stdout=subprocess.PIPE)
        out, err = process.communicate()
        self.volume = volume

    def get_volume(self):
        process = subprocess.Popen(
            self.get_volume_command, stdout=subprocess.PIPE)
        out, err = process.communicate()
        # Set Local volume to reflect system reported volume
        self.volume = int(out)
        return self.volume

# Represents the Data in the program


class VolumeModel:
    """
    Populating the default OSX AudioDevices
    """

    def __init__(self):
        # List of audio devices
        audio_devices = self.audio_devices = []
        # AudioDevice Output
        get_volume_command = ['osascript', '-e',
                              'output volume of (get volume settings)']
        set_volume_command = ['osascript', '-e', 'set volume output volume {}']
        device = AudioDevice("Output", set_volume_command, get_volume_command)
        audio_devices.append(device)
        # AudioDevice Input
        get_volume_command = ['osascript', '-e',
                              'input volume of (get volume settings)']
        set_volume_command = ['osascript', '-e', 'set volume input volume {}']
        device = AudioDevice("Input", set_volume_command, get_volume_command)
        audio_devices.append(device)

    def get_audio_devices(self):
        return self.audio_devices

# Class VolumeView, handles drawing and input


class VolumeView(urwid.WidgetWrap):
    """
    A class responsible for providing the application's interface and
    volume display.
    """
    # Colors used for rendering
    palette = [
        ('bg background', 'white', 'white'),
        ('bg 1',         'black',      'black', 'standout'),
        ('bg 1 smooth',  'dark blue',  'black'),
        ('bg 2',         'black',      'dark gray', 'standout'),
        ('bg 2 smooth',  'dark gray',  'black'),
        ('button normal', 'black', 'white', 'light gray'),
        ('button select', 'white',      'black'),
    ]
    # Initialization

    def __init__(self, controller):
        self.controller = controller
        self.audio_devices = self.controller.get_audio_devices()
        urwid.WidgetWrap.__init__(self, self.main_window())
    # Bar Graph Configuration

    def bar_graph(self, smooth=False):
        satt = None
        if smooth:
            satt = {(1, 0): 'bg 1 smooth', (2, 0): 'bg 2 smooth'}
        w = urwid.BarGraph(['bg background', 'bg 1', 'bg 2'], satt=satt)
        return w

    def button(self, t, fn):
        w = urwid.Button(t, fn)
        w = urwid.AttrWrap(w, 'button normal', 'button select')
        return w
    # Exit Program

    def exit_program(self, w):
        raise urwid.ExitMainLoop()
    # Change Volume

    def delta_output_up(self, w):
        device = self.audio_devices[0]
        device.set_volume(device.get_volume() + 5)
        self.update_graph()

    def delta_output_down(self, w):
        device = self.audio_devices[0]
        device.set_volume(device.get_volume() - 5)
        self.update_graph()

    def delta_input_up(self, w):
        device = self.audio_devices[1]
        device.set_volume(device.get_volume() + 5)
        self.update_graph()

    def delta_input_down(self, w):
        device = self.audio_devices[1]
        device.set_volume(device.get_volume() - 5)
        self.update_graph()
    # Update Graph View

    def update_graph(self, force_update=True):
        l = []
        for index, device in enumerate(self.audio_devices):
            volume = device.volume
            # toggle between two bar types
            if index & 1:
                l.append([0, volume])
            else:
                l.append([volume, 0])
        self.graph.set_data(l, 100)
        return True
    # Controls on the right hand side

    def graph_controls(self):
        l = []
        l.append(urwid.Text("Device Select", align="left"))
        l.append(urwid.Divider())
        l.append(self.button("{} +".format('Output'), self.delta_output_up))
        l.append(self.button("{} -".format('Output'), self.delta_output_down))
        l.append(urwid.Divider())
        l.append(self.button("{}  +".format('Input'), self.delta_input_up))
        l.append(self.button("{}  -".format('Input'), self.delta_input_down))
        l.append(urwid.Divider())
        l.append(self.button("Quit", self.exit_program))
        w = urwid.ListBox(urwid.SimpleListWalker(l))
        return w
    # Configuration of the Main Window, combines controls and bar display

    def main_window(self):
        self.graph = self.bar_graph()
        self.graph_wrap = urwid.WidgetWrap(self.graph)
        vline = urwid.AttrWrap(urwid.SolidFill(u'\u2502'), 'line')
        c = self.graph_controls()
        w = urwid.Columns([('weight', 1, self.graph_wrap),
                           ('fixed', 1, vline), c],
                          dividechars=1, focus_column=2)
        w = urwid.Padding(w, ('fixed left', 1), ('fixed right', 1))
        return w

# Class VolumeController, serves as a view Controller


class VolumeController:
    """
    A class responsible for setting up the model and view and running
    the application.
    """

    def __init__(self):
        self.model = VolumeModel()
        self.view = VolumeView(self)
        self.view.update_graph(True)

    def get_audio_devices(self):
        return self.model.get_audio_devices()

    def main(self):
        self.loop = urwid.MainLoop(self.view, self.view.palette)
        self.loop.run()

# Initialize the VolumeController


def main():
    # Command line Argument Parameters
    parser = argparse.ArgumentParser(description=description_string)
    parser.add_argument('-d', '--device', type=str,
                        help='Break Interval (minutes)', required=False)
    parser.add_argument('-v', '--volume', type=int,
                        help='Volume Level', required=False)
    args = parser.parse_args()

    # User specified a device, but no volume setting, they want info
    if args.device is not None and args.volume is None:
        device = args.device
        if "output" == device:
            print VolumeModel().get_audio_devices()[0].get_volume()
        if "input" == device:
            print VolumeModel().get_audio_devices()[1].get_volume()

    # Volume specified without a device specified, assume they want to change
    # output
    if args.volume is not None and args.device is None:
        volume = args.volume
        device = VolumeModel().get_audio_devices()[0]
        device.set_volume(volume)
        print device.get_volume()

    # User specified volume and device
    if args.volume is not None and args.device is not None:
        device = args.device
        volume = args.volume
        # Assign device to correct device object
        if "output" == device:
            device = VolumeModel().get_audio_devices()[0]
        if "input" == device:
            device = VolumeModel().get_audio_devices()[1]
        device.set_volume(volume)
        print device.get_volume()

    # Execute GUI if no command line arguments passed
    if args.device is None and args.volume is None:
        VolumeController().main()

# If Called from the command line
if __name__ == "__main__":
    main()

##########################################################################
# Shell Commands to Change the Volume (This program executes/wraps these commands)
##########################################################################
# Src: https://coderwall.com/p/22p0ja/set-get-osx-volume-mute-from-the-command-line
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
