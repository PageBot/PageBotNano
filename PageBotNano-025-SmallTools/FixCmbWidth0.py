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
#
#   Set all negative width for all glyphs. Set to 111 (DEFAULT_WIDTH) standard, 
#   so it can be found.
# 
import os, codecs
# Include the openFont function here, instead of the import, in case this
# script is not running inside the current folder.
from pagebotnano_025 import openFont 

TESTING = False
DEFAULT_WIDTH = 111
DEFAULT_RM = 40 # Default right margin for glyphs with zero width error

PATH = 'masters/' # Check all .ufo in this local folder
REPORT_PATH = 'reports/' # Create folder if not exists, export report file there.

report = [] # Collect errors and warnings in this list

for fileName in os.listdir(PATH): # For all the files in the masters/ folder
    if not fileName.endswith('.ufo'):
        continue # Skip anything that is not a ufo file.
    font = openFont(PATH+fileName) # Open the font as instance (not opening a window)

    if TESTING: # Introduce an error, so we test the script
        font['gravecmb'].width = 10

    # Display the font as header of the errors/warning with a marker line.
    report.append('-'*80)
    report.append('Checking %s Cmb glyhps == 0' % font.path)

    # Report if glyph.width < 0, then set it to DEFAULT_WIDTH
    for g in font: # For all glyphs in the font
        if 'cmb' in g.name and g.width != 0:
            report.append('Fixed: Cmb glyph "%s" has non-zero width (%d) to 0' % (g.name, g.width))
            g.width = 0
        elif g.width == 0: # In case accidentally all widths are zero
            report.append('Fixed: Glyph "%s" zero width to right margin %s' % (g.name, DEFAULT_RM))
            g.rightMargin = DEFAULT_RM # Should be g.angledRightMargin in RoboFont

    font.save()
    font.close() # Does not do+anything in this script.

# If the report folder does not exist yet, create it
if not os.path.exists(REPORT_PATH):
    print('Creating', REPORT_PATH)
    os.makedirs(REPORT_PATH)
# Write the errors/warnings file, glueing the separate lines with '\n' newline
print('Errors and warnings: %d' % len(report))
print('\n'.join(report))
f = codecs.open(REPORT_PATH + 'cmbwidthzero_fixed.txt', 'w', encoding='utf-8')
f.write('\n'.join(report))
f.close()

print('Done')

