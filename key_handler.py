#!/usr/bin/python

# key_handler fetch input from the keyboard and tell which key is pressed
import sys, tty, termios
from dir_codes import *

ARROW_CODES = {
    "A": UP,
    "B": DOWN,
    "D": LEFT,
    "C": RIGHT,
}
WASD_CODES = {
    "w": UP,
    "s": DOWN,
    "a": LEFT,
    "d": RIGHT,
    "W": UP,
    "S": DOWN,
    "A": LEFT,
    "D": RIGHT,
}

code = STOP
dirty = False

kill = False

def keypress():
    global kill, code, dirty
    print "Press 'q' or 'CTRL + C' to terminate the program..."
    ch = " "

    while not kill:        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setraw(fd)
        ch = sys.stdin.read(1) # BLOCKING CALL, WAITS FOR NEXT CHARACTER INPUT (INCLUDING HELD DOWN KEY)
        if ord(ch) == 27: # first char of arrows special code
            ch = sys.stdin.read(1)
            if ord(ch) == 91: # second char of arrows special code
                ch = sys.stdin.read(1)
                if ch in ARROW_CODES.keys(): #third char of arrows special code
                    code = ARROW_CODES[ch]
                    dirty = True
        elif ch in WASD_CODES.keys(): # char for wasd code
            code = WASD_CODES[ch]
            dirty = True
        elif ch == "q" or ord(ch) == 3: # terminate thread
            kill = True
        else:
            code = STOP
            dirty = True
        
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        print code



if __name__ == "__main__":
    keypress()
