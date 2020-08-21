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
#   GenerativeDesign.py
#
from pagebotnano_050.elements import Image, Text, Rect, Oval, Image
from pagebotnano_050.document import Document
from pagebotnano_050.babelstring import BabelString
from pagebotnano_050.toolbox.color import color

from pagebotnano_050.contexts.indesign.context import InDesignContext
from pagebotnano_050.contexts.drawbot.context import DrawBotContext
from pagebotnano_050.toolbox import p
if 1:
    context = InDesignContext()
    EXPORT_PATHS = ['JasperMagazine.jsx']
else:
    context = DrawBotContext()
    EXPORT_PATHS = ['_export/Image.pdf']

font = 'Upgrade=Regular' # Is available in Adobe 
styles = {}
styles['h0'] = dict(name='h0', font=font, fontSize=48, leading=44, textFill=color(1, 0, 0))
styles['h1'] = dict(name='h1', font=font, fontSize=24, leading=22, textFill=color(1, 0, 0))
doc = Document(w=510, h=720, context=context)
doc.styles = styles # Overwrite all default styles.
page = doc.newPage()
page.padding = p(4)
fillColor = color(name='red')
scaleType = None #SCALE_TYPE_FITWH # for non-proportional

e = Rect(parent=page, w=p(16), h=p(16), x=p(20), y=p(11), 
	stroke=color(1, 0, 0), strokeWidth=p(2), fill=fillColor)

# Make an oval that fits in this bounding box.
e = Oval(parent=page, w=p(16), h=p(16), x=p(20), y=p(31), 
	stroke=color(1, 0, 0), strokeWidth=p(2), fill=color(c=1, m=0.5, y=0, k=0, a=0.8))

# Make an image element
e = Image('../resources/images/cookbot10.jpg', parent=page, x=page.pl, y=page.pt, 
	w=page.pw, h=page.pw, fill=color(0.5))

"""
page = doc.newPage()
e = Image('../resources/images/cookbot10.jpg', parent=page, x=page.pl, y=page.pt, 
	w=page.pw, h=page.pw, fill=color(0.2))
e = Rect(parent=page, w=p(16), h=p(16), x=p(20), y=p(11), 
	stroke=color(1, 0, 0), strokeWidth=p(2), fill=color(c=1, m=0.5, y=0, k=0, a=0.8))
e = Rect(parent=page, w=p(16), h=p(16), x=page.pl, y=page.pt, fill=color(1, 0, 0))
e = Rect(parent=page, w=p(16), h=p(16), x=page.pl+p(2), y=p(20), 
	fill=color(c=0.5, m=1, y=0, k=0, a=0.5))
bs = BabelString('ABCD EFGH IJKL MNOP', style=doc.styles['h1'])
pad = p(1) # Padding of text in text box
e = Text(bs, parent=page, w=p(16), h=p(8), x=p(34), y=p(22), padding=pad,
	fill=color(c=0, m=0.5, y=1, k=0, a=0.5))

page = doc.newPage()       
e = Image('../resources/images/cookbot10.jpg', parent=page, x=page.pl, y=page.pt, 
	w=page.pw, h=page.pw, fill=color(0.5))
bs = BabelString('@XYZ', style=doc.styles['h0'])
e = Text(bs, parent=page, w=p(26), h=p(8), x=p(14), y=p(22), padding=pad,
	fill=color(c=0, m=0.5, y=1, k=0, a=0.5))

page = doc.newPage()
e = Image('../resources/images/cookbot10.jpg', parent=page, x=page.pl, y=page.pt, 
	w=page.pw, h=page.pw, fill=color(0, 0, 1))
e = Rect(parent=page, w=p(16), h=p(16), x=p(24), y=p(22), fill=color(c=0.5, m=1, y=1, k=0, a=0.5))
bs = BabelString('@EEE', style=doc.styles['h0'])
e = Text(bs, parent=page, w=p(26), h=p(8), x=p(14), y=p(22), padding=pad, 
	fill=color(c=0, m=0.5, y=1, k=0, a=0.5))

page = doc.newPage()
e = Image('../resources/images/cookbot10.jpg', parent=page, x=page.pl, y=page.pt, 
	w=page.pw, h=page.pw, fill=color(1, 0, 0))
e = Rect(parent=page, w=p(16), h=p(16), x=p(24), y=p(22), fill=color(c=0.5, m=1, y=1, k=0, a=0.5))
bs = BabelString('@EEE', style=doc.styles['h0'])
e = Text(bs, parent=page, w=p(26), h=p(8), x=p(14), y=p(22), padding=pad,  
	fill=color(c=0, m=0.5, y=1, k=0, a=0.5))

"""
for exportPath in EXPORT_PATHS:
    doc.export(exportPath)

