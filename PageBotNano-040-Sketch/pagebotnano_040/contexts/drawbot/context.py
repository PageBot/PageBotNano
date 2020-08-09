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
sys.path.insert(0, "../../../") # So we can import pagebotnano without installing.

import drawBot
from pagebotnano_040.babelstring import BabelString
from pagebotnano_040.toolbox.color import color, Color

class DrawBotContext:
    
    def newDrawing(self):
        return drawBot.newDrawing()

    def saveImage(self, path, multipage=True):
        return drawBot.saveImage(path, multipage=multipage)

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

    def text(self, bs, p):
        """Using the BabelString bs.fs proporty, the BabelString
        us forced to answer the DrawBot.FormattedString version
        of the string.
        """
        drawBot.text(bs.fs, p)

    def textBox(self, bs, r):
        # Set the cache from the overflow, we don't have the source anymore
        overFlow = BabelString(hyphenation=bs.hyphenation) 
        overFlow.fs = drawBot.textBox(bs.fs, r) 
        return overFlow # Return this “incomplete” BabelString.

    def textSize(self, bs, w=None, h=None):
        return drawBot.textSize(bs.fs, width=w, height=h)

    def hyphenation(self, flag):
        """Set the hyphenation flag in DrawBot canvas. Note that this only
        works while drawing the TextBox, not when creating the FormattedString.
        """
        drawBot.hyphenation(flag)

if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]