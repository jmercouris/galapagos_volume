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
        audio_devices = self.audio_devices = []
        
        # AudioDevice Output
        get_volume_command = ['osascript', '-e', 'output volume of (get volume settings)']
        set_volume_command = ['osascript', '-e', 'set volume output volume {}']
        device = AudioDevice("Output", set_volume_command, get_volume_command)
        audio_devices.append(device)
        device.set_volume(60)
        
        # AudioDevice Input
        get_volume_command = ['osascript', '-e', 'input volume of (get volume settings)']
        set_volume_command = ['osascript', '-e', 'set volume input volume {}']
        device = AudioDevice("Input", set_volume_command, get_volume_command)
        audio_devices.append(device)
        
    def get_audio_devices(self):
        return self.audio_devices

class VolumeView(urwid.WidgetWrap):
    """
    A class responsible for providing the application's interface and
    volume display.
    """
    
    palette = [
        ('body',         'black',      'light gray', 'standout'),
        ('header',       'white',      'dark red',   'bold'),
        ('screen edge',  'light blue', 'dark cyan'),
        ('main shadow',  'dark gray',  'black'),
        ('line',         'black',      'light gray', 'standout'),
        ('bg background','light gray', 'black'),
        ('bg 1',         'black',      'dark blue', 'standout'),
        ('bg 1 smooth',  'dark blue',  'black'),
        ('bg 2',         'black',      'dark cyan', 'standout'),
        ('bg 2 smooth',  'dark cyan',  'black'),
        ('button normal','light gray', 'dark blue', 'standout'),
        ('button select','white',      'dark green'),
        ('line',         'black',      'light gray', 'standout'),
        ('pg normal',    'white',      'black', 'standout'),
        ('pg complete',  'white',      'dark magenta'),
        ('pg smooth',     'dark magenta','black')
        ]

    def __init__(self, controller):
        self.controller = controller
        self.audio_devices = self.controller.get_audio_devices()
        urwid.WidgetWrap.__init__(self, self.main_window())
        
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
        
    def exit_program(self, w):
        raise urwid.ExitMainLoop()
        
    def update_graph(self, force_update=False):
        l = []
        for n in range(10):
            value = n
            # toggle between two bar types
            if n & 1:
                l.append([0,value])
            else:
                l.append([value,0])
        self.graph.set_data(l,10)
        
    def graph_controls(self):
        l = [
            urwid.Divider(),
            urwid.Text("Device",align="center"),
            urwid.Divider(),
            self.button("Input", self.exit_program ),
            self.button("Output", self.exit_program ),
            self.button("Quit", self.exit_program ),
            ]
        w = urwid.ListBox(urwid.SimpleListWalker(l))
        return w
        
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
