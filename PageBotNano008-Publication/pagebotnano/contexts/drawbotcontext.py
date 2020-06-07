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
from pagebotnano.babelstring import BabelString
from pagebotnano.toolbox.color import asRgbaColor

class DrawBotContext:
    
    def newDrawing(self):
        return drawBot.newDrawing()

    def saveImage(self, path, multipage=True):
        return drawBot.saveImage(path, multipage=multipage)

    def fill(self, c):
        if c is None:
            drawBot.fill(None)
        else:
            r, g, b, a = asRgbaColor(c)
            drawBot.fill(r, g, b, a)
        
    def stroke(self, c, strokeWidth=None):
        if strokeWidth is not None:
            self.strokeWidth(strokeWidth)
        if c is None:
            drawBot.stroke(None)
        else:
            r, g, b, a = asRgbaColor(c)
            drawBot.stroke(r, g, b, a)
        
    def strokeWidth(self, strokeWidth):
        drawBot.strokeWidth(strokeWidth)

    def rect(self, x, y, w, h):
        drawBot.rect(x, y, w, h)
                
    def oval(self, x, y, w, h):
        drawBot.rect(x, y, w, h)
    
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
        overFlow = BabelString() 
        overFlow.fs = drawBot.textBox(bs.fs, r) 
        return overFlow # Return this “incomplete” BabelString.

    def textSize(self, bs, w=None, h=None):
        return drawBot.textSize(bs.fs, width=w, height=h)

if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]