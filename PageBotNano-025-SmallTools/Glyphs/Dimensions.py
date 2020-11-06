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
			
		#print('Verticals', metrics['verticals'])
		#print('Horizontals', metrics['horizontals'])
		# Do something here to show the metrics in the EditorWindow
		#print(layer.parent.name, layer.name, layer.width, metrics)
		if 0:
			print("drawbackground")
			print("   layer: %s" % layer)
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
	def getMetrics(self, layer):
		# Layer is a GlyphsApp glyph style
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
				
		# Looking for stems
		stems = [] # Key (x1, x2), value is [p, p, p, ...]
		stemx1 = stemx2 = None
		for x, pairs in sorted(verticals.items()):
			for p, p1 in pairs:
				if stemx1 is None:
					stemx1 = x
				elif stemx2 is None:
					stemx2 = x
				if not None in (stemx1, stemx2):
					stems.append((stemx1, stemx2))
					stemx1 = stemx2 = None
			
		# Looking for bars
		bars = {}
		# Later: looking for diagonals
		
		metrics = dict(pcs=pcs, verticals=verticals, horizontals=horizontals, stems=stems, bars=bars)
		return metrics
				
	
DimensionsTool()