from pynput.keyboard import Listener, Key
import sys

class inputUser:
    def __init__(self, is2player):
        self.is2player = is2player
        self.w = False
        self.s = False
        self.u = False
        self.d = False
        self.run()

    def on_press(self, key):
        if len(str(key)) == 3:
            print("\b ", end="")
        elif len(str(key)) == 6 or len(str(key)) == 8:
            print("\b\b\b\b    ", end="")
        if len(str(key)) == 3 and key.char == "w" and not self.w:
            self.w = True
        elif len(str(key)) == 3 and key.char == "s" and not self.s:
            self.s = True
        elif len(str(key)) == 6 and key == Key.up and not self.u and self.is2player:
            self.u = True
        elif len(str(key)) == 8 and key == Key.down and not self.d and self.is2player:
            self.d = True

    def on_release(self, key):
        if len(str(key)) == 3: # replace char by space
            print("\b ", end="")
        elif len(str(key)) == 6 or len(str(key)) == 8:
            print("\b\b\b\b    ", end="")
        if len(str(key)) == 3 and key.char == "w" and self.w:
            self.w = False
        elif len(str(key)) == 3 and key.char == "s" and self.s:
            self.s = False
        elif len(str(key)) == 6 and key == Key.up and self.u and self.is2player:
            self.u = False
        elif len(str(key)) == 8 and key == Key.down and self.d and self.is2player:
            self.d = False
        
    def run(self):
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()


inputUser(True)