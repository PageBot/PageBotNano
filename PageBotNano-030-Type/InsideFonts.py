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
#   InsideFonts.py
#
import os
from pagebotnano_030.constants import A4
from pagebotnano_030.document import Document
from pagebotnano_030.elements import Rect, Text, GlyphView
from pagebotnano_030.fonttoolbox.objects.font import font

FONT_PATH = '../../resources/fonts/typetr/PageBot-Bold.ttf'
print(os.path.exists(FONT_PATH))

doc.export('_export/GlyphViews.pdf')
print('Done 030')
