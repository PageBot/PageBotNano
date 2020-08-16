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
#   TestSketchApi.py
#
#   This TestSketchApi.py reads the content of the Template.sketch document, 
#   does some example drawing and saves it as another .sketch document.
#
from pagebotnano_040.pysketch.sketchapi import SketchApi

api = SketchApi()
print('api:', api) # <SketchApi path=Template.sketch>
print('api.sketchFile:', api.sketchFile) # <SketchFile path=Template.sketch>
print('api.sketchFile.path:', api.sketchFile.path.endswith('pysketch/resources/Template.sketch'))
print('api.filePath == api.sketchFile.path:', api.filePath == api.sketchFile.path)

# Get a SketchPage instance, on the level of PageBotNano Publication
skPage = api.selectPage(0) 
print(skPage, skPage.name) # <SketchPage name=Page 1> 'Page 1'
# Get a SketchArtboard instance, on the level of PageBotNano Page
skArtBoard = skPage.artboards[0] 
print(skArtboard, )
"""

>>> path = 'Resources/TemplateSquare.sketch'
>>> api = SketchApi(path)
>>> page, api.page
(<SketchPage name=Page 1>, <SketchPage name=Page 1>)
>>> page.name
'Page 1'
>>> len(page.layers[0]), page.artboards, len(page.artboards[0])
(6, [<SketchArtboard name=Artboard 1 w=576 h=783>], 6)
>>> e = artBoard.layers[3]
>>> e, e.name
(<SketchShapeGroup name=Rectangle Middle Right>, 'Rectangle Middle Right')
>>> e = page.find(pattern='Top Left')[0]
>>> e.name, e.frame
('Rectangle Top Left', <SketchRect x=60 y=96 w=216 h=168>)

"""
if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]    