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
class BaseContext:

    def newDocument(self, w=None, h=None, doc=None):
        raise NotImplementedError

    def newPage(self, w, h):
        raise NotImplementedError
           
    def newDrawing(self):
        raise NotImplementedError

    def saveImage(self, path, multiPage=True):
        raise NotImplementedError

    def fill(self, c):
        raise NotImplementedError
        
    def stroke(self, c, strokeWidth=None):
        raise NotImplementedError
        
    def strokeWidth(self, strokeWidth):
        raise NotImplementedError

    def rect(self, x, y, w, h):
        raise NotImplementedError
                
    def oval(self, x, y, w, h):
        raise NotImplementedError
    
    def line(self, p1, p2):
        raise NotImplementedError
        
    def imageSize(self, path):
        raise NotImplementedError

    def scale(self, sx, sy):
        raise NotImplementedError

    def image(self, path, p):
        raise NotImplementedError

    def text(self, bs, p):
        raise NotImplementedError

    def textBox(self, bs, r):
        raise NotImplementedError

    def textSize(self, bs, w=None, h=None):
        raise NotImplementedError

    def hyphenation(self, flag):
        raise NotImplementedError

if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]