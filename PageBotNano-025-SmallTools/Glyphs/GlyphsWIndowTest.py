#
# Run this as Glyphs macro
#
# Get the current open font object
#
from vanilla import Window, CheckBox, Slider, Button, EditText

DEFAULT_MARGIN = 80

MIN_LSB = -200
MAX_LSB = 400

class DemoWindowTool:
    def __init__(self):
        self.font = Glyphs.font # Returns the current that is open in GlyphsApp
        self.glyph = self.font['H'].layers[0]
        lsb = int(round(self.glyph.LSB))
        
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
        self.w.leftMarginSlider = Slider((pad, y, -pad-60, 24), 
            minValue=MIN_LSB, maxValue=MAX_LSB, value=lsb, 
            tickMarkCount=10, callback=self.leftMarginSliderCallback)   
        self.w.leftMarginBox = EditText((-pad-60+pad, y, -pad, 24), callback=self.leftMarginBoxCallback)
        self.w.leftMarginBox.set(str(lsb))  
            
                
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
        
    def leftMarginBoxCallback(self, sender):
        try:
            if sender.get():
                lsb = int(sender.get())
                lsb = max(lsb, MIN_LSB) # Compare max(lsb = -1000, MIN_LSB = -200)
                lsb = min(lsb, MAX_LSB) # Compare min(lsb = 1000, MAX_LSB = 400)
                self.w.leftMarginSlider.set(lsb)
        except ValueError:
            print('Value is not an number: %s' % sender.get())
        
        
        
DemoWindowTool()    