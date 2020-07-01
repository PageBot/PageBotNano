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
import drawBot
from random import random

class Page:
    # Class names start with a capital. See a class as a factory
    # of page objects (name spelled with an initial lower case.)
    def __init__(self, w, h, pn):
        self.w = w
        self.h = h
        self.pn = pn # Store the page number in the page.
        # Store the elements on the page here. Start with an empty list.
        self.elements = []

    def build(self, doc):
        """Recursively make the pages to draw themselves in DrawBot.
        The build is “broadcast” to all the elements on the page.

        """
        drawBot.newPage(self.w, self.h) # Create a new DrawBot page.
        for element in self.elements:
            # Passing on doc and this page in case an element needs more info.
            element.build(doc, self) 


        # Now let DrawBot do its work, creating the page and saving it.
        # For now to have something visible.
        # Fill the page with a random dark color (< 50% for (r, g, b))
        drawBot.fill(random()*0.5, random()*0.5, random()*0.5)
        drawBot.rect(0, 0, self.w, self.h)
        fs = drawBot.FormattedString('My specimen\nPage %d' % self.pn, 
            font='Georgia', fontSize=80, fill=1)
        drawBot.text(fs, (50, self.h-100))
