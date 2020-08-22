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
SW = 200 # Square size

# Create a new page canvas of 1000 x 1000 px
drawBot.newPage(W, H)
# Fill page with white background
drawBot.fill(1)
drawBot.rect(0, 0, W, H)
# Set fill color to red (r, g, b)
drawBot.fill(0, 0.5, 0)
# Draw a black square (x, y, width, height)
drawBot.oval(M, M, SW, SW)
drawBot.oval(M, W-M-SW, SW, SW)
drawBot.oval(W-M-SW, H-M-SW, SW, SW)
drawBot.oval(W-M-SW, M, SW, SW)
# Export as png file in created _export folder (that does not sync in Github)
export('_export/0012-CirclesPar.png')
