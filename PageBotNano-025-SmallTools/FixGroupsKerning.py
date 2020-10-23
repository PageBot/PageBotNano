#!/usr/bin/env python3
# #-*- coding: UTF-8 -*-
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
import os, codecs
from pagebotnano_025 import openFont

# Kerning pair (group1, group2) 
# Kerning pair (group1, glyph2)
# Kerning pair (glyph1, group2)
# Kerning pair (glyph1, glyph2)
# 
TAB_WIDTH = 630

PATH = 'masters/'
REPORT_PATH = 'reports/'

report = []
fixed = []

fonts = []

for fileName in os.listdir(PATH):
    if fileName.startswith('.') or not fileName.endswith('.ufo'):
        continue
    font = openFont(PATH+fileName)
    fonts.append(font)

    report.append('Checking %s Groups %d Kerning %d' % (font.path, len(font.groups), len(font.kerning)))

    # Check on kerning pairs only (group1, group2)
    # Kerning with value 0
    # Glyphs of group1 can only be there once, same with glyphs of group2
    # All glyphs in groups exist
    # Different of groups between all fonts

    # Kerning with value 0
    if 1:
        for pair, value in font.kerning.items():
            if value == 0:
                fixed.append('Remove kerning %s == 0' % str(pair))
                del font.kerning[pair] # will delete the kerning pair from the font

    if 1:
        # Glyphs of group1 can only be there once, same with glyphs of group2
        glyph2Group1 = {} # Glyphs --> groupName on left side of pair
        glyph2Group2 = {} # Glyphs --> groupName on right side of pair
        for groupName, group in font.groups.items():
            for glyphName in group:
                if 'kern1' in groupName:
                    if glyphName in glyph2Group1:
                        report.append('Error: Glyph "%s" in group "%s" and in group "%s"' % (glyphName, groupName, glyph2Group1[glyphName]))
                    else:
                        glyph2Group1[glyphName] = groupName
                elif 'kern2' in groupName:
                    if glyphName in glyph2Group2:
                        report.append('Error: Glyph "%s" in group "%s" and in group "%s"' % (glyphName, groupName, glyph2Group2[glyphName]))
                    else:
                        glyph2Group2[glyphName] = groupName


    # Check on kerning pairs only (group1, group2)
    # All groups exist
    if 1:
        for (name1, name2), value in font.kerning.items():
            if name1 in font.keys():
                if name1 in glyph2Group1:
                    del font.kerning[(name1, name2)]
                    fixed.append('Removed kerning (%s,%s) with value %d' % (name1, name2, value))
                else: # Glyph does not exist in a group
                    del font.kerning[(name1, name2)]
                    groupName1 = 'public.kern1.%s' % name1
                    if groupName1 in f.groups:
                        report.append('Error: Trying to create existing group "%s"' % groupName1)
                    else:
                        f.groups[groupName1] = [name1]
                    fixed.append('Add new group (%s,%s) with value %d' % (groupName1, name2, value))
                    name1 = groupName1
            if name2 in font.keys():
                if name2 in glyph2Group2:
                    del font.kerning[(name1, name2)]
                    fixed.append('Removed kerning (%s,%s) with value %d' % (name1, name2, value))
                else: # Glyph does not exist in a group
                    del font.kerning[(name1, name2)]
                    groupName2 = 'public.kern2.%s' % name2
                    if groupName2 in f.groups:
                        report.append('Error: Trying to create existing group "%s"' % groupName2)
                    else:
                        f.groups[groupName2] = [name2]
                    fixed.append('Add new group (%s,%s) with value %d' % (name1, groupName2, value))

            #elif not name1 in font.groups:
            #    report.append('Error: Group "%s" in kern1 does not exist' % name1)
            #if name2 in font.keys():
            #    report.append('Warning: Glyph "%s" in kern2 should be a group' % name2)
            #elif not name2 in font.groups:
            #    report.append('Error: Group "%s" in kern2 does not exist' % name2)

    # All glyphs in groups exist
    if 0:
        for groupName, group in font.groups.items():
            for glyphName in group:
                if not glyphName in font.keys():
                    report.append('Error: Glyph "%s" in group "%s" does not exist' % (glyphName, groupName))


    font.save()
    font.close() # Does not do+anything in this script.

if not os.path.exists(REPORT_PATH):
    print('Creating', REPORT_PATH)
    os.makedirs(REPORT_PATH)

print('Errors and warnings: %d' % len(report))
f = codecs.open(REPORT_PATH + 'errors_warnings.txt', 'w', encoding='utf-8')
f.write('\n'.join(report))
f.close()

print('Fixed: %d' % len(fixed))
f = codecs.open(REPORT_PATH + 'fixed.txt', 'w', encoding='utf-8')
f.write('\n'.join(fixed))
f.close()

print('Done')

