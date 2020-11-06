#MenuTitle: CallBack Test
# -*- coding: utf-8 -*-
__doc__="""
Do several adjustments to the font and current glyph.
"""
from AppKit import *
from drawBot import *
import vanilla
from vanilla import EditText, TextBox, Button, CheckBox, TextEditor
from random import random

class DimensionsTool:
    def __init__( self ):
        # Window 'self.w':
        w  = 300
        h = 300
        windowWidthResize  = 200 # user can resize width by this value
        windowHeightResize = 500   # user can resize height by this value
        self.w = vanilla.FloatingWindow(
            (w, h ), # default window size
            "Dimensions", # window title
            minSize = ( w, h-100 ), # minimum size (for resizing)
            maxSize = ( w + windowWidthResize, h + windowHeightResize ), # maximum size (for resizing)
            autosaveName = "com.typetr.Dimensions.mainwindow" # stores last window position and size
        )
        M = 10
        y = 30
        # UI elements:
        self.w.tabWidth = EditText( (M, y, w/4-M-M, 20), "650", sizeStyle='small' )
        self.w.tabWidthLabel = TextBox( (w/4, y+4, w/2, 20), "Tab width", sizeStyle='small' )
        
        y += 30
        # Run Button:
        self.w.doFix = CheckBox((M, y, -M, 24), "Fix errors", value=False, sizeStyle='regular' )
                
                   
        # Open window and focus on it:
        self.w.bind('close', self.windowCloseCallback)
        self.w.open()
        self.w.makeKey()
        
        # establish callbacks:
        
        Glyphs.addCallback( self.drawforeground, DRAWFOREGROUND )
        Glyphs.addCallback( self.drawbackground, DRAWBACKGROUND )
        

    def windowCloseCallback(self, sender):
        self.removeCallbacks()
        print('removeObserver currentGlyphChanged')
    
    def drawforeground(self, layer, info):
        if 0:
            print "drawforeground"
            print "   layer: %s" % layer
            for dictKey in info.keys():
                print "   info > %s: %s" % ( dictKey, info[dictKey] )
            

        #fill(1, 1, 0)
        #rect(50, 50, 300, 300)
                
    def drawbackground(self, layer, info):
        if 0:
            print "drawbackground"
            print "   layer: %s" % layer
            for dictKey in info.keys():
                print "   info > %s: %s" % ( dictKey, info[dictKey] )
        """
        for n in range(20):
            point = NSPoint(500*random(), 500*random())
            NSColor.redColor().set()
            rect = NSRect(point, (100, 100))
            bezierPath = NSBezierPath.bezierPathWithOvalInRect_(rect)
            bezierPath.fill()
        """ 
       
    def cleanUp(self, sender):
        self.removeCallbacks()
        print sender
        
    def removeCallbacks(self):
        Glyphs.removeCallback( self.drawforeground, DRAWFOREGROUND )
        Glyphs.removeCallback( self.drawbackground, DRAWBACKGROUND )
    
    def showWindow(self, sender):
        # brings macro window to front and clears its log:
        Glyphs.clearLog()
        Glyphs.showMacroWindow()
        print sender
        
DimensionsTool()