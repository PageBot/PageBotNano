import importlib
from vanilla import Window, FloatingWindow, CheckBox, Button, Slider, RadioGroup

import FixTabWidths
importlib.reload(FixTabWidths)
from FixTabWidths import fixTabWidths

class DBFinalTool:
    def __init__(self):
        self.glyph = None # Typical RoboFont function
        self.updating = False
        
        pad = 10
        leading = 32
        y = pad
        w = 300
        h = 400
        buttonWidth = 100
        buttonHeight = 48
        
        self.w = Window((100, 100, w, h), 'Final tool window')
                    
        self.w.bind('close', self.windowCloseCallback)
        self.w.open()
        
    def windowCloseCallback(self, sender):
        print('removeObservers')
                 
DBFinalTool()
        