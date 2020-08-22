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
#	Example inspired by https://www.drawbot.com/content/shapes/drawingPath.html
#
import sys
import drawBot
from math import sin, cos, radians

if __name__ == "__main__":
    sys.path.insert(0, "..") # So we can import pagebotnano003 without installing.

from pagebotnano_000 import export

W = H = 300
M = 10
R = W/2 - 2*M
LINES = 50 # Number of lines to draw

# Create a new page canvas of 1000 x 1000 px
drawBot.newPage(W, H)
# Fill page with white background
drawBot.fill(1)
drawBot.rect(0, 0, W, H)

# Cmd-drag these values in DrawBotApp to see interactive 
pt0 = 74, 48
pt1 = 238, 182
pt2 = 46, 252
radius = 60

def drawPt(pos, r=5):
    x, y = pos
    drawBot.oval(x-r, y-r, r*2, r*2)

drawBot.fill(None)

path = drawBot.BezierPath()
path.moveTo(pt0)
path.arcTo(pt1, pt2, radius)
path.lineTo(pt2)

drawBot.stroke(0, 1, 1)
drawBot.polygon(pt0, pt1, pt2)
for pt in [pt0, pt1, pt2]:
    drawPt(pt)

drawBot.stroke(0, 0, 1)
drawBot.drawPath(path)
drawBot.stroke(1, 0, 1)
for pt in path.onCurvePoints:
    drawPt(pt, r=3)
for pt in path.offCurvePoints:
    drawPt(pt, r=2)

# Export as png file in created _export folder (that does not sync in Github)
export('_export/0030-Arcs.png')
