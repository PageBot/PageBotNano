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

if __name__ == "__main__":
    sys.path.insert(0, "..") # So we can import pagebotnano003 without installing.

from pagebotnano_000 import export

W = H = 600
M = 50
INSET = 150

# Create a new page canvas of 1000 x 1000 px
drawBot.newPage(W, H)
# Fill page with white background
drawBot.fill(1)
drawBot.rect(0, 0, W, H)
# Set fill color to red (r, g, b)
drawBot.fill(0.2, 0.2, 1)
# Draw a polygon with x-amount of points
drawBot.polygon(
	(M, M), (M+INSET, W/2), (M, H-M), # Left
	(W/2, H-M-INSET), # Top
	(W-M, H-M), (W-M-INSET, H/2), (W-M, M), # Right
	(W/2, INSET), # Bottom
	close=True)
# Export as png file in created _export folder (that does not sync in Github)
export('_export/0020-PolygonPar.png')
