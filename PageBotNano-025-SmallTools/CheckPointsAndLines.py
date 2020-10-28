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
#    Check on exact vertical/horizontal lines (within margin)
#    Check on off-curves in extremes that are not vertical/horizontal
#   
import os, codecs
# Include the openFont and copyGlyph function here, instead of the import, 
# in case this script is not running inside the current folder.
from pagebotnano_025 import openFont, copyGlyph

PATH = 'masters/'

def getPointContext(pts, i):
    return pts[i-6],pts[i-5],pts[i-4],pts[i-3],pts[i-2],pts[i-1],pts[i]

MARGIN = 10

REPORT_PATH = 'reports/' # Create folder if not exists, export report file there.

report = [] # Collect errors and warnings in this list

for fileName in os.listdir(PATH): # For all fonts in the masters/ folder   
    if not fileName.endswith('.ufo'): 
        continue # Skip all that is not a .ufo file.
    font = openFont(PATH+fileName)
    report.append('-'*80+'\nChecking %s' % font.path)
    for g in font:
        if g.name != 'C':
            continue
        #for cIndex, contour in enumerate(g.contours): 
        #    for sIndex, segment in enumerate(contour): # If looking at space between on-curves
        #        print(cIndex, sIndex, segment)
        #
        for cIndex, contour in enumerate(g.contours): 
            points = contour.points
            for pIndex in range(len(points)):
                p_3, p_2, p_1, p, p1, p2, p3 = getPointContext(points, pIndex)
                #if p.type == 'offcurve' or p1.type == 'offcurve':
                if 'offcurve' not in (p.type, p1.type):
                    if abs(p.x - p1.x) <= MARGIN and p.x != p1.x:
                        report.append('Vertical off: Index:%d Offset:%d Type=%s p=%s p1=%s' % (pIndex-3, abs(p.x - p1.x), p.type, (p.x, p.y), (p1.x, p1.y)))
                    if abs(p.y - p1.y) <= MARGIN and p.y != p1.y:
                        report.append('Horizontal off: Index:%d Offset:%d Type=%s p=%s p1=%s' % (pIndex-3, abs(p.y - p1.y), p.type, (p.x, p.y), (p1.x, p1.y)))
                if p.type != 'offcurve' and p_1.type == 'offcurve' and p1.type == 'offcurve':
                    if abs(p_1.x - p.x) <= MARGIN and p.x != p_1.x:
                        report.append('Vertical off: Index:%d Offset:%d Type=%s p_1=%s p=%s' % (pIndex-3, abs(p_1.x - p.x), p.type, (p_1.x, p_1.y), (p.x, p.y)))
                    if abs(p.x - p1.x) <= MARGIN and p.x != p1.x:
                        report.append('Vertical off: Index:%d Offset:%d Type=%s p=%s p1=%s' % (pIndex-3, abs(p.x - p1.x), p.type, (p.x, p.y), (p1.x, p1.y)))
                    if abs(p_1.y - p.y) <= MARGIN and p.y != p_1.y:
                        report.append('Horizontal off: Index:%d Offset:%d Type=%s p_1=%s p=%s' % (pIndex-3, abs(p_1.y - p.y), p.type, (p_1.x, p_1.y), (p.x, p.y)))
                    if abs(p.y - p1.y) <= MARGIN and p.y != p1.y:
                        report.append('Horizontal off: Index:%d Offset:%d Type=%s p=%s p1=%s' % (pIndex-3, abs(p.y - p1.y), p.type, (p.x, p.y), (p1.x, p1.y)))
    #font.save()
    #font.close() # Does not do anything in this script.

# If the report folder does not exist yet, create it
if not os.path.exists(REPORT_PATH):
    print('Creating', REPORT_PATH)
    os.makedirs(REPORT_PATH)
# Write the errors/warnings file, glueing the separate lines with '\n' newline
print('Errors and warnings: %d' % len(report))
f = codecs.open(REPORT_PATH + 'check_points_and_lines_warnings.txt', 'w', encoding='utf-8')
f.write('\n'.join(report))
f.close()

print('Done')


