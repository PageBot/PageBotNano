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
#   Generate tab figures from figures if they don't exists.
#   Check on equal tab spacing if they do exist.
#
import os
# Include the openFont and copyGlyph function here, instead of the import, 
# in case this script is not running inside the current folder.
from pagebotnano_025 import openFont, copyGlyph

TAB_WIDTH = 630 # Standard tab width for all masters
FIGURES = ('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'zero')
PATH = 'masters/'

for fileName in os.listdir(PATH): # For all .ufo files in the masters/ folder
    if fileName.startswith('.'):
        continue # Skip anything that is not a ufo file
    font = openFont(PATH+fileName) # Open then font without opening a FontWindow
    print('Checking', font.path)
    for gName in FIGURES: # Just doing from original figures
        if gName in font: # Only figure does exist already
            g = font[gName] # Get the figure glyph
            tabName = gName + '.tab' # Make the new figure.tab name
            if not tabName in font: # Only if it does not exists 
                copyGlyph(font, gName, font, tabName) # Copy the original to the .tab
                diff = TAB_WIDTH - g.width # Calculate the difference in width
                tabGlyph = font[tabName] # Set the tab width and center the figure
                tabGlyph.leftMargin += diff/2 # First set the margin
                tabGlyph.width = TAB_WIDTH # Then set the width
                print('Creating tab figure', tabName, 'on width', TAB_WIDTH)
    font.save()
    font.close() # Does not do anything in this script.

print('Done')


