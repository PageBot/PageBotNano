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

from pagebotnano.elements import Element, Rect, Line
from pagebotnano.babelstring import BabelString
from pagebotnano.toolbox.color import noColor, color
from pagebotnano.constants import CENTER

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
    >>> e = GlyphView('Georgia', 'Hhj', x=pad, y=pad, w=page.pw, h=page.ph, fill=0.9)
    >>> page.addElement(e)
    >>> doc.export('_export/GlyphView.pdf')
    """
    def __init__(self, font, glyphName, **kwargs):
        Element.__init__(self, **kwargs)
        self.font = font
        self.glyphName = glyphName

    def drawContent(self, ox, oy, doc, page, parent):
        fontSize = self.h
        style = dict(font=self.font, fontSize=fontSize, textFill=0, align=CENTER)
        bs = BabelString(self.glyphName, style=style)
        tw, th = bs.textSize
        if self.w and tw > self.w: # If width of self defined and string is wider
            # Interpolate the fontSize from the measured width
            fontSize = self.w * fontSize / tw
            # Make a new string with the fitting fontSize
            style = dict(font=self.font, fontSize=fontSize, align=CENTER)
            bs = BabelString(self.glyphName, style=style)
            tw1, th1 = bs.textSize

        doc.context.font(self.font, fontSize) # Set to new fontSize, so metrics do fit
        descender = doc.context.fontDescender()
        baseline = (self.h - fontSize)/2 - descender
        
        y = oy + baseline
        doc.context.font(self.font, fontSize)
        doc.context.text(bs, (ox+self.w/2, y))

        doc.context.stroke((0, 0, 1), 0.5)
        doc.context.line((ox, y), (ox+self.w, y)) # Baseline

        xHeight = doc.context.fontXHeight()
        y = oy + baseline + xHeight
        doc.context.line((ox, y), (ox+self.w, y))

        capHeight = doc.context.fontCapHeight()
        y = oy + baseline + capHeight
        doc.context.line((ox, y), (ox+self.w, y))

        y = oy + baseline + descender
        doc.context.line((ox, y), (ox+self.w, y)) # Descender

        y = oy + baseline + fontSize + descender
        doc.context.line((ox, y), (ox+self.w, y)) # Descender

        """
        Font Properties
        fontContainsCharacters(characters)
        Return a bool if the current font contains the provided characters. Characters is a string containing one or more characters.

        fontContainsGlyph(glyphName)
        Return a bool if the current font contains a provided glyph name.

        fontFilePath()
        Return the path to the file of the current font.

        listFontGlyphNames()
        Return a list of glyph names supported by the current font.

        fontDescender()
        Returns the current font descender, based on the current font and fontSize.

        fontAscender()
        Returns the current font ascender, based on the current font and fontSize.

        fontXHeight()
        Returns the current font x-height, based on the current font and fontSize.

        fontCapHeight()
        Returns the current font cap height, based on the current font and fontSize.

        fontLeading()
        Returns the current font leading, based on the current font and fontSize.

        fontLineHeight()
        Returns the current line height, based on the current font and fontSize. If a lineHeight is set, this value will be returned.       
        """

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
