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
#   page.py
#
#   This source contains the class with knowledge about elements that
#   can be placed on a page.
#
import sys
sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

import drawBot
from random import random

from pagebotnano.elements import Element

class Page(Element):
    # Class names start with a capital. See a class as a factory
    # of page objects (name spelled with an initial lower case.)
    # Page being another kind of Element, means that theoretically
    # it can be placed on another page or inside another element.
    def __init__(self, pn=None, **kwargs):
        Element.__init__(self, **kwargs)
        self.pn = pn # Store the page number in the page.

    def __repr__(self):
        # This method is called when print(page) is executed.
        # It shows the name of the class, which can be different, if the
        # object inherits from Page.
        return '<%s pn=%d w=%d h=%d elements=%d>' % (self.__class__.__name__, 
            self.pn, self.w, self.h, len(self.elements))

    def compose(self, doc, page=None, parent=None):
        if page is None:
            page = self
        Element.compose(self, doc, page, parent)

    def addElement(self, e):
        """Add the element to the list of child elements.
        """
        self.elements.append(e)

    def build(self, x=0, y=0, doc=None, **kwargs):
        """Draw the page and recursively make the child elements to draw 
        themselves in DrawBot. The build is “broadcast” to all the elements 
        on the page.

        """
        assert doc is not None, ('%s.build: Document needs to be defined.' % self.__class__.__name__)
        drawBot.newPage(self.w, self.h) # Create a new DrawBot page.
        for element in self.elements:
            # Passing on doc and this page in case an element needs more info.
            # Since this bottom-left corner of the page is the origin for position,
            # set it to default (0, 0).
            # In case a page is used on a spread or for display on another page,
            # (x, y) can have another value.
            element.build(x=x, y=y, doc=doc, page=self, parent=self) 

    # Rough example of implementing HTML/CSS generator in this architecture
    #def build_html(self):
    #   drawBot.newPage(self.w, self.h) # Create a new DrawBot page.
    #   for element in self.elements:
    #     # Passing on doc and this page in case an element needs more info.
    #     # Since this bottom-left corner of the page is the origin for position,
    #     # set it to (0, 0)
    #     element.build_html(x=0, y=0, doc=doc, page=self, parent=self) 

if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]