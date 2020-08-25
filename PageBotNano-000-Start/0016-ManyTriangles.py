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
import os
import drawBot

W = H = 600
M = 50
TW = 20 # Triangle size
TH = 18

# Create a new page canvas of 1000 x 1000 px
drawBot.newPage(W, H)
# Fill page with white background
drawBot.fill(1)
drawBot.rect(0, 0, W, H)
for n in range(200):
    # Random position within the page range
    x = M + random()*(W-M-M-TW)
    y = M + random()*(H-M-M-TW)
    # Set a random color
    drawBot.fill(random(), random(), random())
    path = drawBot.BezierPath()
    path.moveTo((x, y))
    path.lineTo((x+TW, y))
    path.lineTo((x+TW/2, y+TH))
    path.closePath()
    drawBot.drawPath(path)

# Check is the _export/ folder exists, otherwise create it.
# We want to save exported files there, to avoid that those files get 
# committed to Github everytime a new one is exported.
if not os.path.exists('_export'):
    os.path.mkdir('_export/')
# Export as png file in created _export folder (that does not sync in Github)
drawBot.saveImage('_export/0016-ManyTriangles.png')
