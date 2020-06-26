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
#   typespecimen.py
#
#   This source contains the class with knowledge about elements that
#   can be placed on a page.
#
import sys
sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

import drawBot

from pagebotnano.elements import Element, Rect, Line, Text
from pagebotnano.babelstring import BabelString
from pagebotnano.toolbox.color import noColor, color
from pagebotnano.constants import CENTER, LEFT

FONT_NAME = 'Verdana'
LABEL_SIZE = 10
LEADING = 13

class GlyphView(Element):
    """The GlyphView show single glyphs with metrics lines.

    >>> from pagebotnano.document import Document
    >>> doc = Document(w=200, h=200)
    >>> page = doc.newPage()
    >>> pad = 10
    >>> page.padding = pad
    >>> e = GlyphView('Hhj', 'Georgia', x=pad, y=pad, w=page.pw, h=page.ph, fill=0.96)
    >>> page.addElement(e)
    >>> doc.export('_export/GlyphView.pdf')
    """
    def __init__(self, glyphName, font, lineColor=None, lineWidth=None, **kwargs):
        Element.__init__(self, **kwargs)
        self.font = font
        self.glyphName = glyphName
        self.lineColor = lineColor or (0, 0, 1) # Color of metrics lines
        self.lineWidth = lineWidth or 0.5 # Thickness of metrics lines
        self.fontSize = self.h # As start assume the full height of the element as fontSize

        # Create a style for it, so we can draw the glyph(s) as Text.
        style = dict(font=self.font, fontSize=self.fontSize, textFill=0, align=CENTER)
        self.bs = BabelString(self.glyphName, style=style)
        tw, th = self.bs.textSize # Get the size of the glyph(s) string to see if it fits.

        if self.w and tw > self.w: # If width of self is defined and string is wider
            # Interpolate the fontSize from the measured width to smaller scaled fontSize.
            self.fontSize *= self.w / tw
            # Make a new string with the fitting fontSize
            style['fontSize'] = self.fontSize # Adjust the existing style
            self.bs = BabelString(self.glyphName, style=style)

    def drawContent(self, ox, oy, doc, page, parent):
        """Draw the content of this single glyph/string fitting, with line indicators
        of vertical metrics.

        TODO: Show more font metrics and glyph metrics here. Add labels of values and names.
        """

        # Set the contextx to font and fontSize, so we get the right descender back.
        doc.context.font(self.font, self.fontSize) # Set to new fontSize, so metrics do fit
        descender = doc.context.fontDescender() # Scaled descender of current font/fontSize
        # If the fontSize is down scaled to match the string width, then evenely 
        # distribute the extra vertical space above and below that scaled fontSize.
        baseline = (self.h - self.fontSize)/2 - descender # Distance from baseline to bottom y
        
        y = oy + baseline # Calculate the position of the baseline.
        doc.context.text(self.bs, (ox+self.w/2, y)) # Draw the glyphs on centered position.

        doc.context.stroke(self.lineColor, self.lineWidth)
        doc.context.line((ox, y), (ox+self.w, y)) # Draw baseline

        xHeight = doc.context.fontXHeight()
        y = oy + baseline + xHeight
        doc.context.line((ox, y), (ox+self.w, y))

        capHeight = doc.context.fontCapHeight()
        y = oy + baseline + capHeight
        doc.context.line((ox, y), (ox+self.w, y))

        y = oy + baseline + descender
        doc.context.line((ox, y), (ox+self.w, y)) # Descender

        y = oy + baseline + self.fontSize + descender
        doc.context.line((ox, y), (ox+self.w, y)) # Descender

class Waterfall(Element):
    """The GlyphView show single glyphs with metrics lines.

    >>> from pagebotnano.document import Document
    >>> pad = 30
    >>> doc = Document(w=400, h=800)
    >>> page = doc.newPage()
    >>> page.padding = pad
    >>> sample = Waterfall.AaBbCc
    >>> e = Waterfall(sample, 'Georgia', x=pad, y=pad, w=page.pw, h=page.ph, fill=0.9)
    >>> page.addElement(e)
    >>> sample = Waterfall.Hamburg
    >>> page = doc.newPage()
    >>> page.padding = pad
    >>> e = Waterfall(sample, 'Georgia', x=pad, y=pad, w=page.pw, h=page.ph, fill=0.9)
    >>> page.addElement(e)

    >>> doc.export('_export/Waterfall.pdf')
    """
    Hamburg = 'Hamburgefonstiv'
    AaBbCc = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'
    DEFAULT_FONTSIZES = (8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 24, 26, 28, 30, 
        32, 36, 40, 44, 48, 52, 56, 60, 64)

    def __init__(self, sample, font, fontSizes=None, align=None, leading=None, **kwargs):
        Element.__init__(self, **kwargs)
        self.sample = sample or self.Hamburg
        self.font = font or 'Georgia'
        self.fontSizes = fontSizes or self.DEFAULT_FONTSIZES
        self.leading = leading or 1.2 # Leading * fontSize factor
        self.align = align or LEFT

    def drawContent(self, ox, oy, doc, page, parent):
        """Draw the content of this single glyph/string fitting, with line indicators
        of vertical metrics.

        TODO: Show more font metrics and glyph metrics here. Add labels of values and names.
        """
        labelStyle = dict(font=self.font, fontSize=7, textFill=0, lineHeight=8, aligh=LEFT)
        style = dict(font=self.font, fontSize=self.fontSizes[0], textFill=0, align=LEFT)
        bs = BabelString('', style)
        tw, th = bs.textSize
        for fontSize in self.fontSizes:
            labelLine = BabelString(' %d pt' % fontSize, labelStyle)
            ltw, lth = labelLine.textSize

            style['fontSize'] = fontSize
            style['lineHeight'] = fontSize * self.leading
            sample = self.sample
            textLine = BabelString(sample, style)
            stw, sth = textLine.textSize

            while sample and self.w and stw + ltw > self.w: 
                # If not fitting, shorten the string until it does
                sample = sample[:-1]
                textLine = BabelString(sample, style)
                stw, sth = textLine.textSize
            if self.h and th + sth > self.h:
                break # No vertical space left, skip the rest of the fontSizes. 
            
            bs += BabelString('\n'+sample, style) + labelLine # There still is vertical space, add the textLine
            tw, th = bs.textSize

        e = Text(bs, x=ox, y=oy+self.h)
        page.addElement(e)

class Stacked(Element):
    """The GlyphView show single glyphs with metrics lines.

    >>> from pagebotnano.document import Document
    >>> pad = 30
    >>> doc = Document(w=200, h=800)
    >>> page = doc.newPage()
    >>> page.padding = pad
    >>> e = Stacked(Stacked.WORDS*4, 'Georgia', x=pad, y=pad, w=page.pw, h=page.ph, capsOnly=True, fill=0.9)
    >>> page.addElement(e)

    >>> doc.export('_export/Stacked.pdf')
    """
    WORDS = ('The', 'Quick Brown', 'Fox', 'Jumps', 'Over', 'The Lazy', 'Dog')

    def __init__(self, words, font, leading=None, w=None, h=None, capsOnly=False, 
        **kwargs):
        Element.__init__(self, **kwargs)
        self.words = words or self.WORDS
        self.font = font or 'Georgia'
        self.leading = leading or 1.2 # Leading * fontSize factor
        self.w = w or 200 # Make sure there is default size.
        self.h = h or 400
        self.capsOnly = capsOnly

    def drawContent(self, ox, oy, doc, page, parent):
        """Draw the content of this single glyph/string fitting, with line indicators
        of vertical metrics.

        TODO: Show more font metrics and glyph metrics here. Add labels of values and names.
        TODO: Better vertical positioning
        """
        y = self.h
        style = dict(font=self.font, textFill=0, lineHeight=10, align=LEFT)
        for word in self.words:
            if self.capsOnly:
                word = word.upper()
            style['fontSize'] = 100 # Start with large guess of fontSize
            textLine = BabelString(word, style) 
            tlw, tlh = textLine.textSize

            style['fontSize'] *= self.w / tlw
            style['lineHeight'] = style['fontSize'] * self.leading
            textLine = BabelString(word, style) # Get a new scaled version
            tlw, tlh = textLine.textSize
            if tlh > y: # Not fitting this word vertical anymore, try other.
                continue

            e = Text(textLine, x=ox, y=oy+y-tlh)
            page.addElement(e)
            y -= tlh

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
