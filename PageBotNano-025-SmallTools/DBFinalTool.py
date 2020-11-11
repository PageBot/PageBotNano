import importlib, os, codecs
from vanilla import Window, CheckBox, Button, Slider, RadioGroup, EditText, List
from vanilla.dialogs import getFolder

import FixTabWidths
importlib.reload(FixTabWidths)
from FixTabWidths import fixTabWidths

import FixNegativeWidth
importlib.reload(FixNegativeWidth)
from FixNegativeWidth import fixNegativeWidth

import FixMissingComponent
importlib.reload(FixMissingComponent)
from FixMissingComponent import fixMissingComponent

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
        self.w.fontList = List((pad, pad, c2, -w/2), [])
        
        y = pad
        self.w.fixTabWidths = Button((-c1-pad, y, c1, bh), 
            'Fix tab widths', callback=self.fixTabWidthsCallback)  
        
        y += leading            
        self.w.fixNegativeWidths = Button((-c1-pad, y, c1, bh), 
            'Fix negative widths', callback=self.fixNegativeWidthsCallback)  
  
        y += leading            
        self.w.fixMissingComponentsWidths = Button((-c1-pad, y, c1, bh), 
            'Fix missing components', callback=self.fixMissingComponentCallback)  
                     
        self.w.selectFolder = Button((-c1-pad, -pad-bh, c1, bh), 
            'Select fonts', callback=self.selectFontFolder)           

        self.w.report = EditText((pad, -w/2+pad, -pad, -pad),
            readOnly=False)
        
        self.w.bind('close', self.windowCloseCallback)
        self.w.open()

        self.dirPath = self.selectFontFolder()
        
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
            result = fixNegativeWidths(self.dirPath + fontFile )
            self.report('\n'.join(result))
            #self.report(self.dirPath )
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
        