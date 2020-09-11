#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#   P A G E B O T  N A N O
#
#   Copyright (c) 2020+ Buro Petr van Blokland + Claudia Mens
#   www.pagebot.io
#   Licensed under MIT conditions
#
#   Supporting DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#   elements.py
#
#   This source contains the class with knowledge about elements that
#   can be placed on a page.
#
import drawBot

try:
    import pagebotnano_004
except ImportError:
    import sys # Import access to some deep Python functions
    sys.path.insert(0, "../") # So we can import pagebotnano002 without installing.


def asColor(r, g=None, b=None, a=None):
    """Convert the attribute to a color tuple that is valid in DrawBot.

    >>> asColor(1) # Answer white color tuple
    (1, 1, 1, 1)
    >>> asColor(0, 0, 1) # Answer blue color
    (0, 0, 1, 1)
    >>> asColor(0.5) # 50% gray
    (0.5, 0.5, 0.5, 1)
    >>> asColor(0.5, 0.4, 0.3, 0.2)
    (0.5, 0.4, 0.3, 0.2)
    """
    if isinstance(r, (tuple, list)):
        if len(r) == 3:
            r, g, b = r
            return r, g, b, 1 # Return the color with undefined opacity.
        if len(r) == 4:
            return r # Answer the color tuple unchanged.
        print('asColor: Color "%s" for not have the right format')
        return (0, 0, 0) # Answer black in case of error
    if isinstance(r, (float, int)) and 0 <= r <= 1:
        # Fill the green and blue with the red value, if they are undefined.
        return r, g or r, b or r, a or 1 # Answer the (r, g ,b, a) 
    return None, None, None, None


class Element:
    """Base class of all elements that can be placed on a page.
    Class names start with a capital. See a class as a factory of element objects 
    (name spelled with an initial lower case.)
    
    >>> from pagebotnano_004.document import Document
    >>> doc = Document()
    >>> page = doc.newPage()
    >>> page
    <Page pn=1 w=595 h=842 elements=0>
    >>> e = Element(100, 100, 200, 300)
    >>> page.addElement(e)
    >>> page
    <Page pn=1 w=595 h=842 elements=1>
    >>> page.elements
    [<Element x=100 y=100 w=200 h=300 elements=0>]
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

    def __repr__(self):
        return '<%s x=%d y=%d w=%d h=%d elements=%s>' % (
            self.__class__.__name__, self.x, self.y, self.w, self.h, 
            len(self.elements))

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

    >>> t = Text('ABC'*200, x=100, y=200)
    >>> t
    <Text ABCABCABCA... x=100 y=200 w=None h=None>
    >>> t.fs[:10]
    'ABCABCABCA'
    """
    FormattedString = drawBot.FormattedString

    def __init__(self, fs, x, y, w=None, h=None, fill=None, stroke=None, strokeWidth=None):
        # Call the base element with all standard attributes.
        Element.__init__(self, x, y, w=w, h=h, fill=fill, stroke=stroke, strokeWidth=strokeWidth)
        self.fs = fs # Store the FormattedString in self.

    def __repr__(self):
        s = self.fs[:10]
        if len(s) != len(self.fs):
            s += '...'
        return '<%s %s x=%d y=%d w=%s h=%s>' % (
            self.__class__.__name__, s, self.x, self.y, self.w, self.h)

    def drawForeground(self, ox, oy, dox, page, parent):
        """We just need to define drawing of the foreground. The rest of behavior
        for the Text element (including drawing og the background) is handled
        by the base Element class.
        """
        drawBot.text(self.fs, (ox, oy))

if __name__ == "__main__":
    import doctest
    doctest.testmod()[0]