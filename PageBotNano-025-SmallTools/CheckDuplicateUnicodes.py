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
#   This script checks some aspects of the consistency of kerning and groups.
#   In this approach, it is assumed that all kerning is done by groups.
#   Kerning pair (group1, group2) 
#   Kerning pair (group1, glyph2): gives warning, should be (group1, @[glyph2])
#   Kerning pair (glyph1, group2): gives warning, should be (@[glyph1], group2)
#   Kerning pair (glyph1, glyph2): gives warning, should be (@[glyph1], @[glyph2])
#   
#   From a production point of view, this may not seem ideal (adding extra 
#   space to the font file for groups with only one glyph), but it is useful 
#   in the design phase, where glyphs can easily be added to a group, without
#   changing the kerning table. 
#   Single-glyph groups can always be converted later in a productions script,
#   where the other way around is less straight forward.
# 
import os, codecs
# Include the openFont function here, instead of the import, in case this
# script is not running inside the current folder.
from pagebotnano_025 import openFont 

PATH = 'masters/' # Check all .ufo in this local folder
REPORT_PATH = 'reports/' # Create folder if not exists, export report file there.

report = [] # Collect errors and warnings in this list

fonts = [] # Store the processed fonts, so we can compare the groups.

for fileName in os.listdir(PATH): # For all the files in the masters/ folder
    if not fileName.endswith('.ufo'):
        continue # Skip anything that is not a ufo file.
    font = openFont(PATH+fileName) # Open the font as instance (not opening a window)
    fonts.append(font) # Keep the processed font for later comparing of groups.

    # Display the font as header of the errors/warning with a marker line.
    report.append('-'*80)
    report.append('Checking %s Groups %d Kerning %d' % (font.path, len(font.groups), len(font.kerning)))

    # Check on kerning pairs only (group1, group2)
    # Kerning with value 0
    # Glyphs of group1 can only be there once, same with glyphs of group2
    # All glyphs in groups exist
    # Different of groups between all fonts

    # Warning on kerning with value 0
    if 1: # Simple switch to turn on/off on this check.
        for pair, value in font.kerning.items(): 
            if value == 0: #
                report.append('Warning: Kerning %s == 0' % str(pair))
                #del font.kerning[pair] will delete the kerning pair from the font

    # Check on kerning pairs only (group1, group2)
    # Check if all groups exist
    if 1:
        for (name1, name2), value in font.kerning.items():
            if name1 in font.keys(): # If this is a plain existing glyph name
                report.append('Warning: Glyph "%s" in kern1 should be a group' % name1)
            elif not name1 in font.groups: # Otherwise it is a group, check if it exists
                report.append('Error: Group "%s" in kern1 does not exist' % name1)
            if name2 in font.keys(): # If this is a plain existing glyph name
                report.append('Warning: Glyph "%s" in kern2 should be a group' % name2)
            elif not name2 in font.groups: # Otherwise it is a group, check if it exists
                report.append('Error: Group "%s" in kern2 does not exist' % name2)

    # Check if all glyphs in groups exist
    if 1:
        for groupName, group in font.groups.items(): # For all groups
            for glyphName in group: # For all glyphs in each group
                if not glyphName in font.keys(): # Error if the glyph does not exist.
                    report.append('Error: Glyph "%s" in group "%s" does not exist' % (glyphName, groupName))

    if 1:
        # Glyphs of group1 can only be there once, same with glyphs of group2
        # Keep track on the glyphs we already passed
        glyph2Group1 = {} # Glyphs --> groupName on left side of pair
        glyph2Group2 = {} # Glyphs --> groupName on right side of pair
        for groupName, group in font.groups.items(): # For all groups
            for glyphName in group: # For all glyphs in each group
                if 'kern1' in groupName: # If this is a kern1, check on previous in glyph2Group1
                    if glyphName in glyph2Group1:
                        # Glyph already was seen, this is an error, can't be in multiple group1
                        report.append('Error: Glyph "%s" in group "%s" and in group "%s"' % (glyphName, groupName, glyph2Group1[glyphName]))
                    else: # All good, store this glyphName and the name of its group 
                        glyph2Group1[glyphName] = groupName
                elif 'kern2' in groupName:
                    if glyphName in glyph2Group2:
                        # Glyph already was seen, this is an error, can't be in multiple group1
                        report.append('Error: Glyph "%s" in group "%s" and in group "%s"' % (glyphName, groupName, glyph2Group2[glyphName]))
                    else: # All good, store this glyphName and the name of its group 
                        glyph2Group2[glyphName] = groupName


    font.save()
    font.close() # Does not do+anything in this script.

# If the report folder does not exist yet, create it
if not os.path.exists(REPORT_PATH):
    print('Creating', REPORT_PATH)
    os.makedirs(REPORT_PATH)
# Write the errors/warnings file, glueing the separate lines with '\n' newline
print('Errors and warnings: %d' % len(report))
f = codecs.open(REPORT_PATH + 'errors_warnings.txt', 'w', encoding='utf-8')
f.write('\n'.join(report))
f.close()

print('Done')

