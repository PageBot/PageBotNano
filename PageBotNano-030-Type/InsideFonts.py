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
from pagebotnano_030.elements import Rect, Text, GlyphView, Stacked
from pagebotnano_030.fonttoolbox.objects.font import Font

fontPath = '../resources/fonts/typetr/PageBot-Bold.ttf'
f = Font(fontPath)

padding = 40
w, h = A4

doc = Document(w=w, h=h)
page = doc.newPage()
page.padding = padding
gv = GlyphView('g', font=f, x=page.pl, y=page.pb, w=page.pw, h=page.ph)
page.addElement(gv)

page = doc.newPage()
st = Stacked(font=f, x=page.pl, y=page.pb, w=page.pw, h=page.ph)
page.addElement(st)
page.padding = padding

doc.export('_export/GlyphViews.pdf')
print('Done 030')
