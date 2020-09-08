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

from random import shuffle, choice
import drawBot

from pagebotnano_030.elements import Element, Rect, Line, Text
from pagebotnano_030.babelstring import BabelString
from pagebotnano_030.toolbox.color import noColor, Color
from pagebotnano_030.constants import CENTER, LEFT
from pagebotnano_030.fonttoolbox.objects.font import Font

FONT_NAME = 'Verdana'
LABEL_SIZE = 10
LEADING = 13

class GlyphView(Element):
    """The GlyphView show single glyphs with metrics lines.

    >>> from pagebotnano_030.document import Document
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
        if isinstance(font, Font):
            font = font.path
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

        # Set the context to font and fontSize, so we get the right descender back.
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

    >>> from pagebotnano_030.document import Document
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
        page.h = page.pb + page.pt + th
        page.addElement(e)

class Stacked(Element):
    """The GlyphView show single glyphs with metrics lines.

    >>> from random import shuffle
    >>> from pagebotnano_030.document import Document
    >>> from pagebotnano_030.constants import SPORTS
    >>> pad = 30
    >>> words = list(SPORTS)
    >>> shuffle(words)
    >>> doc = Document(w=400, h=800)
    >>> page = doc.newPage()
    >>> page.padding = pad
    >>> font = 'Verdana'
    >>> e = Stacked(words, font, x=pad, y=pad, w=page.pw, h=page.ph, gh=12, capsOnly=True, fill=0.9)
    >>> page.addElement(e)
    >>> #doc.export('_export/Stacked-%s.pdf' % font)
    >>> doc.export('_export/Stacked-%s.jpg' % font) # Generating for Instagram
    """
    WORDS = ('The', 'Quick Brown', 'Fox', 'Jumps', 'Over', 'The Lazy', 'Dog')

    def __init__(self, words=None, font=None, fontChoice=None, leading=None, w=None, h=None, 
        theme=None, capsOnly=False, gh=None, **kwargs):
        Element.__init__(self, **kwargs)
        if words is None:
            woefd = self.WORDS
        self.words = list(words)
        self.fontChoice = fontChoice # If defined, choose randomly
        self.font = font or 'Georgia' # otherwise use this one.
        self.leading = leading or 1 # Leading * fontSize factor
        self.gh = gh or 0 # Vertical fixed gutter instead of relative leading.
        self.w = w or 200 # Make sure there is default size.
        self.h = h or 400
        self.capsOnly = capsOnly
        self.theme = theme # Choice for random colors, if defined.

    def drawContent(self, ox, oy, doc, page, parent):
        """Draw the content of this single glyph/string fitting, with line indicators
        of vertical metrics.

        TODO: Show more font metrics and glyph metrics here. Add labels of values and names.
        TODO: For large sizes, compensate for the side beatings of straight stems.
        """
        y = self.h
        for word in self.words:
            if self.fontChoice:
                fontName = choice(self.fontChoice)
            else:
                fontName = self.font
            if self.theme is None:
                textColor = Color(0)
            else:
                textColor = self.theme.randomTextColor
            style = dict(font=fontName, textFill=textColor, align=LEFT)
            if self.capsOnly:
                word = word.upper()
            style['fontSize'] = fontSize = 100 # Start with large guess of fontSize
            textLine = BabelString(word, style) 
            tlw, tlh = textLine.textSize

            style['fontSize'] = fontSize = fontSize * self.w / tlw
            textLine = BabelString(word, style) # Get a new scaled version
            tlw, tlh = textLine.textSize
            if tlh > y: # Not fitting this word vertical anymore, try other.
                continue

            if self.capsOnly:
                y -= doc.context.fontCapHeight(self.font, fontSize)
            else:
                y -= doc.context.fontAscender(self.font, fontSize)
            e = Text(textLine, x=ox, y=oy+y)
            page.addElement(e)
    
            if not self.capsOnly:
                y += doc.context.fontDescender(self.font, fontSize)
            y -= fontSize * (self.leading - 1) + self.gh

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
