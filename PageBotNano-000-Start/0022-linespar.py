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
import sys
import drawBot
from math import sin, cos, radians

if __name__ == "__main__":
    sys.path.insert(0, "..") # So we can import pagebotnano003 without installing.

from pagebotnano_000 import export

W = H = 600
M = 10
R = W/2 - 2*M
LINES = 50 # Number of lines to draw

# Create a new page canvas of 1000 x 1000 px
drawBot.newPage(W, H)
# Fill page with white background
drawBot.fill(1)
drawBot.rect(0, 0, W, H)
# No fill color
drawBot.fill(None)
# Set stroke color to red (r, g, b)
drawBot.stroke(0, 0, 0.5)
drawBot.strokeWidth(4)
# Calculate the middle point of the lines
mx, my = W/2, H/2
for n in range(LINES):
	angle = radians(360/LINES)*n
	drawBot.line((mx, my), (mx+sin(angle)*R, my+cos(angle)*R))
# Export as png file in created _export folder (that does not sync in Github)
export('_export/0022-LinesPar.png')
