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
# 
import os, codecs
# Include the openFont function here, instead of the import, in case this
# script is not running inside the current folder.
from pagebotnano_025 import openFont 

TESTING = False
PATH = 'masters/' # Check all .ufo in this local folder
REPORT_PATH = 'reports/' # Create folder if not exists, export report file there.

report = [] # Collect errors and warnings in this list

for fileName in os.listdir(PATH): # For all the files in the masters/ folder
    if not fileName.endswith('.ufo'):
        continue # Skip anything that is not a ufo file.
    font = openFont(PATH+fileName) # Open the font as instance (not opening a window)

    if TESTING: # Insert error to test on
        font['A'].unicode = 61
        font['B'].unicode = 61

    # Display the font as header of the errors/warning with a marker line.
    report.append('-'*80)
    report.append('Checking %s Groups %d Kerning %d' % (font.path, len(font.groups), len(font.kerning)))

    unicode2Name = {}
    for g in font:
        if g.unicode is None or not g.unicodes: # Only test if there is a unicode set.
            continue
        for u in g.unicodes:
            # In RoboFont g.unicode == g.unicodes[0]
            if u in unicode2Name: # Not just test on the first unicode
                report.append('Error: Glyph "%s" has same unicode %04x as "%s"' % (g.name, u, unicode2Name[u]))
                #print(g.name, g.unicode, g.unicodes)
            else: # Otherwise remember this first glyph name<-->unicode
                unicode2Name[u] = g.name 

    if not TESTING:
        font.save()
    font.close() # Does not do+anything in this script.

# If the report folder does not exist yet, create it
if not os.path.exists(REPORT_PATH):
    print('Creating', REPORT_PATH)
    os.makedirs(REPORT_PATH)
# Write the errors/warnings file, glueing the separate lines with '\n' newline
print('Errors and warnings: %d' % len(report))
print('\n'.join(report))
f = codecs.open(REPORT_PATH + 'duplicateunicode_fixes.txt', 'w', encoding='utf-8')
f.write('\n'.join(report))
f.close()

print('Done')

