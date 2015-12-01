#!/usr/bin/env python
# Imports
import curses 

# Global Variables
screen = None;
dimensions = None;

# Main Input Loop
def main():
    global screen
    global dimensions
    # Disable output to terminal
    screen = curses.initscr()
    curses.noecho()
    screen.immedok(True)
    screen.border(0)
    screen.addstr("System Volume Control")
    dimensions = screen.getmaxyx()

    # Main Input Loop
    user_input = None
    while user_input != 7:
        draw_bars()
        screen.getch()

    # Break out of main loop, end program
    curses.endwin()

def draw_bars():
    box1 = curses.newwin(dimensions[0]-10, dimensions[1]-10, 10, 10)
    box1.immedok(True)
    
    box1.box()    
    box1.addstr("System Volume")

if __name__ == "__main__":
    main()


# from subprocess import call
# call(["ls", "-l"])

# osascript -e "set Volume 0"

# osascript -e 'set ovol to output volume of (get volume settings)'

