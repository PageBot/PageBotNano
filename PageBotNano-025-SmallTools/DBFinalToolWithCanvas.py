import importlib, os, codecs, traceback
from vanilla import Window, CheckBox, Button, Slider, RadioGroup, EditText, List
from vanilla.dialogs import getFolder

from pagebotnano_025.canvas import Canvas
from AppKit import NSMakeRect, NSColor, NSBezierPath
from pagebotnano_025.colors import rgba

import FixTabWidths
importlib.reload(FixTabWidths)
from FixTabWidths import fixTabWidths

import FixNegativeWidths
importlib.reload(FixNegativeWidths)
from FixNegativeWidths import fixNegativeWidths

import FixMissingComponent
importlib.reload(FixMissingComponent)
from FixMissingComponent import fixMissingComponent


import os, codecs
# Include the openFont function here, instead of the import, in case this
# script is not running inside the current folder.
from pagebotnano_025 import openFont 

TESTING = False
DEFAULT_WIDTH = 111
PATH = 'masters/' # Check all .ufo in this local folder
REPORT_PATH = 'reports/' # Create folder if not exists, export report file there.


class DBFinalTool:
    def __init__(self):
        self.glyph = None # Typical RoboFont function
        self.updating = False
        
        pad = 10
        leading = 32
        y = pad
        w = 500
        h = 500
        c1 = 150
        c2 = 200
        bh = 24 # Button height
        leading = bh + pad/2
        
        self.w = Window((100, 100, w, h), 'Final tool window',
            minSize=(w, h))
        self.w.fontList = List((pad, pad, c2, -w/2), [], 
            doubleClickCallback=self.openFontCallback,
            selectionCallback=self.update)
        
        y = pad
        self.w.fixTabWidths = Button((-c1-pad, y, c1, bh), 
            'Fix tab widths', callback=self.fixTabWidthsCallback)  
        self.w.fixTabWidths.enable(False)
        
        y += leading            
        self.w.fixNegativeWidths = Button((-c1-pad, y, c1, bh), 
            'Fix negative widths', callback=self.fixNegativeWidthsCallback)  
        self.w.fixNegativeWidths.enable(False)

        y += leading            
        self.w.fixMissingComponentsWidths = Button((-c1-pad, y, c1, bh), 
            'Fix missing components', callback=self.fixMissingComponentCallback)  
        self.w.fixMissingComponentsWidths.enable(False)
                     
        self.w.selectFolder = Button((-c1-pad, -pad-bh, c1, bh), 
            'Select fonts', callback=self.selectFontFolder)           

        self.w.canvas = Canvas((pad, -w/2-pad, -pad, -w/4), delegate=self)

        self.w.report = EditText((pad, -w/4+pad, -pad, -pad),
            readOnly=False)
        
        self.w.bind('close', self.windowCloseCallback)
        self.w.open()

        self.dirPath = self.selectFontFolder()

    # Handle events from the Canvas
    def draw(self, rect): # Drawing delegate from the Canvas drawing evening
        for n in range(50):
            rgba(random(), random(), random()).set()
            rect = NSMakeRect(random()*400+M, random()*400+M, M, M)
            path = NSBezierPath.bezierPathWithRect_(rect)
            path.fill()
    
    # Callback from controls in our own window.
    def update(self, sender):
        """Do some UI status update work"""
        enable = len(self.w.fontList.getSelection()) > 0    
        self.w.fixTabWidths.enable(enable)
        self.w.fixMissingComponentsWidths.enable(enable)
        self.w.fixNegativeWidths.enable(enable)
    
    def openFontCallback(self, sender):
        selectedFonts = []
        for index in self.w.fontList.getSelection():
            selectedFonts.append(self.w.fontList.get()[index])
        # Do something here with the fonts after double click
        # Open in RoboFont of Glyphs
        cmd = 'open'
        for selectedFont in selectedFonts:
            cmd += ' '+self.dirPath + selectedFont
        self.report(cmd)
        #os.system(cmd)
    
    def selectFontFolder(self, sender=None):
        result = getFolder(
            messageText='Select fonts folder', 
            title='Select', 
            allowsMultipleSelection=False)
        if result:
            path = result[0]
            fontNames = []
            for filePath in os.listdir(path):
                if filePath.startswith('.') or not filePath.endswith('.ufo'):
                    continue
                fontNames.append(filePath)
            self.w.fontList.set(fontNames)
            return path + '/'
        return None
    
    def fixTabWidthsCallback(self, sender):
        self.clearReport()
        for index in self.w.fontList.getSelection():
            fontFile = self.w.fontList.get()[index]
            result = fixTabWidths(self.dirPath + fontFile )
            self.report('\n'.join(result))
            #self.report(self.dirPath )
            self.report('Done %s' % fontFile)
    
    def fixNegativeWidthsCallback(self, sender):
        self.clearReport()
        for index in self.w.fontList.getSelection():
            fontFile = self.w.fontList.get()[index]
            try:
                result = fixNegativeWidths(self.dirPath + fontFile )
                self.report('\n'.join(result))
            except:
                f = open(self.dirPath+'error.txt', 'w')
                traceback.print_exc(file=f)
                f.close()           
            self.report('Done %s\n' % fontFile)

    def fixMissingComponentCallback(self, sender):
        self.clearReport()
        for index in self.w.fontList.getSelection():
            fontFile = self.w.fontList.get()[index]
            result = fixMissingComponent(self.dirPath + fontFile )
            self.report('\n'.join(result))
            #self.report(self.dirPath )
            self.report('Done %s\n' % fontFile)
                                
    def windowCloseCallback(self, sender):
        self.report('removeObservers')
    
    def clearReport(self):
        self.w.report.set('')
        
    def report(self, report):
        s = self.w.report.get()
        if s:
            s += '\n'
        self.w.report.set(s + str(report))
        #f = codecs.open('./report.txt', 'a', encoding='utf-8')
        #f.write(report+'\n')
        #f.close() 
                 
DBFinalTool()
        