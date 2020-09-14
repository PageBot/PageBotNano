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
#   MakeDocumentJS.py
#
#   This script creates a Sketch-API based Javascript, that creates an example
#   document, running it inside SketchApp.
#

from pagebotnano_040.contexts.sketchjs.context import SketchJSContext

context = SketchJSContext()

if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]    