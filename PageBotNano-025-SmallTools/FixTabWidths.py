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
import os
from pagebotnano_025 import openFont

TAB_WIDTH = 630

PATH = 'masters/'

for fileName in os.listdir(PATH):
    if fileName.startswith('.') or not fileName.endswith('.ufo'):
        continue
    font = openFont(PATH+fileName)
    #print('Family:', font.info.familyName, 'Style:', font.info.styleName, 'Path:', font.path)
    print('Checking', font.path)
    for g in font: # Runs through the glyph, instead of glyph names
        if 'tab' in g.name:
            if abs(g.width - TAB_WIDTH) > 1:
                diff = TAB_WIDTH - g.width
                print('Set tab width', g, TAB_WIDTH, '-->', g.width)
                g.leftMargin += diff/2 # First set the margin
                g.width = TAB_WIDTH # Then set the width
                g.update() 

    font.save()
    font.close() # Does not do+anything in this script.

print('Done')



