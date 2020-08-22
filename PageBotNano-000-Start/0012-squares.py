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

# Create a new page canvas of 1000 x 1000 px
drawBot.newPage(1000, 1000)
# Draw a black square (x, y, width, height)
drawBot.rect(100, 100, 500, 500)
# Export as png file in created _export folder (that does not sync in Github)
export('_export/0012-Squares.png')
