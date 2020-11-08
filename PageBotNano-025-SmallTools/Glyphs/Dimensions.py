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

		radius = 30
		
		metrics = self.getMetrics(layer)
		#print(metrics['stems'])
		y = -300
		for pair in metrics['stems']:
			for x in pair:
				point = NSPoint(x-radius, y-radius)
				NSColor.redColor().set()
				rect = NSRect(point, (radius*2, radius*2))
				bezierPath = NSBezierPath.bezierPathWithOvalInRect_(rect)
				bezierPath.stroke()
			
		x = -300
		for pair in metrics['bars']:
			for y in pair:
				point = NSPoint(x-radius, y-radius)
				NSColor.redColor().set()
				rect = NSRect(point, (radius*2, radius*2))
				bezierPath = NSBezierPath.bezierPathWithOvalInRect_(rect)
				bezierPath.stroke()
			
		#print('Verticals', metrics['verticals'])
		#print('Horizontals', metrics['horizontals'])
		# Do something here to show the metrics in the EditorWindow
		#print(layer.parent.name, layer.name, layer.width, metrics)
		if 0:
			print("drawbackground")
			print("layer: %s" % layer)
			radius = 30
			for contour in layer.paths:
				for p in contour.nodes:
					#print(p.x, p.y, p.type)
					point = NSPoint(p.x-radius, p.y-radius)
					NSColor.redColor().set()
					rect = NSRect(point, (radius*2, radius*2))
					bezierPath = NSBezierPath.bezierPathWithOvalInRect_(rect)
					bezierPath.stroke()
			#for dictKey in info.keys():
			#    print("   info > %s: %s" % ( dictKey, info[dictKey] ))

		#Layer.completeBezierPath
		#displayText = NSAttributedString.alloc().initWithString_attributes_(text, fontAttributes)
		#displayText.drawAtPoint_((10,10))				
		if 0:
			path = NSBezierPath.bezierPath()
			path.moveToPoint_((100+random()*10, 100+random()*10))
			path.lineToPoint_((500+random()*10, 100+random()*10))
			path.lineToPoint_((300+random()*10, 400+random()*10))
			path.closePath()
			path.setLineWidth_(10)
			NSColor.greenColor().set()
			path.stroke()
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
		
	# Glyph analyser code starts
	def findDefaults(self, layer):
		"""Try to guess the default stem and bar from the /H with the
		following strategy:
		- Find all verticals, then the smallest distance between
		the longest verticals is likely to be a stem.
		- Find all horizontals, then the distance between the 
		longest horizontals is likely to be a bar.
		With this approach we cancel out any verticals or horizontals
		that are part of serifs.
		Note that for now this approach only works with romans, as
		we'll just compare x-values to decide if a line is vertical.

		Once we have guessed the stem and bar for this layer, it is 
		easier to detect them in all other glyphs.
		"""
		stem = bar = 0
		if layer.parent.name != 'H':
			layer = layer.parent.parent.glyphs['H'].layers[layer.name]
			pcs, verticals, horizontals = self.findVerticalsHorizontals(layer)
			# Find the smallest (x1, x2) for the longest two verticals
			v1 = v2 = None # Keep track of longest verticals with the smallest x
			x1 = x2 = 1000000
			for x, pairs in verticals.items():
				for p, p1 in pairs: # Multiple vertical can be on the same x position
					v = abs(p.y - p1.y)
					if v1 is None or v >= v1:
						v1 = v
						x1 = min(x, x1)
					elif v2 is None or v >= v2:
						v2 = v
						x2 = min(x, x2)
			stem = abs(x1 - x2)
			
			# Find the smallest (y1, y2) combination of horizontals
			y1 = 0
			y2 = 1000000
			for y, pairs in horizontals.items():
				if y1 is None:
					y1 = y
				elif y2 is None:
					y2 = y
				elif 0 < abs(y1 - y) < abs(y1 - y2):
					y2 = y
				elif 0 < abs(y2 - y) < abs(y1 - y2):
					y1 = y
			bar = abs(y1 - y2)
		return stem, bar
		
	LO_MARGIN = 0.6
	HI_MARGIN = 1.4
	def findStems(self, verticals, defaultStem):
		# Looking for stems
		stems = [] # Key (x1, x2), value is [p, p, p, ...]
		def1 = defaultStem * self.LO_MARGIN
		def2 = defaultStem * self.HI_MARGIN
		for x1 in sorted(verticals.keys()): # Just need to know the x values now
			for x2 in sorted(verticals.keys()):
				if x1 <= x2: # Skip mirrors and identical x values
					continue
				if def1 <= abs(x1 - x2) <= def2:
					stems.append((x1, x2))
		return stems

	def findBars(self, horizontals, defaultBar):
		# Looking for stems
		bars = [] # Key (x1, x2), value is [p, p, p, ...]
		def1 = defaultBar * self.LO_MARGIN
		def2 = defaultBar * self.HI_MARGIN
		for y1 in sorted(horizontals.keys()): # Just need to know the y values now
			for y2 in sorted(horizontals.keys()):
				if y1 <= y2: # Skip mirrors and identical y values
					continue
				if def1 <= abs(y1 - y2) <= def2:
					bars.append((y1, y2))
		return bars

	def findVerticalsHorizontals(self, layer):
		"""Answer the dictionary verticals and horizontals, where the key is respectively
		the x and y position of the line and the value is a list of (p, p1) pairs
		for the vertical or horizontal on that position (since, e.g. as in the /H there
		can be multiple verticals on the same x position.
		"""
		pcs = [] # List of point context tuples [(p_2, p_1, p, p1, p2), ...] 
		verticals = {} # Key is horizontal position, value is list [(p, p1), ...]
		horizontals = {} # Key is vertical position, value is [(p, p1), ...]
		#diagonals = []
		for contour in layer.paths:
			points = list(contour.nodes)
			for i in range(len(points)):
				# (p-2, p-1, p, p+1, p+2) <---- [p,   p, p, p, p, p, p, ..., p]
				#                                i-1  i                      i-2
				p_2, p_1, p, p1, p2 = points[i-4], points[i-3], points[i-2], points[i-1], points[i]
				pcs.append((p_2, p_1, p, p1, p2))
				if p.x == p1.x:
					if not p.x in verticals:
						verticals[p.x] = []
					verticals[p.x].append((p, p1))
				if p.y == p1.y:
					if not p.y in horizontals:
						horizontals[p.y] = []
					horizontals[p.y].append((p, p1))
		return pcs, verticals, horizontals
		
	def getMetrics(self, layer):
		# Find the stem and bar in the /H glyph of the layer parent font.
		defaultStem, defaultBar = self.findDefaults(layer)
		# Layer is a GlyphsApp glyph style
		pcs, verticals, horizontals = self.findVerticalsHorizontals(layer)
		# Looking for stems, using the defaultStem, as found in /H as reference.
		stems = self.findStems(verticals, defaultStem)	
		# Looking for bars, using the defaultBar, as found in /H, as reference.
		bars = self.findBars(horizontals, defaultBar)
		# Later: looking for diagonals
		
		metrics = dict(pcs=pcs, verticals=verticals, horizontals=horizontals, stems=stems, bars=bars)
		return metrics
				
	
DimensionsTool()