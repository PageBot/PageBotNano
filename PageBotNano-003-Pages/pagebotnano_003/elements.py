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
#   elements.py
#
#   This source contains the class with knowledge about elements that
#   can be placed on a page.
#
class Element:
    # Class names start with a capital. See a class as a factory
    # of element objects (name spelled with an initial lower case.)
    
    def build(self, doc, page):
    	"""For now it will do nothing, but that will change."""
    	