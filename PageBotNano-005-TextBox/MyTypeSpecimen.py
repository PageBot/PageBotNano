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
#   MyTypeSpecimen.py
#
#   This MyTypeSpecimen.py shows an example how to import
#   existing libaries, that contain knowledge about document,
#   pages and the elements on the pages.
#
from random import random
import drawBot
# From the library we import the classes (=object factories)
# that we need for creating the type specimen.
# Classes can be recognised by their initial capital name.
from pagebotnano_005.document import Document
from pagebotnano_005.elements import Rect, Text, TextBox
from pagebotnano_005.toolbox.loremipsum import loremipsum

PAD = 48
G = 8

font = 'ACaslonPro-Bold'
titleStyle = dict(font=font, fontSize=14)
pageNumberStyle = dict(font=font, fontSize=14, align='right')
lineStyle = dict(font=font, fontSize=None, lineHeight=None)
labelTabStyle = dict(font=font, fontSize=9, lineHeight=9, tabs=((24, 'right'), (24+G, 'left')))
labelStyle = dict(font=font, fontSize=9, lineHeight=9)
glyphStyle = dict(font=font, fontSize=36, lineHeight=38, tracking=0)

class TypeSpecimen(Document):
    def __init__(self, font, **kwargs):
        Document.__init__(self, **kwargs)
        self.font = font
        
    def initializePage(self, page):
        """Initialize the basic elements on @page.
        Add the name of the font, horizontal ruler on top and bottom.
        Add a pagenumber.
        """
        pw = page.w-2*PAD # Usable page width
        fs = Text.FS(self.font, **titleStyle)
        e = Text(fs, x=PAD, y=page.h-PAD*4/5)
        page.addElement(e)
        # Add line as thin rectangle to avoid making Line class here
        e = Rect(x=PAD, y=page.h-PAD, w=pw, h=1, fill=0)
        page.addElement(e)
        e = Rect(x=PAD, y=PAD, w=pw, h=1, fill=0)
        page.addElement(e)
        # Add page number
        fs = Text.FS(str(page.pn), **pageNumberStyle)
        e = Text(fs, x=page.w-PAD, y=PAD*2/3)
        page.addElement(e)

    def makeWaterfall(self, page, s):
        pw = page.w-2*PAD # Usable page width
        ph = page.h-2*PAD # Usable page height
        fontSize = (8,9,10,11,12,13,14,15,16,18,20,22,24,26,28,32,36,40,
            44,48,52,56)
        fs = Text.FS('')
        for size in fontSize:
            lineStyle['fontSize'] = size
            lineStyle['lineHeight'] = size # To be sure, in case label is behind
            labelTabStyle['lineHeight'] = size * 1.2 # Label defines lineHeight
            fs += Text.FS('\t%dpt\t' % size, **labelTabStyle)
            fs += Text.FS(s+'\n', **lineStyle)
        e = TextBox(fs, x=PAD, y=PAD+8, w=pw, h=ph-24, fill=1)
        page.addElement(e)
        
    def makeIncrementalTextSamples(self, page, s):
        pw = page.w-2*PAD # Usable page width
        ph = page.h-2*PAD # Usable page height
        fontSize = (8,9,10,11,12,13,14,15,16,18,20,22,24,26,28,32,36,40,
            44,48,52,56)
        y = ph-PAD/2
        for size in fontSize:
            lineHeight = size * 1.2
            lineStyle['fontSize'] = size
            lineStyle['lineHeight'] = lineHeight # To be sure, in case label is behind
            labelStyle['lineHeight'] = lineHeight # Label defines lineHeight
            fs = Text.FS('%dpt\n' % size, **labelStyle)
            fs += Text.FS(s+'\n', **lineStyle)
            e = TextBox(fs, x=PAD, y=y, w=pw, h=lineHeight*7, fill=1)
            page.addElement(e)
            y -= lineHeight*8+G
            if y < PAD:
                break
                
    def makeGlyphSet(self, page): 
        pw = page.w-2*PAD # Usable page width
        ph = page.h-2*PAD # Usable page height
        fs = Text.FS('', **glyphStyle)
        drawBot.font(self.font)
        #glyphNames = []
        #for glyphName in drawBot.listFontGlyphNames():
        #    glyphNames.append(glyphName)
        #    glyphNames.append('space')
        glyphNames = drawBot.listFontGlyphNames()
        fs.appendGlyph(*glyphNames)
        pc = 0
        while pc < 4 and fs:
            if pc > 0:
                page = typeSpecimen.newPage()
                self.initializePage(page)
            e = TextBox(fs, x=PAD, y=PAD+8, w=pw, h=ph-24, fill=1)
            page.addElement(e)
            fs = e.getOverflow(fs, w=PAD, h=ph-24, doc=self)
            pc += 1
                                   
# Create a document with default A4-portrait size.
typeSpecimen = TypeSpecimen(font) # Execute the class/factory by adding "()"
page = typeSpecimen.newPage()
typeSpecimen.initializePage(page)
typeSpecimen.makeWaterfall(page, 'Hamburgefonstiv')

page = typeSpecimen.newPage()
typeSpecimen.initializePage(page)
lorem = loremipsum().replace('\n', ' ')
typeSpecimen.makeIncrementalTextSamples(page, lorem)

page = typeSpecimen.newPage()
typeSpecimen.initializePage(page)
typeSpecimen.makeGlyphSet(page)

# Build the document, all pages and their contained elements.
typeSpecimen.build() 

typeSpecimen.export('_export/MyTypeSpecimen.pdf')

print('Done 005')
