#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#	P A G E B O T  N A N O
#
#	Copyright (c) 2020+ Buro Petr van Blokland + Claudia Mens
#	www.pagebot.io
#	Licensed under MIT conditions
#
#	Supporting DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#	elements.py
#
#	This source contains the class with knowledge about elements that
#	can be placed on a page.
#
import sys
sys.path.insert(0, "..") # So we can import pagebotnano without installing.
import drawBot

class Element:
	"""Base class of all elements that can be placed on a page.
	Class names start with a capital. See a class as a factory of element objects 
	(name spelled with an initial lower case.)
	
	>>> from pagebotnano.document import Document
	>>> doc = Document()
	>>> page = doc.newPage()
	>>> page
	<Page pn=1 w=595 h=842 elements=0>
	"""
	def __init__(self, x, y, w, h, fill=None, stroke=None, strokeWidth=0):
		self.x = x # (x, y) position of the element from bottom left of parent.
		self.y = y
		self.w = w # Width and height of the element bounding box
		self.h = h 
		self.fill = fill or asColor(0) # Default is drawing a black rectangle.
		self.stroke = stroke # Default is drawing no stroke frame
		self.strokeWidth = strokeWidth
		self.elements = [] # Storage in case there are child elements

	def build(self, x, y, doc, page, parent=None):
		# Calculate the new origing relative to self, for all drawing,
		# including the child elements
		ox = x + self.x
		oy = y + self.y

		# Do building of the element background here. 
		#Let inheriting subclasses handle what must appear on the background.
		self.drawBackground(ox, oy, doc, page, parent)

		# Then recursively pass the build instruction on to all child elements.
		# Use the position of self as origin for the relative position of the children.
		for element in self.elements:
			element.build(ox, oy, doc, page, parent=self)

		# Do building of the element foreground here. 
		#Let inheriting subclasses handle what must appear on the background.
		self.drawForeground(ox, oy, doc, page, parent)

	def drawBackground(self, ox, oy, doc, page, parent):
		"""Draw the background of the element. Default is to just draw the 
		rectangle with the fill color, if it is defined. This method should be 
		redefined by inheriting subclasses that need different foreground drawing.
		"""
		if self.fill is not None:
			drawBot.stroke(None) # Any stroke drawing is done in foreground
			r, g, b, a = asColor(self.fill)
			if r is None:
				drawBot.fill(None)
			else:
				drawBot.fill(r, g, b, a)
			if self.w is not None and self.h is not None:
				drawBot.rect(ox, oy, self.w, self.h)

	def drawForeground(self, ox, oy, doc, page, parent):
		"""Draw the foreground of the element. Default is to just draw the 
		rectangle with the fill color, if it is defined. This method should be 
		redefined by inheriting subclasses that need different foreground drawing.
		"""
		if self.stroke is not None and self.strokeWidth: # Only if defined.
			drawBot.fill(None) # Fill is done in background drawing.
			r, g, b, a = asColor(self.stroke)
			if r is None:
				drawBot.stroke(None)
			else:
				drawBot.strokeWidth(self.strokeWidth)
				drawBot.stroke(r, g, b, a)
			if self.w is not None and self.h is not None:
				drawBot.rect(ox, oy, self.w, self.h)

class Rect(Element):
	"""This element draws a simple rectangle. This is identical to the default 
	behavior of the base Element class, so nothing needs to be defined here."""

class Text(Element):
	"""This element draws a FormattedString on a defined place. Not text wrapping
	is done. 
	"""
	FormattedString = drawBot.FormattedString

	def __init__(self, fs, x, y, w=None, h=None, fill=None, stroke=None, strokeWidth=None):
		# Call the base element with all standard attributes.
		Element.__init__(self, x, y, w=w, h=h, fill=fill, stroke=stroke, strokeWidth=strokeWidth)
		self.fs = fs # Store the FormattedString in self.

	def drawForeground(self, ox, oy, dox, page, parent):
		"""We just need to define drawing of the foreground. The rest of behavior
		for the Text element (including drawing og the background) is handled
		by the base Element class.
		"""
		drawBot.text(self.fs, (ox, oy))

if __name__ == "__main__":
    import doctest
    doctest.testmod()[0]