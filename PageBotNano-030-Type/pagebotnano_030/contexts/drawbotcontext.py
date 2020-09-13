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
#   drawbotcontext.py
#
import sys
sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

import drawBot
from pagebotnano_030.babelstring import BabelString
from pagebotnano_030.toolbox.color import color, Color

class DrawBotContext:
    
    def newDrawing(self):
        return drawBot.newDrawing()

    def saveImage(self, path, multipage=True):
        return drawBot.saveImage(path, multipage=multipage)

    def newPath(self):
        """Answer a new empty drawBot.BezierPath.

        >>> context = DrawBotContext()
        >>> context.newPath()
        <BezierPath>
        """
        return drawBot.BezierPath()

    def font(self, fontName, fontSize=None):
        """Set the context to this selected font name
        
        >>> context = DrawBotContext()
        >>> context.font('Georgia', 12)
        """
        drawBot.font(fontName, fontSize)

    def fontSize(self, fontSize):
        """Set the context to this selected font name
        
        >>> context = DrawBotContext()
        >>> context.fontSize(12)
        """
        drawBot.fontSize(fontSize)

    def fontContainsCharacters(self, characters):
        """Return a bool if the current font contains the provided characters. 
        Characters is a string containing one or more characters.
        """
        return drawBot.fontContainsCharacters(characters)

    def fontContainsGlyph(self, glyphName):
        """Return a bool if the current font contains a provided glyph name.
        """
        return drawBot.fontContainsGlyph(glyphName)

    def fontFilePath(self):
        """Return the path to the file of the current font."""
        return drawBot.fontFilePath()

    def listFontGlyphNames(self):
        """Return a list of glyph names supported by the current font."""
        return drawBot.listFontGlyphNames()

    def fontDescender(self, font=None, fontSize=None):
        """Returns the current font descender, based on the current font 
        and fontSize."""
        if font is not None:
            drawBot.font(font)
        if fontSize is not None:
            drawBot.fontSize(fontSize)
        return drawBot.fontDescender()

    def fontAscender(self, font=None, fontSize=None):
        """Returns the current font ascender, based on the current font 
        and fontSize."""
        if font is not None:
            drawBot.font(font)
        if fontSize is not None:
            drawBot.fontSize(fontSize)
        return drawBot.fontAscender()

    def fontXHeight(self, font=None, fontSize=None):
        """Returns the current font x-height, based on the current font 
        and fontSize."""
        if font is not None:
            drawBot.font(font)
        if fontSize is not None:
            drawBot.fontSize(fontSize)
        return drawBot.fontXHeight()

    def fontCapHeight(self, font=None, fontSize=None):
        """Returns the current font cap height, based on the current font 
        and fontSize."""
        if font is not None:
            drawBot.font(font)
        if fontSize is not None:
            drawBot.fontSize(fontSize)
        return drawBot.fontCapHeight()

    def fontLeading(self, font=None, fontSize=None):
        """Returns the current font leading, based on the current font 
        and fontSize."""
        if font is not None:
            drawBot.font(font)
        if fontSize is not None:
            drawBot.fontSize(fontSize)
        return drawBot.fontLeading()

    def fontLineHeight(self, font=None, fontSize=None):
        """Returns the current line height, based on the current font and 
        fontSize. If a lineHeight is set, this value will be returned."""
        if font is not None:
            drawBot.font(font)
        if fontSize is not None:
            drawBot.fontSize(fontSize)
        return fontLineHeight()     

    def fill(self, c):
        """Set the fill mode of the context. `c` can be None, a number,
        a name or a Color instance. 

        >>> context = DrawBotContext()
        >>> context.fill(None)
        >>> context.fill('red')
        >>> context.fill((1, 0, 0))
        >>> context.fill(Color(1, 0, 0))
        >>> context.fill(0.5)
        """
        if c is None:
            drawBot.fill(None)
        else: # Make sure is it a Color instance.
            if not isinstance(c, Color):
                c = color(c)
            r, g, b, a = c.rgba
            drawBot.fill(r, g, b, a)
        
    def stroke(self, c, strokeWidth=None):
        """Set the stroke mode of the context. `c` can be None, a number,
        a name or a Color instance. 

        >>> context = DrawBotContext()
        >>> context.stroke(None)
        >>> context.stroke('red')
        >>> context.stroke((1, 0, 0))
        >>> context.stroke(Color(1, 0, 0))
        >>> context.stroke(0.5, 1)
        """
        if strokeWidth is not None:
            self.strokeWidth(strokeWidth)
        if c is None:
            drawBot.stroke(None)
        else: # Make sure it is a Color instance.
            if not isinstance(c, Color):
                c = color(c)
            r, g, b, a = c.rgba
            drawBot.stroke(r, g, b, a)
        
    def strokeWidth(self, strokeWidth):
        drawBot.strokeWidth(strokeWidth)

    def rect(self, x, y, w, h):
        drawBot.rect(x, y, w, h)
                
    def oval(self, x, y, w, h):
        drawBot.rect(x, y, w, h)
    
    def line(self, p1, p2):
        drawBot.line(p1, p2)
        
    def imageSize(self, path):
        return drawBot.imageSize(path)

    def scale(self, sx, sy):
        drawBot.scale(sx, sy)

    def image(self, path, p):
        drawBot.image(path, p)

    def _asFs(self, bs):
        if isinstance(bs, BabelString):
            return bs.fs
        return str(bs)

    def text(self, bs, p):
        """Using the BabelString bs.fs proporty, the BabelString
        us forced to answer the DrawBot.FormattedString version
        of the string.
        """
        drawBot.text(self._asFs(bs), p)

    def textBox(self, bs, r):
        # Set the cache from the overflow, we don't have the source anymore
        overFlow = BabelString(hyphenation=bs.hyphenation) 
        overFlow.fs = drawBot.textBox(self._asFs(bs), r) 
        return overFlow # Return this “incomplete” BabelString.

    def textSize(self, bs, w=None, h=None):
        return drawBot.textSize(self._asFs(bs), width=w, height=h)

    def FormattedString(self, txt, **kwargs):
        if 'fill' in kwargs and isinstance(kwargs['fill'], Color):
            kwargs['fill'] = kwargs['fill'].rgb
        if 'stroke' in kwargs and isinstance(kwargs['stroke'], Color):
            kwargs['stroke'] = kwargs['stroke'].rgb
        return drawBot.FormattedString(txt, **kwargs)

    def hyphenation(self, flag):
        """Set the hyphenation flag in DrawBot canvas. Note that this only
        works while drawing the TextBox, not when creating the FormattedString.
        """
        drawBot.hyphenation(flag)

if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]