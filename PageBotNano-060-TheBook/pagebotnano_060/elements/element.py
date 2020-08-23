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
import os
from copy import deepcopy
import sys
sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano_060.constants import CENTER, PADDING
from pagebotnano_060.babelstring import BabelString
from pagebotnano_060.toolbox.transformer import path2FileName, makePadding
from pagebotnano_060.toolbox.color import color

class Element:
    """Base class of all elements that can be placed on a page.
    Class names start with a capital. See a class as a factory of element objects 
    (name spelled with an initial lower case.)
    
    >>> from pagebotnano_060.document import Document
    >>> from pagebotnano_060.contexts.drawbot.context import DrawBotContext
    >>> context = DrawBotContext()
    >>> doc = Document(context=context)
    >>> page = doc.newPage()
    >>> page
    <Page pn=1 w=595pt h=842pt elements=0>
    """
    def __init__(self, x=None, y=None, w=None, h=None, name=None, parent=None,
            template=None, fill=None, stroke=None, strokeWidth=0, 
            padding=None, margin=None):
        self.x = x or 0 # (x, y) position of the element from bottom left of parent.
        self.y = y or 0
        self.w = w # Width and height of the element bounding box
        self.h = h
        self.fill = color(fill) # Default is drawing a black rectangle.
        self.stroke = color(stroke) # Default is drawing no stroke frame
        self.strokeWidth = strokeWidth
        self.padding = padding # Initialize the padding
        self.margin = margin
        self.elements = [] # Storage in case there are child elements

        # Optional name, e.g. for template or element finding. Defaults to class name.
        self.name = name or self.__class__.__name__ 
        self.template = template # Optional template function for this element.

        # If a parent is defined, then add self to the parent children.
        if parent is not None:
            parent.addElement(self)

        # Allow elements, pages and templates to initialize themselves
        # by implementing the self.initialize method.
        self.initialize()

    def initialize(self):
        """Allow elements, pages and templates to initialize themselves
        by implementing this method in inheriting classes.
        Default behavior is to do nothing.
        """

    def _get_padding(self):
        """Answer a tuple of the 4 padding values of the element

        >>> from pagebotnano_060.toolbox.units import mm, pt
        >>> e = Element() # Other values are default PADDING
        >>> e.padding
        (30pt, 30pt, 30pt, 30pt)
        >>> e = Element(padding=20)
        >>> e.padding
        (20pt, 20pt, 20pt, 20pt)
        >>> e.padding = mm(40)
        >>> e.padding
        (40mm, 40mm, 40mm, 40mm)
        >>> e.padding = pt(10, 20, 30, 40)
        >>> e.padding 
        (10pt, 20pt, 30pt, 40pt)
        """
        return self.pt, self.pr, self.pb, self.pl 
    def _set_padding(self, padding):
        self.pt, self.pr, self.pb, self.pl = makePadding(padding, default=PADDING)
    padding = property(_get_padding, _set_padding)

    def _get_pw(self):
        """Answer the usable element space, withing the horizontal padding

        >>> e = Element(w=500, padding=(50, 50, 100, 50))
        >>> e.pw
        400pt
        """
        return self.w - self.pl - self.pr
    pw = property(_get_pw)

    def _get_ph(self):
        """Answer the usable element space, withing the vertical padding

        >>> e = Element(h=500, padding=(50, 50, 100, 50))
        >>> e.ph
        350pt
        """
        return self.h - self.pt - self.pb
    ph = property(_get_ph)

    def __repr__(self):
        return '<%s name=%s w=%s h=%s>' % (self.__class__.__name__, self.name, self.w, self.h)

    def addElement(self, e):
        """Add the element to the list of child elements.
        """
        self.elements.append(e)
        return e # Answer the element in convenience for the caller.

    def find(self, name=None, pattern=None):
        """Search through the tree of self and self.elements to find an
        element with the indicated name.

        >>> e = Element(name='root')
        >>> child1 = e.addElement(Element(name='child1'))
        >>> child2 = child1.addElement(Element(name='child2'))
        >>> child3 = child2.addElement(Element(name='child3'))
        >>> e is e.find('root')
        True
        >>> child1 is e.find('child1')
        True
        >>> child3 is e.find('child3') # Finding recursive deep
        True
        """
        assert name is not None or pattern is not None, ('Element.find: Define either name or pattern' % self.__class__.__name__)
        if name is not None and name == self.name:
            return self
        if pattern is not None and pattern in self.name:
            return self
        for child in self.elements:
            found = child.find(name)
            if found is not None:
                return found
        return None

    def compose(self, doc, page, parent=None):
        """Compose the layout of an element. Default behavior is to pass it on
        to the children. To be redefined by inheriting Element to make their own
        layout composition.

        >>> from pagebotnano_060.document import Document
        >>> from pagebotnano_060.templates.onecolumn import OneColumnTemplates
        >>> from pagebotnano_060.themes import SeasoningTheDish
        >>> theme = SeasoningTheDish()
        >>> doc = Document()
        >>> page = OneColumnTemplates.oneColumnPage(theme, doc)
        >>> page
        <Page pn=1 w=595pt h=842pt elements=2>
        """
        if self.template is not None:
            self.template(doc, page, self)
        # Now broadcast the compose call to all child elements.
        # Note that these may just have been created by the template.
        for e in self.elements:
            e.compose(doc, page, self)

    def build(self, x, y, doc, page, parent=None):
        """Build the content of the element, including background color,
        stroked frame and content of the inheriting classes.

        >>> from pagebotnano_060.document import Document
        >>> from pagebotnano_060.contexts.drawbot.context import DrawBotContext
        >>> context = DrawBotContext()
        >>> doc = Document(context=context)
        >>> page = doc.newPage()
        >>> e = Element(10, 10, 100, 100, fill=color(1, 0, 0))
        >>> page.addElement(e)
        >>> doc.build() # Recursively draws all pages and their elements.
        >>> doc.export('_export/Element-build.pdf') # Export an build again.
        """
        # Calculate the new origing relative to self, for all drawing,
        # including the child elements
        ox = x + self.x
        oy = y + self.y

        # Do building of the element background here. 
        # Let inheriting subclasses handle what must appear on the background.
        # Disadvantage of this method is that fill objects with a stroke get
        # drawn double in InDesign. Bit allows to use the stroke outlines as
        # clipping frame if other content is added to between the two layers.
        self.drawBackground(ox, oy, doc, page, parent)

        # Then let inheriting subclasses draw any content (if they have it)
        self.drawContent(ox, oy, doc, page, parent)

        # Then recursively pass the build instruction on to all child elements.
        # Use the position of self as origin for the relative position of the children.
        for element in self.elements:
            element.build(ox, oy, doc, page, parent=self)

        # Do building of the element foreground here. 
        # Let inheriting subclasses handle what must appear on the background.
        # Draw the stroke of the element, in case a color and tickness was defined. 
        self.drawForeground(ox, oy, doc, page, parent)

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
            doc.context.stroke(None) # Any stroke drawing is done in foreground
            doc.context.fill(self.fill)
            if self.w is not None and self.h is not None:
                doc.context.rect(ox, oy, self.w, self.h)

    def drawForeground(self, ox, oy, doc, page, parent):
        """Draw the foreground of the element. Default is to just draw the 
        rectangle with the fill color, if it is defined. This method should be 
        redefined by inheriting subclasses that need different foreground drawing.
        """
        if self.stroke is not None and self.strokeWidth: # Only if defined.
            doc.context.fill(None) # Fill is done in background drawing.
            doc.context.stroke(self.stroke, self.strokeWidth)
            if self.w is not None and self.h is not None:
                doc.context.rect(ox, oy, self.w, self.h)

# Rect = Element would have been the same.
class Rect(Element):
    """This element draws a simple rectangle. This is identical to the default 
    behavior of the base Element class, so nothing needs to be defined here.
        
    >>> from pagebotnano_060.document import Document
    >>> from pagebotnano_060.contexts.drawbot.context import DrawBotContext
    >>> context = DrawBotContext()
    >>> doc = Document(context=context)
    >>> page = doc.newPage()
    >>> padding = 40
    >>> e = Rect(parent=page, x=padding, y=padding, w=page.w-2*padding, h=page.h-2*padding, fill=color(1, 0.2, 1))
    >>> doc.export('_export/Rect.pdf') # Build and export.
    """

# Oval = Element would have been the same.
class Oval(Element):
    """This element draws a simple oval. 
        
    >>> from pagebotnano_060.document import Document
    >>> doc = Document()
    >>> page = doc.newPage()
    >>> padding = 40
    >>> e = Oval(parent=page, x=padding, y=padding, w=page.w-2*padding, h=page.h-2*padding, fill=color(1, 0.2, 1))
    >>> doc.export('_export/Rect.pdf') # Build and export.
    """
    def drawBackground(self, ox, oy, doc, page, parent):
        """Draw the background of the element. Default is to just draw the 
        oval with the fill color, if it is defined. This method should be 
        redefined by inheriting subclasses that need different foreground drawing.
        """
        if self.fill is not None:
            doc.context.stroke(None) # Any stroke drawing is done in foreground
            doc.context.fill(self.fill)
            if self.w is not None and self.h is not None:
                doc.context.oval(ox, oy, self.w, self.h)

    def drawForeground(self, ox, oy, doc, page, parent):
        """Draw the foreground of the element. Default is to just draw the 
        rectangle with the fill color, if it is defined. This method should be 
        redefined by inheriting subclasses that need different foreground drawing.
        """
        if self.stroke is not None and self.strokeWidth: # Only if defined.
            doc.context.fill(None) # Fill is done in background drawing.
            doc.context.stroke(self.stroke, self.strokeWidth)
            if self.w is not None and self.h is not None:
                doc.context.oval(ox, oy, self.w, self.h)

class Text(Element):
    """This element draws a FormattedString on a defined place. Not text wrapping
    is done. 

    >>> from pagebotnano_060.document import Document

    >>> from pagebotnano_060.babelstring import BabelString
    >>> from pagebotnano_060.contexts.drawbot.context import DrawBotContext
    >>> context = DrawBotContext()
    >>> style = dict(font='Georgia', fontSize=100)
    >>> bs = BabelString('Hello world', style)
    >>> doc = Document(context=context)
    >>> page = doc.newPage()
    >>> padding = 40
    >>> e = Text(bs, padding=padding, w=page.h/2, fill=color(1, 0, 0))
    >>> page.addElement(e)
    >>> doc.export('_export/Text.pdf') # Build and export.
    """

    def __init__(self, bs, **kwargs):
        # Call the base element with all standard attributes.
        Element.__init__(self, **kwargs)

        if not isinstance(bs, BabelString):
            bs = BabelString(bs)
        self.bs = bs # Store the BabelString in self.

    def drawContent(self, ox, oy, doc, page, parent):
        """We just need to define drawing of the content. The rest of behavior
        for the Text element (including drawing on the background and the frame) 
        is handled by the base Element class.
        """
        doc.context.text(self.bs, (ox, oy))

class TextBox(Text):
    """This elements draws a FormattedString as wrapped text on a defined place
    with a defined width. It handles overflow and hyphenation for the given language
    code. 

    >>> from pagebotnano_060.document import Document
    >>> from pagebotnano_060.babelstring import BabelString
    >>> from pagebotnano_060.toolbox.loremipsum import loremipsum
    >>> from pagebotnano_060.contexts.drawbot.context import DrawBotContext
    >>> context = DrawBotContext()
    >>> headLine = 'Example of TextBox overflow\\n'
    >>> txt = loremipsum()
    >>> fontSize = 30
    >>> headSize = fontSize*1.5
    >>> headStyle = dict(font='Georgia-Bold', lineHeight=headSize*1.2, fontSize=headSize, fill=color(0))
    >>> textStyle = dict(font='Georgia', lineHeight=fontSize*1.4, fontSize=fontSize, fill=color(0))
    >>> bs = BabelString(headLine, headStyle)
    >>> bs2 = BabelString(txt, textStyle)
    >>> bs.append(bs2)
    >>> doc = Document(context=context)
    >>> padding = 80
    >>> while True:
    ...     page = doc.newPage()
    ...        # Add text element with page number
    ...     pn = BabelString(str(page.pn), dict(align=CENTER, font='Georgia', fontSize=16))
    ...     e = Text(pn, w=page.w/2, parent=page)
    ...     e = TextBox(bs, parent=page, x=padding, y=padding, w=page.w-2*padding, h=page.h-2*padding, fill=1)
    ...     bs = e.getOverflow(bs, doc=doc)
    ...     if not bs.fs: # Test on this “incomplete” BabelString, as it only has a cached FS
    ...         break
    >>> doc.export('_export/TextBox-Overflow.pdf') # Build and export.

    """
    def __init__(self, bs, w=None, **kwargs):
        """Call the super class element with all standard attributes.
        Different from the Text class, now the width `w` is a required attribute.
        """
        assert w is not None
        Text.__init__(self, bs, w=w, **kwargs)

    def getOverflow(self, bs=None, w=None, h=None, doc=None):
        """Flow the text into self and put any overflow in self.next.
        If there is no self.next defined, then store the remaining overflow
        text in self.overflow.
        """
        # Make sure that there is a `doc` for the context.
        assert doc is not None

        # If another FormattedString is defined, then use that.
        # Otherwise use the existing BabelString self.bs
        if bs is None:
            bs = self.bs

        # Note that the hyphenation flag works while drawing the textBox, for the
        # entire textbox. It is not – what would be expected – defined per paragraph.
        doc.context.hyphenation(bs.hyphenation)

        # Since we cannot test the overflow without drawing in the context, 
        # we'll create a text column far outside the page boundaries. 
        # Unfortunately this increases the PDF export size.
        h = w or self.h
        w = h or self.w
        if h is None and w is not None:
            # Height of the box is undefined, measure it from the defined column width.
            _, h = doc.context.textSize(bs, width=w)
        elif w is None and h is not None:
            # Width of the box is undefined, measure it from the defined column height.
            w, _ = doc.context.textSize(bs, height=h)

        # Height of the box is undefined, measure it from the defined column width.
        return doc.context.textBox(bs, (10000000, 0, w, h))

    def drawContent(self, ox, oy, doc, page, parent):
        """We just need to define drawing of the foreground. The rest of behavior
        for the Text element (including drawing on the background) is handled
        by the base Element class.
        """
        # Note that the hyphenation flag works while drawing the textBox, for the
        # entire textbox. It is not – what would be expected – defined per paragraph.
        doc.context.hyphenation(self.bs.hyphenation)

        # Store any overflow to be processed by the caller.
        # Note that this should never happen, as the context of the text box
        # better can be processed by self.flowText before any drawing is done.
        # It is assumed that self.h is set, otherwise take the height of the
        # text column that fits all text.
        h = self.h
        w = self.w
        if h is None and w is not None:
            # Height of the box is undefined, measure it from the defined column width.
            _, h = doc.context.textSize(self.bs, w=w)
        elif w is None and h is not None:
            # Width of the box is undefined, measure it from the defined column height.
            w, _ = doc.context.textSize(self.bs, h=h)
        # Else if width and height are both defined or undefined, we can used them as is. 
        # In case width and height are both defined, it may result in a new overflow
        # FormattedString. Store that in self.overflow.
        self.overflow = doc.context.textBox(self.bs, (ox, oy, self.w, self.h or page.h)) 

class Image(Element):
    """This element draws an image on a defined place. 

    >>> from pagebotnano_060.document import Document
    >>> doc = Document()
    >>> page = doc.newPage()
    >>> padding = 40
    >>> imagePath = '../../../resources/images/cookbot10.jpg'
    >>> e = Image(imagePath, x=padding, w=page.w/2-2*padding)
    >>> iw, ih = e.getSize(doc) # Get the size of the Image element
    >>> e.y = page.h - padding - ih # Align the image on top of the page.
    >>> page.addElement(e)
    >>> e = Image(imagePath, x=padding, y=padding, w=page.w-2*padding)
    >>> iw, ih = e.getSize(doc) # Get the size of the Image element
    >>> page.addElement(e)
    >>> doc.export('_export/Image.pdf') # Build and export as PDF
    >>> doc.export('_export/Image.png') # Build and export as PNG
    """
    def __init__(self, path=None, **kwargs):
        # Call the base element with all standard attributes.
        Element.__init__(self, **kwargs)
        assert path is None or os.path.exists(path), ('Image: Path "%s" does not exist.' % path)
        self.path = path # Path can be None for later filling. 

    def __repr__(self):
        return '<%s file=%s w=%s h=%s>' % (self.__class__.__name__, path2FileName(self.path), self.w, self.h)

    @classmethod
    def imageSize(cls, path, doc):
        """Answer the images size in points.

        >>> from pagebotnano_060.document import Document
        >>> doc = Document()
        >>> path = '../../../resources/images/cookbot10.jpg'
        >>> Image.imageSize(path, doc)
        (2058, 946)
        """
        return doc.context.imageSize(path)

    def getSize(self, doc):
        """Answer the scaled size of the image.

        >>> from pagebotnano_060.document import Document
        >>> doc = Document()
        >>> imagePath = '../../../resources/images/cookbot10.jpg'
        >>> e = Image(imagePath, w=500)
        >>> w, h = e.getSize(doc)
        >>> '%0.2f, %0.2f' % (w, h) # Python method of rounding float numbers.
        '500.00, 229.83'
        """
        iw, ih = self.imageSize(self.path, doc)
        sx, sy = self.getScale(doc)
        return iw*sx, ih*sy

    def getScale(self, doc):
        """Answer the scale of the image file, compared to the target scale of self.
        Detect if the image should proportionally scaled to (w, h) in case one 
        of the two is undefined.

        >>> from pagebotnano_060.document import Document
        >>> doc = Document()
        >>> imagePath = '../../../resources/images/cookbot10.jpg'
        >>> e = Image(imagePath, w=500)
        >>> sx, sy = e.getScale(doc)
        >>> '%0.2f, %0.2f' % (sx, sy) # Python method of rounding float numbers.
        '0.24, 0.24'
        >>> e.h = 2000 # Scaling disproportional now
        >>> sx, sy = e.getScale(doc)
        >>> '%0.2f, %0.2f' % (sx, sy) # Python method of rounding float numbers.
        '0.24, 2.11'
        >>> e.w = e.h = None # Disable scaling of the image
        >>> sx, sy = e.getScale(doc)
        >>> '%0.2f, %0.2f' % (sx, sy) # Python method of rounding float numbers.
        '1.00, 1.00'
        """
        if self.path is None or not os.path.exists(self.path):
            # Can be None or none existing image, then answer default size.
            iw = ih = 1000
        else:
            # Get the size in points of this image
            iw, ih = self.imageSize(self.path, doc)
        # If both (w, h) are defined, then scale non-proportional
        if self.w and self.h is None:
            sx = sy = self.w/iw
        elif self.w is None and self.h:
            sx = sy = self.h/ih
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
        if self.path is None or not os.path.exists(self.path):
            w = self.w or self.h or 1000
            h = self.h or w
            doc.context.fill(0.5)
            doc.context.stroke(0, 0.5)
            doc.context.rect(self.x, self.y, w, h)
            doc.context.fill(None)
            doc.context.line((self.x, self.y), (self.x+w, self.y+h))
            doc.context.line((self.x, self.y+h), (self.x+w, self.y))

        else: # There is a legal path, draw the image.
            # Get the scale of the image, comparing the file size with the size
            # of the image element.
            sx, sy = self.getScale(doc)
            # In drawBot it is not possible to scale the image, so we need to scale
            # the canvas instead. Then also we need to scale the (ox, oy) positions.
            # After drawing, reverse scale the canvas back to 100%
            doc.context.scale(sx, sy)
            doc.context.image(self.path, (ox/sx, oy/sy))
            doc.context.scale(1/sx, 1/sy)

# Marker = Element would have been the same.
class Marker(Element):
    """This element does not draw anything. It is used as instructor code
    when composing pages from a galley. There are several different markers 
    supported by the Typesetter, such as $page$, $chapter$, etc.
    """
    def __init__(self, markerType, index=0, **kwargs):
        """Call the base element with all standard attributes.
        """
        Element.__init__(self, **kwargs)
        self.markerType = markerType # Name of the tag, for the composer to respond to.
        self.index = index # Optional index reference of the tag.

    def __repr__(self):
        return '<%s type=%s index=%s>' % (self.__class__.__name__, self.markerType, self.index)

    def build(self, x, y, doc, page, parent=None):
        """Ingore any drawing or passing on to children.
        """
        pass

if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]