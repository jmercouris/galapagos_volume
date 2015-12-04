#!/usr/bin/env python
# Imports
import os
import subprocess
import urwid
# Represents an OSX audio device, e.g. input, output
class AudioDevice:
    """
    A class responsible for representing & manipulating OSX audio devices
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

# Represents the Data in the program
class VolumeModel:
    """
    Populating the default OSX AudioDevices
    """
    def __init__(self):
        # List of audio devices
        audio_devices = self.audio_devices = []
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
    def get_audio_devices(self):
        return self.audio_devices

# Class VolumeView, handles drawing and input
class VolumeView(urwid.WidgetWrap):
    """
    A class responsible for providing the application's interface and
    volume display.
    """
    palette = [
        ('bg background','white', 'white'),
        ('bg 1',         'black',      'black', 'standout'),
        ('bg 1 smooth',  'dark blue',  'black'),
        ('bg 2',         'black',      'dark gray', 'standout'),
        ('bg 2 smooth',  'dark gray',  'black'),
        ('button normal','black', 'white', 'light gray'),
        ('button select','white',      'black'),
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
            satt = {(1,0): 'bg 1 smooth', (2,0): 'bg 2 smooth'}
        w = urwid.BarGraph(['bg background','bg 1','bg 2'], satt=satt)
        return w
    def button(self, t, fn):
        w = urwid.Button(t, fn)
        w = urwid.AttrWrap(w, 'button normal', 'button select')
        return w
    # Exit Program
    def exit_program(self, w):
        raise urwid.ExitMainLoop()
    # Update Graph View
    def update_graph(self, force_update=False):
        l = []
        for index, device in enumerate(self.audio_devices):
            volume = device.get_volume()
            # toggle between two bar types
            if index & 1:
                l.append([0,volume])
            else:
                l.append([volume,0])
        self.graph.set_data(l,100)
    # Controls on the right hand side
    def graph_controls(self):
        l = [
            urwid.Text("Device Select",align="left"),
            urwid.Divider(),]
        
        for device in self.audio_devices:
            l.append(self.button("{}  Volume:+".format(device.name), self.exit_program))
            l.append(self.button("{}  Volume:-".format(device.name), self.exit_program))
            l.append(urwid.Divider())
            
        l.append(self.button("Quit", self.exit_program ))
            
        w = urwid.ListBox(urwid.SimpleListWalker(l))
        return w
    # Configuration of the Main Window
    def main_window(self):
        self.graph = self.bar_graph()
        self.graph_wrap = urwid.WidgetWrap( self.graph )
        vline = urwid.AttrWrap( urwid.SolidFill(u'\u2502'), 'line')
        c = self.graph_controls()
        w = urwid.Columns([('weight',2,self.graph_wrap),
            ('fixed',1,vline), c],
            dividechars=1, focus_column=2)
        w = urwid.Padding(w,('fixed left',1),('fixed right',0))
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
    VolumeController().main()
# If Called from the command line
if __name__ == "__main__":
    main()

################################################################################
# Shell Commands to Change the Volume (This program executes these commands)
################################################################################
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
