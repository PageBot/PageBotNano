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
import sys # Import access to some deep Python functions
import os
import drawBot

if __name__ == "__main__":
    sys.path.insert(0, "..") # So we can import pagebotnano002 without installing.

from pagebotnano_006.toolbox.color import asColor

class Element:
    """Base class of all elements that can be placed on a page.
    Class names start with a capital. See a class as a factory of element objects 
    (name spelled with an initial lower case.)
    
    >>> from pagebotnano_006.document import Document
    >>> doc = Document()
    >>> page = doc.newPage()
    >>> page
    <Page pn=1 w=595 h=842 elements=0>
    """
    def __init__(self, x=None, y=None, w=None, h=None, fill=None, stroke=None, strokeWidth=0):
        self.x = x or 0 # (x, y) position of the element from bottom left of parent.
        self.y = y or 0
        self.w = w # Width and height of the element bounding box
        self.h = h
        self.fill = fill or asColor(0) # Default is drawing a black rectangle.
        self.stroke = stroke # Default is drawing no stroke frame
        self.strokeWidth = strokeWidth
        self.elements = [] # Storage in case there are child elements

    def build(self, x, y, doc, page, parent=None):
        """Build the content of the element, including background color,
        stroked frame and content of the inheriting classes.

        >>> from pagebotnano_006.document import Document
        >>> doc = Document()
        >>> page = doc.newPage()
        >>> e = Element(10, 10, 100, 100, fill=(1, 0, 0))
        >>> page.addElement(e)
        >>> doc.build() # Recursively draws all pages and their elements.
        >>> doc.export('_export/Element-build.pdf') # Export an build again.
        """
        # Calculate the new origing relative to self, for all drawing,
        # including the child elements
        ox = x + self.x
        oy = y + self.y

        # Do building of the element background here. 
        #Let inheriting subclasses handle what must appear on the background.
        self.drawBackground(ox, oy, doc, page, parent)

        # Then let inheriting subclasses draw any content (if they have it)
        self.drawContent(ox, oy, doc, page, parent)

        # Then recursively pass the build instruction on to all child elements.
        # Use the position of self as origin for the relative position of the children.
        for element in self.elements:
            element.build(ox, oy, doc, page, parent=self)

        # Do building of the element foreground here. 
        #Let inheriting subclasses handle what must appear on the background.
        self.drawForeground(ox, oy, doc, page, parent)

    # Rough example of implementing HTML/CSS generator in this architecture
    #def build_html(self, x, y, doc, page, parent=None):
    #   print('<div class="" style="background-color: %s">' % asHtmlColor(self.fill))
    #   self.drawContent(ox, oy, doc, page, parent)
    #   print('</div>')

    def drawContent(self, ox, oy, doc, page, parent):
        """Default behavior is to do nothing, as the Element (and e.h. Rect)
        don’t have content to draw, besides the background and frame.
        """
        pass

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

# Rect = Element would have been the same.
class Rect(Element):
    """This element draws a simple rectangle. This is identical to the default 
    behavior of the base Element class, so nothing needs to be defined here.
        
    >>> from pagebotnano_006.document import Document
    >>> doc = Document()
    >>> page = doc.newPage()
    >>> padding = 40
    >>> e = Rect(padding, padding, page.w-2*padding, page.h-2*padding, fill=(1, 0.2, 1))
    >>> page.addElement(e)
    >>> doc.export('_export/Rect.pdf') # Build and export.
    """

class Text(Element):
    """This element draws a FormattedString on a defined place. Not text wrapping
    is done. 

    >>> from pagebotnano_006.document import Document
    >>> fs = Text.FormattedString('Hello world', font='Georgia', fontSize=100)
    >>> doc = Document()
    >>> page = doc.newPage()
    >>> padding = 40
    >>> e = Text(fs, padding, page.h/2, fill=(1, 0, 0))
    >>> page.addElement(e)
    >>> doc.export('_export/Text.pdf') # Build and export.
    """
    # Add abbreviation for easier usage.
    FormattedString = FS = drawBot.FormattedString

    def __init__(self, fs, x, y, w=None, h=None, fill=None, stroke=None, 
        strokeWidth=None):
        # Call the base element with all standard attributes.
        Element.__init__(self, x=x, y=y, w=w, h=h, fill=fill, stroke=stroke, 
            strokeWidth=strokeWidth)
        self.fs = fs # Store the FormattedString in self.

    def drawContent(self, ox, oy, dox, page, parent):
        """We just need to define drawing of the content. The rest of behavior
        for the Text element (including drawing on the background and the frame) 
        is handled by the base Element class.
        """
        drawBot.text(self.fs, (ox, oy))

class TextBox(Text):
    """This elements draws a FormattedString as wrapped text on a defined place
    with a defined width. It handles overflow and hyphenation for the given language
    code. 

    >>> from pagebotnano_006.document import Document
    >>> from pagebotnano_006.toolbox.loremipsum import loremipsum
    >>> headLine = 'Example of TextBox overflow\\n'
    >>> txt = loremipsum()
    >>> fontSize = 30
    >>> headSize = fontSize*1.5
    >>> fs = Text.FS(headLine, font='Georgia-Bold', lineHeight=headSize*1.4, fontSize=headSize)
    >>> fs.append(Text.FS(txt, font='Georgia', lineHeight=fontSize*1.4, fontSize=fontSize))
    >>> doc = Document()
    >>> padding = 80
    >>> while True:
    ...     page = doc.newPage()
    ...        # Add text element with page number
    ...     pn = Text.FS(str(page.pn), align='center', font='Georgia', fontSize=16)
    ...     e = Text(pn, page.w/2, padding/2)
    ...     page.addElement(e)
    ...     e = TextBox(fs, x=padding, y=padding, w=page.w-2*padding, h=page.h-2*padding, fill=1)
    ...     page.addElement(e)
    ...     fs = e.getOverflow(fs)
    ...     if not fs:
    ...         break
    >>> doc.export('_export/TextBox-Overflow.pdf') # Build and export.

    """
    def __init__(self, fs, x, y, w, h=None, fill=None, stroke=None, 
            strokeWidth=None):
        """Call the super class element with all standard attributes.
        Different from the Text class, now the width `w` is a required attribute.
        """
        Text.__init__(self, fs, x=x, y=y, w=w, h=h, fill=fill, stroke=stroke, 
            strokeWidth=strokeWidth)

    def getOverflow(self, fs=None, w=None, h=None, doc=None):
        """Flow the text into self and put any overflow in self.next.
        If there is no self.next defined, then store the remaining overflow
        text in self.overflow.
        """
        # If another FormattedString is defined, then use that.
        # Otherwise use the existing self.fs
        if fs is None:
            fs = self.fs
        # Since we cannot test the overflow without drawing in DrawBot, we'll
        # create a text column far outside the page boundaries. 
        # Unfortunately this increases the PDF export size.
        h = w or self.h
        w = h or self.w
        if h is None and w is not None:
            # Height of the box is undefined, measure it from the defined column width.
            _, h = drawBot.textSize(fs, width=w)
        elif w is None and h is not None:
            # Width of the box is undefined, measure it from the defined column height.
            w, _ = drawBot.textSize(fs, height=h)
        # Height of the box is undefined, measure it from the defined column width.
        return drawBot.textBox(fs, (10000000, 0, w, h))

    def drawContent(self, ox, oy, doc, page, parent):
        """We just need to define drawing of the foreground. The rest of behavior
        for the Text element (including drawing on the background) is handled
        by the base Element class.
        """
        # Store any overflow to be processed by the caller.
        # Note that this should never happen, as the context of the text box
        # better can be processed by self.flowText before any drawing is done.
        # It is assumed that self.h is set, otherwise take the height of the
        # text column that fits all text.
        h = self.h
        w = self.w
        if h is None and w is not None:
            # Height of the box is undefined, measure it from the defined column width.
            _, h = drawBot.textSize(self.fs, width=w)
        elif w is None and h is not None:
            # Width of the box is undefined, measure it from the defined column height.
            w, _ = drawBot.textSize(self.fs, height=h)
        # Else if width and height are both defined or undefined, we can used them as is. 
        # In case width and height are both defined, it may result in a new overflow
        # FormattedString. Store that in self.overflow.
        self.overflow = drawBot.textBox(self.fs, (ox, oy, self.w, self.h or page.h)) 

class Image(Element):
    """This element draws an image on a defined place. 

    >>> from pagebotnano_006.document import Document
    >>> doc = Document()
    >>> page = doc.newPage()
    >>> padding = 40
    >>> imagePath = '../../resources/images/cookbot10.jpg'
    >>> e = Image(imagePath, x=padding, w=page.w/2-2*padding)
    >>> iw, ih = e.getSize() # Get the size of the Image element
    >>> e.y = page.h - padding - ih # Align the image on top of the page.
    >>> page.addElement(e)
    >>> e = Image(imagePath, x=padding, y=padding, w=page.w-2*padding)
    >>> iw, ih = e.getSize() # Get the size of the Image element
    >>> page.addElement(e)
    >>> doc.export('_export/Image.pdf') # Build and export as PDF
    >>> doc.export('_export/Image.png') # Build and export as PNG
    """
    def __init__(self, path, x=None, y=None, w=None, h=None, fill=None, stroke=None, 
        strokeWidth=None):
        # Call the base element with all standard attributes.
        Element.__init__(self, x=x, y=y, w=w, h=h, fill=fill, stroke=stroke, 
            strokeWidth=strokeWidth)
        assert os.path.exists(path), ('Image: Path "%s" does not exist.' % path)
        self.path = path

    @classmethod
    def imageSize(cls, path):
        """Answer the images size in points.

        >>> imagePath = '../../resources/images/cookbot10.jpg'
        >>> Image.imageSize(imagePath)
        (2058, 946)
        """
        return drawBot.imageSize(path)

    def getSize(self):
        """Answer the scaled size of the image.

        >>> imagePath = '../../resources/images/cookbot10.jpg'
        >>> e = Image(imagePath, w=500)
        >>> w, h = e.getSize()
        >>> '%0.2f, %0.2f' % (w, h) # Python method of rounding float numbers.
        '500.00, 229.83'
        """
        iw, ih = self.imageSize(self.path)
        sx, sy = self.getScale()
        return iw*sx, ih*sy

    def getScale(self):
        """Answer the scale of the image file, compared to the target scale of self.
        Detect if the image should proportionally scaled to (w, h) in case one 
        of the two is undefined.

        >>> imagePath = '../../resources/images/cookbot10.jpg'
        >>> e = Image(imagePath, w=500)
        >>> sx, sy = e.getScale()
        >>> '%0.2f, %0.2f' % (sx, sy) # Python method of rounding float numbers.
        '0.24, 0.24'
        >>> e.h = 2000 # Scaling disproportional now
        >>> sx, sy = e.getScale()
        >>> '%0.2f, %0.2f' % (sx, sy) # Python method of rounding float numbers.
        '0.24, 2.11'
        >>> e.w = e.h = None # Disable scaling of the image
        >>> sx, sy = e.getScale()
        >>> '%0.2f, %0.2f' % (sx, sy) # Python method of rounding float numbers.
        '1.00, 1.00'
        """
        # Get the size in points of this image
        iw, ih = self.imageSize(self.path)
        # If self.w is defined and not self.h defined, then scale proportional
        if self.w and self.h is None:
            sx = sy = self.w/iw
        # If self.w not defined and self.h is defined, then scale proportional
        elif self.w is None and self.h:
            sx = sy = self.h/ih
        # If both (w, h) are defined, then scale non-proportional
        elif self.w and self.h: # Non-proportional scaling
            sx = self.w/iw
            sy = self.h/ih
        else: # No scaling
            sx = sy = 1 
        return sx, sy

    def drawContent(self, ox, oy, doc, page, parent):
        """We just need to define drawing of the image. The rest of behavior
        for the Image element (including drawing on the background and the frame) 
        is handled by the base Element class.
        """
        # Get the scale of the image, comparing the file size with the size
        # of the image element.
        sx, sy = self.getScale()
        # In drawBot it is not possible to scale the image, so we need to scale
        # the canvas instead. Then also we need to scale the (ox, oy) positions.
        # After drawing, reverse scale the canvas back to 100%
        drawBot.save()
        drawBot.scale(sx, sy)
        drawBot.image(self.path, (ox/sx, oy/sy))
        #drawBot.scale(1/sx, 1/sy)
        drawBot.restore()


if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]