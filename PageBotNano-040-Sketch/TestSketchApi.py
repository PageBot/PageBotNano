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
import os
from pagebotnano_040.pysketch.sketchapi import SketchApi
from pagebotnano_040.pysketch.sketchclasses import SketchColor

EXPORT_PATH = '_export/'

api = SketchApi()
print('api:', api) # <SketchApi path=Template.sketch>
print('api.sketchFile:', api.sketchFile) # <SketchFile path=Template.sketch>
print('api.sketchFile.path:', api.sketchFile.path.endswith('pysketch/resources/Template.sketch'))
print('api.filePath == api.sketchFile.path:', api.filePath == api.sketchFile.path)

# Get a SketchPage instance, on the level of PageBotNano Publication
skPage = api.selectPage(0) 
print(skPage, skPage.name) # <SketchPage name=Page 1> 'Page 1'
# Get a SketchArtboard instance, on the level of PageBotNano Page
skArtboard = skPage.artboards[0] 
print(skArtboard)
# Get one of the existing rectangles in the template
e = skArtboard.layers[0]
print(e.style.fills[0].color) #e.__dict__.keys())
e.style.fills[0].color = SketchColor(red=1, green=0, blue=0, alpha=1)
print(e.style.fills[0].color) #e.__dict__.keys())

# Offset the rectangle, visible in the export file that it happened.
print(e, e.frame.x, e.frame.y)
e.frame.x += 50
e.frame.y += 50

# Set the parent layer in the api
#api.layer = skArtboard
#g = api.rect(100, 110, 200, 210, fill=(1, 0, 0.5, 0.25))

if not os.path.exists(EXPORT_PATH):
    os.makedirs(EXPORT_PATH)
api.save(EXPORT_PATH + '/TestSketchApi.sketch')
api.save(EXPORT_PATH + '/TestSketchApi.zip')

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