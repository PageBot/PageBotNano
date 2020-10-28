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
#   TODO: Extend the checking on component also on transformation matrix
#   component.transformation = (m1, m2, m3, m4, dx, dy)
#   (m1, m2, m3, m4) take care of skewing, scale and rotation. (Not in VF)
#   Production fonts this better be (1, 0, 0, 1)
#   (dx, dy) position of component, works in VF
# 
import os, codecs
# Include the openFont function here, instead of the import, in case this
# script is not running inside the current folder.
from pagebotnano_025 import openFont 

TESTING = True
REPLACE = False # Just do reporting, otherwise set missing references to 'H'
REPLACE_BY = 'H'

PATH = 'masters/' # Check all .ufo in this local folder
REPORT_PATH = 'reports/' # Create folder if not exists, export report file there.

report = [] # Collect errors and warnings in this list

for fileName in os.listdir(PATH): # For all the files in the masters/ folder
    if not fileName.endswith('.ufo'):
        continue # Skip anything that is not a ufo file.
    font = openFont(PATH+fileName) # Open the font as instance (not opening a window)

    if TESTING: # Introduce an error, so we test the script
        for component in font['Agrave'].components:
            if component.baseGlyph == 'A':
                component.baseGlyph = 'HHH' # Does not exist
                break
        
    # Display the font as header of the errors/warning with a marker line.
    report.append('-'*80)
    report.append('Checking %s missing component references' % font.path)

    # Report if glyph.width < 0, then set it to DEFAULT_WIDTH
    for g in font: # For all glyphs in the font
        if g.components:
            for component in g.components:
                #print(g.name, component)
                if component.baseGlyph not in font:
                    if REPLACE:
                        report.append('Fixed: Component in glyph "%s" baseGlyph "%s" changed to "%s"' %
                            (g.name, component.baseGlyph, REPLACE_BY))
                        ccomponent.baseGlyph = REPLACE_BY
                    else:
                        report.append('Warning: Component in glyph "%s" baseGlyph "%s" should change to "%s"' %
                            (g.name, component.baseGlyph, REPLACE_BY))


    if not TESTING:
        font.save()
    font.close() # Does not do+anything in this script.

# If the report folder does not exist yet, create it
if not os.path.exists(REPORT_PATH):
    print('Creating', REPORT_PATH)
    os.makedirs(REPORT_PATH)
# Write the errors/warnings file, glueing the separate lines with '\n' newline
print('Errors and warnings: %d' % len(report))
#print('\n'.join(report))
f = codecs.open(REPORT_PATH + 'fixmissingcomponent_fixed_sortof.txt', 'w', encoding='utf-8')
f.write('\n'.join(report))
f.close()

print('Done')

