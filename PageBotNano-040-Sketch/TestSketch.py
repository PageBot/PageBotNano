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

path = 'pysketch/Resources/TemplateSquare.sketch'

api = SketchApi(path) # See pysketch/sketchapi.py for interface specs.
print('SketchFile:', api.sketchFile) # <SketchFile path=TemplateSquare.sketch>
print('Path:', api.sketchFile.path) # The api stores the path of the Sketch file

sketchPage = api.selectPage(0) # SketchPage instance, not PageBotNano Page.
print('Sketch Page:', sketchPage) # SketchPage: <SketchPage name=Page 1>
print('Page name:', sketchPage.name) # 'Page 1' 
# Since Sketch has pages with artboards, we'll use this extra layer
# as follows:
# sketchPage --> PageBotNano Document
# stetchArtBoard --> PageBotNano Page
artBoard = sketchPage.artBoards[0] 
print('Sketch ArtBoard:', artBoard) # <SketchArtboard name=Artboard 1 w=576 h=783>
# Get one of the rectangles on this artBoard
e = artBoard.layers[3]
print('Element[3] name:', e.name) # 'Rectangle Middle Right'
# Find the element with this name
e = sketchPage.find(pattern='Top Left')[0]
print('Found element name:', e.name) # 'Rectangle Top Left'
print('Found element frame:', e.frame) # <SketchRect x=60 y=0 w=216 h=168>

print('Done')