
from vanilla import Window, FloatingWindow, CheckBox, Button, Slider, RadioGroup
from mojo.events import addObserver, removeObserver # Typical RoboFont Event handling
from mojo.drawingTools import fill, stroke, rect, oval, text
from mojo.UI import UpdateCurrentGlyphView

class DemoWindowTool:
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
        
        self.w = FloatingWindow((100, 100, w, h), 'DemoWindowTool')
        self.w.doDraw = CheckBox((pad, y, 100, 24), 'Draw', callback=self.doDrawCallback)
        y += leading
        self.w.mySlider = Slider((pad, y, -pad, 24), minValue=0, maxValue=2000, value=0, 
            tickMarkCount=10, callback=self.mySliderCallback)
        y = self.w.saveFont = Button((-buttonWidth-pad, -buttonHeight-pad, buttonWidth, buttonHeight), 
            'Save', callback=self.saveFontCallback)
            
        addObserver(self, "currentGlyphChanged", "currentGlyphChanged") # Subscribe to application event
        addObserver(self, 'draw', 'draw')
        addObserver(self, 'drawBackground', 'drawBackground')
        
        self.w.bind('close', self.windowCloseCallback)
        self.w.open()
        
    def windowCloseCallback(self, sender):
        removeObserver(self, "currentGlyphChanged") # Unsubscribing from application event
        removeObserver(self, 'draw')
        removeObserver(self, 'drawBackground')
        print('removeObserver currentGlyphChanged')
        
    def mySliderCallback(self, sender):
        if self.glyph is not None:
            self.glyph.width = sender.get() # same as self.w.mySlider  
            self.updating = True  
            self.glyph.changed()
            UpdateCurrentGlyphView()
            self.updating = False
    
    def doDrawCallback(self, sender):
        UpdateCurrentGlyphView()
                
    def saveFontCallback(self, sender):
        print('Saving') 
    
    def draw(self, info):
        #print('Drawing' ,info['glyph'])
        if not self.updating:
            glyph = info['glyph']
            self.w.mySlider.set(glyph.width)
        if self.w.doDraw.get():
            fill(1, 0, 0, 0.5)
            rect(0, 0, glyph.width, 50)
        
    def drawBackground(self, info):
        #print('Drawing' ,info['glyph'])
        if not self.updating:
            glyph = info['glyph']
            self.w.mySlider.set(glyph.width)
        if self.w.doDraw.get():
            fill(0, 0, 1, 0.5)
            rect(0, 0, glyph.width, 50)
        
    #def glyphChanged(self, info):
    #    print('Glyph changed', info['glyph'])
        
    def currentGlyphChanged(self, info):
        #if self.glyph is not None:
        #    self.glyph.removeObserver(self, 'Glyph.Change')
        self.glyph = info['glyph']
        #self.glyph.addObserver(self, 'glyphChanged', 'Glyph.Change')
        #print('Glyph', info['glyph'], 'changed')
            
DemoWindowTool()
        