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
    screen = curses.initscr()
    screen.immedok(True)
    screen.border(0)
    screen.addstr("System Volume Control")
    dimensions = screen.getmaxyx()
    draw_bars()
    screen.getch()
    curses.endwin()

def draw_bars():
    box1 = curses.newwin(dimensions[0]-10, dimensions[1]-10, 10, 10)
    box1.immedok(True)
    
    box1.box()    
    box1.addstr("System Volume")

if __name__ == "__main__":
    main()
