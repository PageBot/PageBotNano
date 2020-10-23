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
#   Delete tab figures if they exists.
#   
import os
# Include the openFont and copyGlyph function here, instead of the import, 
# in case this script is not running inside the current folder.
from pagebotnano_025 import openFont, copyGlyph

FIGURES = ('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'zero')
PATH = 'masters/'

for fileName in os.listdir(PATH): # For all fonts in the masters/ folder   
	if not file.endswith('.ufo'): 
		continue # Skip all that is not a .ufo file.
	font = openFont(PATH+fileName)
	print('Checking', font.path)
	for gName in FIGURES:
		if gName in font:
			tabName = gName + '.tab'
			if tabName in font:
				font.removeGlyph(tabName)
				print('Deleting tab figure', tabName)
	font.save()
	font.close() # Does not do anything in this script.

print('Done')


