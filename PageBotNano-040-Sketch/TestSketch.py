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
#   TestSketch.py
#
#   This TestSketch.py reads the content of a .sketch document, and converts
#   it into a PageBotNano document.
#
from pysketch.sketchapi import SketchApi

class SketchTester:
    """The SketchTest app reads/writes from a template Sketch document.

    >>> path = 'pysketch/Resources/TemplateSquare.sketch'
    >>> api = SketchApi(path) # See pysketch/sketchapi.py for interface specs.
    >>> api.sketchFile # Read the Sketch file into PageBotNano dictionary.
    <SketchFile path=TemplateSquare.sketch>
    >>> api.sketchFile.path # The api stores the path of the Sketch file
    'pysketch/Resources/TemplateSquare.sketch'
    >>> sketchPage = api.selectPage(0) # SketchPage instance, not PageBotNano Page.
    >>> sketchPage
    <SketchPage name=Page 1>
    >>> sketchPage.name
    'Page 1'
    >>> # Since Sketch has pages with artboards, we'll use this extra layer as follows:
    >>> # sketchPage --> PageBotNano Document
    >>> # sketchArtBoard --> PageBotNano Page
    >>> # sketchRectangle --> PageBotNano Rect element
    >>> artBoard = sketchPage.artboards[0]
    >>> artBoard
    <SketchArtboard name=Artboard 1 w=576 h=783>
    >>> # Get one of the rectangles on this artBoard
    >>> ske = artBoard.layers[3]
    >>> ske
    <SketchRectangle name=Rectangle Middle Right>
    >>> se.name
    'Rectangle Middle Right'
    >>> se = sketchPage.find(pattern='Top Left')[0] # Find the element with this name
    >>> se
    <SketchRectangle name=Rectangle Top Left>
    >>> se.frame # SketchRect is a frame with position and size, different from SketchRectangle
    <SketchRect x=60 y=0 w=216 h=168>
    >>> se.frame.x += 400 # Move the rectangle.

    """

if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]
