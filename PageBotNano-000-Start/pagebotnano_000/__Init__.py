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

def export(path):
	dirPath = '/'.join(path.split('/')[:-1])
	if not os.path.exists(dirPath):
		os.makedirs(dirPath)
	drawBot.saveImage(path)
