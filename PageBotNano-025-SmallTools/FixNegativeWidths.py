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

TESTING = True
DEFAULT_WIDTH = 111
PATH = 'masters/' # Check all .ufo in this local folder
REPORT_PATH = 'reports/' # Create folder if not exists, export report file there.


def fixNegativeWidths(filePath):
    report = [] # Collect errors and warnings in this list
    font = openFont(filePath) # Open the font as instance (not opening a window)

    if TESTING: # Introduce an error, so we test the script
        font['H'].width = -200
        font['O'].width = -500

    # Display the font as header of the errors/warning with a marker line.
    report.append('-'*80)
    report.append('Checking %s Groups %d Kerning %d' % (font.path, len(font.groups), len(font.kerning)))

    # Report if glyph.width < 0, then set it to DEFAULT_WIDTH
    for g in font: # For all glyphs in the font
        if g.width < 0:
            report.append('Error: Glyph %s has negative width (%d)' % (g.name, g.width))
            g.width = DEFAULT_WIDTH
        elif g.width == DEFAULT_WIDTH:
            report.append('Warning: Glyph %s has DEFAULT_WIDTH (%d)' % (g.name, g.width))

    report.append('Saving font')
    font.save()
    font.close() # Does not do+anything in this script.
    return report

#print('This is included as', __name__)
if __name__ == "__main__":
    for fileName in os.listdir(PATH):
        if fileName.startswith('.') or not fileName.endswith('.ufo'):
            continue
        fontPath = PATH + fileName
        report = fixNegativeWidths(fontPath)

        # If the report folder does not exist yet, create it
        if not os.path.exists(REPORT_PATH):
            print('Creating', REPORT_PATH)
            os.makedirs(REPORT_PATH)
        # Write the errors/warnings file, glueing the separate lines with '\n' newline
        print('Errors and warnings: %d' % len(report))
        f = codecs.open(REPORT_PATH + 'negativeWidth_errors_warnings.txt', 'a', encoding='utf-8')
        f.write('\n'.join(report))
        f.close()

    print('Done')

