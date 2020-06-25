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
#   ThemeSpecimens.py
#
#   This ThemeColors.py shows samples of all standard theme colors,
#   with their closest spot color, CMYK, RGB, CSS hex-color and CSS name.
#
from pagebotnano.document import Document
from pagebotnano.themes import AllThemes, BackToTheCity
from pagebotnano.constants import *
from pagebotnano.elements import Rect, Text
from pagebotnano.elements.colorcell import (ColorCell, OVERLAY, SPOTSAMPLE, 
    COLOR_LABELS, HEX, NAME, RGB, SPOT, CMYK)
from pagebotnano.babelstring import BabelString
from pagebotnano.toolbox import pt
from pagebotnano.toolbox.color import color

H, W = A3 # Reversed maked landscape
PADDING_FACTOR = 0.8
FONT_NAME = 'Upgrade-Medium'
TITLE_SIZE = 20
LABEL_SIZE_FACTOR = 0.5
LEADING = 1.2

def makeColorSpecimen(layoutData):
    pageSize, fontSize, fileName, layout, textColor, labels, extension = layoutData
    labelSize = fontSize * LABEL_SIZE_FACTOR
    labelLeading = labelSize * LEADING

    w, h, = pageSize
    padding = w/14

    doc = Document(w=w, h=h)
    for Theme in AllThemes:
        for mood in (DARK, LIGHT):
            theme = Theme(mood=mood)
            page = doc.newPage()
            page.padding = padding
            cw = page.pw/len(theme.colors[0]) # Column width
            ch = page.ph/len(theme.colors) # Column height
            for shade in range(len(theme.colors[0])):
                for base in range(len(theme.colors)):
                    # Get the color from the theme color matrix and add as rectangle
                    # This is the extened example, instead of using the ColorCell element.
                    c = theme.colors[base][shade]
                    # If textColor not defined, then get it from the theme, based on the
                    # darkness of the current color.
                    if textColor is None:
                        tc = theme.textColor(base, shade)
                    else:
                        tc = textColor
                    labelStyle = dict(font=FONT_NAME, fontSize=labelSize, lineHeight=labelLeading, 
                        fill=tc, align=CENTER)

                    # The ColorCell element takes care of showing the color as rectangle
                    # and the lines of various recipes on top.
                    e = ColorCell(c, x=page.pl+shade*cw, y=page.pb+base*ch, w=cw, h=ch, 
                        layout=layout, labels=labels, style=labelStyle, pb=labelLeading)
                    page.addElement(e)
                    
            # Add background rectangle on top with theme name and mood. getColor(shade, base)
            e = Rect(x=page.pl, y=page.h-page.pt, w=page.pw, h=page.pt, fill=theme.getColor(0,2))
            page.addElement(e)
            titleStyle = dict(font=FONT_NAME, fontSize=fontSize, fill=theme.getColor(-2,2))
            bs = BabelString('%s – %s' % (theme.name, mood), titleStyle)
            tw, th = bs.textSize
            e = Text(bs, x=page.pl+fontSize/2, y=page.h-page.pt*2/3, w=page.pw)
            page.addElement(e)

            footNoteStyle = dict(font=FONT_NAME, fontSize=labelSize, lineHeight=labelLeading, 
                fill=theme.colors[0][4], align=LEFT)
            bs = BabelString('Colors with (parenthesis) are approximated to the closest recipe.', 
                footNoteStyle)
            tw, th = bs.textSize
            e = Text(bs, x=page.pl, y=page.pb-th, w=page.pw)
            page.addElement(e)

            footNoteStyle = dict(font=FONT_NAME, fontSize=labelSize, lineHeight=labelLeading, 
                fill=theme.colors[0][4], align=RIGHT)
            bs = BabelString('Generated by PageBotNano', 
                footNoteStyle)
            tw, th = bs.textSize
            e = Text(bs, x=page.pl+page.pw, y=page.pb-th, w=page.pw)
            page.addElement(e)

    doc.export('_export/ThemeSpecimen-%s.%s' % (fileName, extension), multipage=True)

layoutDatas = (
    # Page size, filename, layout, labelColor, labels
    ((W, H), TITLE_SIZE, OVERLAY, OVERLAY, None, (HEX, NAME, RGB, SPOT, CMYK, ), 'pdf'),
    ((W, H), TITLE_SIZE, SPOTSAMPLE+'1', SPOTSAMPLE, color(0), (HEX, NAME, SPOT), 'pdf'),
    ((A5[1], A5[0]), TITLE_SIZE, SPOTSAMPLE+'-A5', SPOTSAMPLE, color(0), (HEX,), 'pdf'),
    ((A5[1], A5[0]*2/3), TITLE_SIZE, OVERLAY+'-A5ish', SPOTSAMPLE, color(0), (HEX,), 'pdf'),
    ((2160, 2160), TITLE_SIZE*3.6, OVERLAY+'-Instagram', SPOTSAMPLE, color(0), (HEX,), 'jpg'),
)

for layoutData in layoutDatas:
    makeColorSpecimen(layoutData)

print('Done')