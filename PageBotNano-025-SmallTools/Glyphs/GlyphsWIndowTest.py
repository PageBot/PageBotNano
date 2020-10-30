#
# Run this as Glyphs macro
#
# Get the current open font object
#
from vanilla import Window, CheckBox, Slider, Button

class DemoWindowTool:
	def __init__(self):
		self.font = Glyphs.font # Returns the current that is open in GlyphsApp
		self.glyph = self.font['H'].layers[0]
		
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
		self.w.mySlider = Slider((pad, y, -pad, 24), minValue=0, maxValue=2000, value=0, 
		    tickMarkCount=10, callback=self.mySliderCallback)		
		y = self.w.saveFont = Button((-buttonWidth-pad, -buttonHeight-pad, buttonWidth, buttonHeight), 
		    'Save', callback=self.saveFontCallback)

		self.w.open()

	def saveFontCallback(self, sender):
		pass
		
	def doDrawCallback(self, sender):
		pass
		
	def mySliderCallback(self, sender):
		#self.glyph.width = sender.get()
		pass
		
DemoWindowTool()	