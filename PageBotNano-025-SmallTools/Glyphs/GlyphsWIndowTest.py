#
# Run this as Glyphs macro
#
# Get the current open font object
#
from vanilla import Window, CheckBox, Slider, Button, EditText, TextBox

DEFAULT_MARGIN = 80

MIN_LSB = MIN_RSB = -200
MAX_LSB = MAX_RSB = 400
LSBS = {
    'H': ('B', 'D', 'E', 'F', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'R'),
    'O': ('C', 'G', 'O', 'Q'),
}
RSBS = {
    'H': ('H', 'I', 'M', 'N'),
    'O': ('D', 'O', 'Q'),
}
class DemoWindowTool:
    def __init__(self):
        self.font = Glyphs.font # Returns the current that is open in GlyphsApp
        self.currentGlyphName = 'H'
        self.glyph = self.font[self.currentGlyphName].layers[0]
        lsb = int(round(self.glyph.LSB))
        rsb = int(round(self.glyph.RSB))
        
        pad = 10
        leading = 32
        y = pad
        w = 300
        h = 400
        buttonWidth = 100
        buttonHeight = 48
        
        self.w = Window((100, 100, w, h), 'DemoWindowTool')
        self.w.doDraw = CheckBox((pad, y, 100, 24), 'Draw', callback=self.doDrawCallback)
        
        y += leading
        self.w.leftMarginLabel = TextBox((pad, y, -pad, 24), 'Left margin')
        y += leading/2
        self.w.leftMarginSlider = Slider((pad, y, -pad-60, 24), 
            minValue=MIN_LSB, maxValue=MAX_LSB, value=lsb, 
            tickMarkCount=10, callback=self.leftMarginSliderCallback)   
        self.w.leftMarginBox = EditText((-pad-60+pad, y, -pad, 24), callback=self.leftMarginBoxCallback)
        self.w.leftMarginBox.set(str(lsb))  
            
        y += leading
        self.w.rightMarginLabel = TextBox((pad, y, -pad, 24), 'Right margin')
        y += leading/2
        self.w.rightMarginSlider = Slider((pad, y, -pad-60, 24), 
            minValue=MIN_RSB, maxValue=MAX_RSB, value=rsb, 
            tickMarkCount=10, callback=self.rightMarginSliderCallback)  
        self.w.rightMarginBox = EditText((-pad-60+pad, y, -pad, 24), callback=self.rightMarginBoxCallback)
        self.w.rightMarginBox.set(str(rsb))  
                
        y = self.w.saveFont = Button((-buttonWidth-pad, -buttonHeight-pad, buttonWidth, buttonHeight), 
            'Save', callback=self.saveFontCallback)

        self.w.open()

    def saveFontCallback(self, sender):
        pass
        
    def doDrawCallback(self, sender):
        pass
        
    def leftMarginSliderCallback(self, sender):
        #self.glyph.width = sender.get()
        lsb = int(round(sender.get()))
        self.w.leftMarginBox.set(str(lsb))
        if self.currentGlyphName in LSBS:
            for gName in LSBS[self.currentGlyphName]:
                self.font[gName].layers[0].LSB = lsb
        else:
            self.glyph.LSB = lsb
        
    def leftMarginBoxCallback(self, sender):
        try:
            if sender.get():
                lsb = int(sender.get())
                lsb = max(lsb, MIN_LSB) # Compare max(lsb = -1000, MIN_LSB = -200)
                lsb = min(lsb, MAX_LSB) # Compare min(lsb = 1000, MAX_LSB = 400)
                self.w.leftMarginSlider.set(lsb)
                if self.currentGlyphName in LSBS:
                    for gName in LSBS[self.currentGlyphName]:
                        self.font[gName].layers[0].LSB = lsb
                else:
                    self.glyph.LSB = lsb
        except ValueError:
            print('Value is not an number: %s' % sender.get())
        
    def rightMarginSliderCallback(self, sender):
        rsb = int(round(sender.get()))
        self.w.rightMarginBox.set(str(rsb))
        print(self.glyph.name, RSBS.keys())
        if self.currentGlyphName in RSBS:
            for gName in RSBS[self.currentGlyphName]:
                self.font[gName].layers[0].RSB = rsb
        else:
            self.glyph.RSB = rsb
        
    def rightMarginBoxCallback(self, sender):
        try:
            if sender.get():
                rsb = int(sender.get())
                rsb = max(rsb, MIN_RSB) # Compare max(rsb = -1000, MIN_RSB = -200)
                rsb = min(rsb, MAX_RSB) # Compare min(rsb = 1000, MAX_RSB = 400)
                self.w.leftMarginSlider.set(rsb)
                if self.currentGlyphName in RSBS:
                    for gName in RSBS[self.currentGlyphName]:
                        self.font[gName].layers[0].RSB = rsb
                else:
                    self.glyph.RSB = rsb
        except ValueError:
            print('Value is not an number: %s' % sender.get())
        
        
DemoWindowTool()    