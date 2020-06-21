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
print('SketchPage:', sketchPage) # SketchPage: <SketchPage name=Page 1>
"""
>>> page, api.page
(<SketchPage name=Page 1>, <SketchPage name=Page 1>)
>>> page.name
'Page 1'
>>> len(page.layers[0]), page.artBoards, len(page.artBoards[0])
(7, [<SketchArtboard name=Artboard 1 w=576 h=783>], 7)
>>> artBoard = page.artBoards[0]
>>> e = artBoard.layers[3]
>>> e, e.name
(<SketchRectangle name=Rectangle Middle Right>, 'Rectangle Middle Right')
>>> e = page.find(pattern='Top Left')[0]
>>> e.name, e.frame
('Rectangle Top Left', <SketchRect x=60 y=0 w=216 h=168>)
>>> #e.style['fills']
"""
print('Done')