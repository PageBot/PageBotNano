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
#   TypeSpecimen.py
#
from pagebotnano_030.constants import A4
from pagebotnano_030.document import Document
from pagebotnano_030.elements import Rect, Text, GlyphView

W, H = A4
FONT = 'Georgia'
GUTTER = 12

doc = Document(w=W, h=H)
page = doc.newPage()
page.padding = 40

w = page.pw
e1 = GlyphView('A', font=FONT, x=page.pl, y=page.h-page.pt-w, w=w, h=w, fill=0.95)
page.addElement(e1)

w = (page.pw-GUTTER)/2
e2 = GlyphView('Hbj', font=FONT+'-Bold', x=page.pl, y=page.pb, w=w, h=page.pb*3, fill=0.95)
page.addElement(e2)

e3 = GlyphView('Hhj', font=FONT, x=page.pl+w+GUTTER, y=page.pb, w=w, h=page.pb*3, fill=0.95)
page.addElement(e3)

w = (page.pw-GUTTER)/2
e4 = GlyphView('Hbj', font=FONT+'-BoldItalic', x=page.pl, y=page.pb+e3.h, w=w, h=page.pb*3, fill=0.95)
page.addElement(e4)

e5 = GlyphView('Hhj', font=FONT+'-Italic', x=page.pl+w+GUTTER, y=page.pb+e3.h, w=w, h=page.pb*3, fill=0.95)
page.addElement(e5)

doc.export('_export/TypeSpecimen.pdf')
print('Done 030')
