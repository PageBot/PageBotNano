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

class PointContext:
	def __init__(self, p_2, p_1, p, p1, p2):
		self.p_2 = p_2
		self.p_1 = p_1
		self.p = p
		self.p1 = p1
		self.p2 = p2
		
class Vertical:
	def __init__(self, p, p1):
		# abs(p.x - p1.x) <= TOLERANCE
		assert p.y != p1.y
		self.p = p
		self.p1 = p1		

	def __repr__(self):
		return '<%s x=%d h=%d>' % (self.__class__.__name__, self.x, self.h)

	def _get_x(self):
		return self.p.x
	x = property(_get_x)
			
	def _get_y(self):
		return self.p.y
	y = property(_get_y)
		
	def _get_h(self):
		# Answering the height of the vertical
		return abs(self.p.y - self.p1.y)
	h = property(_get_h)
	
	def _get_isVertical(self):
		return self.p.x == self.p1.x
	isVertical = property(_get_isVertical)
		
class Horizontal:
	def __init__(self, p, p1):
		# abs(p.x - p1.x) <= TOLERANCE
		self.p = p
		self.p1 = p1
	
	def __repr__(self):
		return '<%s y=%d w=%d>' % (self.__class__.__name__, self.y, self.w)
	
	def _get_x(self):
		return self.p.x
	x = property(_get_x)
			
	def _get_y(self):
		return self.p.y
	y = property(_get_y)
		
	def _get_w(self):
		# Answering the width of the horizontal
		return abs(self.p.x - self.p1.x)
	w = property(_get_w)
	
	def _get_isHorizontal(self):
		return self.p.y == self.p1.y
	isHorizontal = property(_get_isHorizontal)

class Diagonal:
	def __init__(self, p, p1):
		self.p = p
		self.p1 = p1

class Stem:
	def __init__(self, v1, v2):
		self.v1 = v1 # Vertical instance
		self.v2 = v2

	def __repr__(self):
		return '<%s x=%d w=%d>' % (self.__class__.__name__, self.x, self.w)
		
	def _get_x(self):
		return min(self.v1.x, self.v2.x)
	x = property(_get_x)
	
	def _get_y(self):
		return min(self.v1.y, self.v2.y)
	y = property(_get_y)
	
	def _get_w(self):
		return abs(self.v1.x - self.v2.x)
	w = property(_get_w)
		
class Bar:
	def __init__(self, h1, h2):
		self.h1 = h1 # Horizontal instance
		self.h2 = h2

	def __repr__(self):
		return '<%s x=%d w=%d>' % (self.__class__.__name__, self.y, self.h)

	def _get_y(self):
		return min(self.h1.y, self.h2.y)
	y = property(_get_y)

	def _get_x(self): # Answer smallest x of the bar.
		return min(self.h1.x, self.h2.x)
	x = property(_get_x)
		
	def _get_h(self):
		return abs(self.h1.y - self.h2.y)
	h = property(_get_h)
	
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
		# UI elements we'll use later
		self.w.tabWidth = EditText( (M, y, w/4-M-M, 20), "650", sizeStyle='small' )
		self.w.tabWidthLabel = TextBox( (w/4, y+4, w/2, 20), "Tab width", sizeStyle='small' )
		
		y += 30
		# Checkbox to flag if any drawing should be done by this tools
		self.w.doDraw = CheckBox((M, y, -M, 24), "Fix errors", value=False, sizeStyle='regular' )
					   
		# Open window and focus on it:
		self.w.bind('close', self.windowCloseCallback) # Make bind in case the window is closed
		self.w.open()
		self.w.makeKey()
		
		# Establish callbacks that we need for this tool
		Glyphs.addCallback( self.drawforeground, DRAWFOREGROUND )
		Glyphs.addCallback( self.drawbackground, DRAWBACKGROUND )
		

	def windowCloseCallback(self, sender):
		"""Called when window is closed, so we can unsubscribe from the GlyphsApp event.
		"""
		self.removeCallbacks()
		#print('removeObserver currentGlyphChanged')
	
	def drawbackground(self, layer, info):
		"""Called if GlyphsApp is redrawing in the background of the window (under the glyph).
		"""
		# Currently we have nothing to draw on the background.
	
	def drawLabel(self, label, x, y, sc):
		textColor = NSColor.textColor()
		point = NSPoint(x, y)
		attributes = {
			NSFontAttributeName: NSFont.labelFontOfSize_(10/sc),
			NSForegroundColorAttributeName: textColor,
		}
		NSString.stringWithString_(label).drawAtPoint_withAttributes_(point, attributes)
		
	def drawforeground(self, layer, info):
		"""Called if GlyphsApp is redrawing in the foreground of the window (over the glyph).
		"""
		# Current drawing scale, so we can reverse scale arrow heads and markers
		# to keep them at constant size.
		sc = info['Scale'] 
		arrowSize = 3 / sc # Reversed-scaled radius of the marker circles
		
		# Try to find a ranges of metrics, interpreting directly from the points.
		# For this the metrics of the /H is searched first, so we can compare it 
		# with raw verticals and horizontals of the current glyph. Stems/bars that
		# in a 60% - 140% range (self.LO_MARGIN, self.HI_MARGIN factors) are assumed 
		# to be stems or bars. Currently only
		metrics = self.getMetrics(layer)
		#print(metrics)
		
		y = -250 # Below baseline, could be related to the descender of the glyph
 		for x, stem in metrics['stems'].items(): # x1 is smallest-left, x2 is largest-right
			path = NSBezierPath.bezierPath()
 			x1 = stem.x
 			x2 = x1 + stem.w
 			# Horizontal measure line
			path.moveToPoint_((x1, y))
			path.lineToPoint_((x2, y))
			# Arrow head left
			path.moveToPoint_((x1+arrowSize*2, y+arrowSize))
			path.lineToPoint_((x1, y))
			path.lineToPoint_((x1+arrowSize*2, y-arrowSize))
			# Arrow head right
			path.moveToPoint_((x2-arrowSize*2, y+arrowSize))
			path.lineToPoint_((x2, y))
			path.lineToPoint_((x2-arrowSize*2, y-arrowSize))
			
			path.setLineWidth_(1/sc)
			NSColor.darkGrayColor().set()
			path.stroke()

			# Vertical lines to points
			path = NSBezierPath.bezierPath()
			path.moveToPoint_((x1, y-8))
			path.lineToPoint_((x1, stem.y))
			path.moveToPoint_((x2, y-8))
			path.lineToPoint_((x2, stem.y))

			path.setLineWidth_(0.5/sc)
			NSColor.lightGrayColor().set()
			path.stroke()

			if not stem.v1.isVertical or not stem.v2.isVertical:
				label = '(%d)' % stem.w
			else:
				label = '%d' % stem.w
			tx = x1 + (x2 - x1)/2 - len(label)/2*10
			ty = y + 5/sc
			self.drawLabel(label, tx, ty, sc)

			#y -= 20 Later: needs optimisation to detect overlapping measure lines
											
		x = 0
 		for y, bar in metrics['bars'].items():
 			y1 = bar.y
 			y2 = y1 + bar.h
			path = NSBezierPath.bezierPath()
			path.moveToPoint_((x, y1))
			path.lineToPoint_((x, y2))
			
			# Arrow head top
			path.moveToPoint_((x-arrowSize, y2-arrowSize*2))
			path.lineToPoint_((x, y2))
			path.lineToPoint_((x+arrowSize, y2-arrowSize*2))
			# Arrow head bottom
			path.moveToPoint_((x-arrowSize, y1+arrowSize*2))
			path.lineToPoint_((x, y1))
			path.lineToPoint_((x+arrowSize, y1+arrowSize*2))

			path.setLineWidth_(0.5/sc)
			NSColor.darkGrayColor().set()
			path.stroke()
			
			# Horizontal lines to points
			path = NSBezierPath.bezierPath()
			path.moveToPoint_((x-8, y2))
			path.lineToPoint_((bar.x, y2))
			path.moveToPoint_((x-8, y1))
			path.lineToPoint_((bar.x, y1))

			path.setLineWidth_(0.5/sc)
			NSColor.lightGrayColor().set()
			path.stroke()
			
			if not bar.h1.isHorizontal or not bar.h2.isHorizontal:
				label = '(%d)' % bar.h
			else:
				label = '%d' % bar.h
			tx = x + 5/sc
			ty = y1 + (y2 - y1)/2 - 5/sc
			self.drawLabel(label, tx, ty, sc)
			
			#x -= 40 Later: needs optimisation to detect overlapping measure lines
		
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
		"""Clean up this tool if the window closes"""
		self.removeCallbacks()
		
	def removeCallbacks(self):
		"""Remove the event subscriptions  of this tool into GlyphsApp"""
		Glyphs.removeCallback( self.drawforeground, DRAWFOREGROUND )
		Glyphs.removeCallback( self.drawbackground, DRAWBACKGROUND )
	
	def showWindow(self, sender):
		# brings macro window to front and clears its log:
		Glyphs.clearLog()
		Glyphs.showMacroWindow()
	
	# ---------------------------------------------	
	# Glyph analyser code starts here
	# In the future this code is supposed to go to a more generic library to be imported.
	# Stem, Bar, Vertical and Horizontal classes not yet working.
	
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
		layerI = layer.parent.parent.glyphs['I'].layers[layer.name]
		_, verticals, horizontals = self.findVerticalsHorizontals(layerI)

		# Find the smallest (x1, x2) for the longest two verticals
		v1 = v2 = None
		for x, vs in sorted(verticals.items()): 
			for v in vs:
				if v1 is None or v1.h < v.h:
					v1 = v
				elif v2 is None or v2.h < v.h:
					v2  = v
		stemSize = abs(v1.x - v2.x) # This should be the stem size of the /H
		
		layerH = layer.parent.parent.glyphs['H'].layers[layer.name]
		_, _, horizontals = self.findVerticalsHorizontals(layerH)
		# Find the smallest (y1, y2) combination of horizontals
		barSize = None
		for y1 in horizontals.keys(): 
			for y2 in horizontals.keys(): 
				if y2 <= y1:
					continue
				if barSize is None or barSize > abs(y1  - y2):
					barSize = abs(y1 - y2)
		return stemSize, barSize # Answer the result as tuple.
		
	LO_MARGIN = 0.8 # Low margin factor of 80% for line distance to be considered stem or bar
	HI_MARGIN = 1.2 # High margin factor of 120% for line distance to be considered stem or bar
	 
	def findStems(self, verticals, defaultStem):
		# Looking for stems
		stems = {} # Key (x1, x2), value is Vertical instance
		def1 = defaultStem * self.LO_MARGIN # Widen the search range a bit, e.g. to cover 
		def2 = defaultStem * self.HI_MARGIN # thicker round stems in /O
		for x1, vs1 in sorted(verticals.items()): # Compare the x of all verticals 
			for x2, vs2 in sorted(verticals.items()): # with all other verticals		
				if x1 <= x2: # Skip mirrored and identical y values
					continue
				if def1 <= abs(x1 - x2) <= def2: # if the stem width is within the search range
					for v1 in vs1: # For all the Vertical lines in this x1 position
						for v2 in vs2: # For all the Vertical lines in this x2 position
							stem = Stem(v1, v2) # Create a Stem instance with those two Verticals
							stems[stem.x] = stem # Add the instance to the export dictionary
		return stems # Answer the result

	def findBars(self, horizontals, defaultBar):
		# Looking for stems
		bars = {} # Key (x1, x2), value is Horizontal instance
		def1 = defaultBar * self.LO_MARGIN # Widen the search range a bit, e.g. to cover
		def2 = defaultBar * self.HI_MARGIN # thinner round bars in /O
		for y1, hs1 in sorted(horizontals.items()): # Compare the y of all horizontals 
			for y2, hs2 in sorted(horizontals.items()):	# with all other horizontals				
				if y1 <= y2: # Skip mirrored values and identical x values
					continue
				if def1 <= abs(y1 - y2) <= def2: # If the bar height is within search range
					for h1 in hs1: # For all the Horizontal lines in this y1 position
						for h2 in hs2: # For all the Horizontal lines in this y2 position
							bar = Bar(h1, h2) # Create a Bar instance with those two Horizontals
							bars[bar.y] = bar # Add the instance to the export dictionary
		return bars # Answer the result

	VH_TOLERANCE = 8 # Tolerance in units if lines are considered to be vertical or horizontal
	ANGLE_TOLERANCE = 5 # Toloerance in degrees if diagonals are considered to be paralell.
	
	def findVerticalsHorizontals(self, layer):
		"""Answer the dictionary verticals and horizontals, where the key is respectively
		the x and y position of the line and the value is a list of (p, p1) pairs
		for the vertical or horizontal on that position (since, e.g. as in the /H there
		can be multiple verticals on the same x position.
		"""
		pcs = [] # List of point context tuples [(p_2, p_1, p, p1, p2), ...] 
		verticals = {} # Key is horizontal position, value is list [(p, p1), ...]
		horizontals = {} # Key is vertical position, value is [(p, p1), ...]
		for contour in layer.paths: # Check on all contours in the current glyph layer
			points = list(contour.nodes) # Make a list of all point instances
			for i in range(len(points)): # Run through the list of point with index i
			    # The 4 points around the current selected points (by index), using
			    # the flip over on the right side for negative index values.
			    # Since the starting point of this contours is arbitrary, we start
			    # for p at position p[i-2], so all points are in negative index,
			    # to be extracted as chunk of 5 points "left" of index i.
				# (p-2, p-1, p, p+1, p+2) <---- [p, p, p, p, p, p, p, ..., p]
				#                                i-1  i                      i-2
				p_2, p_1, p, p1, p2 = points[i-4], points[i-3], points[i-2], points[i-1], points[i]
				pcs.append((p_2, p_1, p, p1, p2)) # Add the points to the output list anyway.
				if abs(p.x - p1.x) <= self.VH_TOLERANCE: # Check x-distance (p, p1) within range
					v = Vertical(p, p1) # Then make a Vertical instance from these two points
					if not v.x in verticals: # If it does not exist as vertical key
						verticals[v.x] = [] # Create storage of verticals that share the same x position
					verticals[v.x].append(v) # Add to the output dictionary with smallest (v.x) as key
				if abs(p.y - p1.y) <= self.VH_TOLERANCE: # Check y-distance (p, p1) within range
					h = Horizontal(p, p1) # Then make a Horizontal instance from these two points
					if not h.y in horizontals: # If it does not exist as vertical key
						horizontals[h.y] = [] # Create storage of verticals that share the same x position
					horizontals[h.y].append(h) # Add to the output dictionary with smallest (v.y) as key
		return pcs, verticals, horizontals # Answer the results as tuples

    def getAngle(self, p, p1):
        xDiff = p1.x - p.x
        yDiff = p1.y - p.y
        angle = round(math.atan2(yDiff, xDiff) * 180 / math.pi, 3)
	
        while angle < 0:
            angle += 180
        while angle > 360:
            angle -= 180
        return angle

	def findDiagonals(self, pcs, defaultStem, defaultBar):
        """Find the dictionary of all point contexts, where the key is the
        normalized integer rounded angle. Definition of a diagonal is that it
        cannot be a vertical or horizontal."""
        diagonals = {} # Angle (different from 0, 90) is the key
        for _, _, p, p1, _ in pcs:
        	if p.x != p1.x and p.y != p1.y: # Only diagonals
                angle = int(round(self.getAngle(p, p1)))
                if not angle in diagonals:
                    diagonals[angle] = []
                diagonals[angle].append(Diagonal(p, p1))
        return diagonals

	def findDiagonalStems(self, diagonals):

        diagonalStems = {}

        for _, diagonals1 in diagonals.items(): # Angles are normalized, angle0, diagonals1
            for diagonal0 in diagonals1:
                for _, diagonals2 in diagonals.items(): # angle1, diagonals2
                    for diagonal1 in diagonals2:
                        if diagonal0 is diagonal1 or not diagonal0.isParallel(diagonal1): # Default tolerance of pc
                            continue
                        if (diagonal0.index, diagonal1.index) in found:
                            continue
                        # Test if the y values are in range so this can be seen as stem pair
                        # and test if this pair is spanning a black space
                        if not self.isDiagonalStem(diagonal0, diagonal1):
                            continue
                        found.add((diagonal0.index, diagonal1.index))
                        found.add((diagonal1.index, diagonal0.index))

                        diagonalStem = self.DIAGONALSTEMCLASS(diagonal0, diagonal1, self.glyph.name)
                        distance = diagonalStem.size # Average length of the diagonal projected lines
                        if not distance in diagonalStems:
                            diagonalStems[distance] = []
                        diagonalStems[distance].append(diagonalStem)
        return diagonalStems

	def getMetrics(self, layer):
		# Find the stem and bar in the /H glyph of the layer parent font.
		defaultStem, defaultBar = self.findDefaults(layer)
		print(defaultStem, defaultBar)
		# Layer is a GlyphsApp glyph style
		# pcs = list with [p_2, p_1, p, p1, p2] point contexts
		# verticals = dictionary of Vertical instances, key = vertical.x
		# horizontals = dictionary of Horizontal instances, key = horizontal.y
		pcs, verticals, horizontals = self.findVerticalsHorizontals(layer)
		# Looking for stems, using the defaultStem, as found in /H as reference.
		stems = self.findStems(verticals, defaultStem)	
		# Looking for bars, using the defaultBar, as found in /H, as reference.
		bars = self.findBars(horizontals, defaultBar)
		# Find diagonal line pairs with a distance from each other in the 
		# range of defaultStem or defaultBar, creating Diagonal instances
		diagonals = self.findDiagonals(pcs, defaultStem, defaultBar)
		
		# Make a dictionary of metrics results and aswer it.	
		metrics = dict(pcs=pcs, verticals=verticals, horizontals=horizontals, 
			diagonals=diagonals, stems=stems, bars=bars)
		return metrics
				
DimensionsTool()