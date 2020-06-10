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
#   MyManual.py
#
#   This MyBook.py shows an example how to import
#   existing libaries, that contain knowledge about a publication,
#   document, pages and the elements on the pages.
#
from random import choice, random
from pagebotnano.constants import EN, JUSTIFIED
from pagebotnano.elements import Rect, Text
from pagebotnano.publications.book import Book
from pagebotnano.toolbox.loremipsum import loremipsum, randomName, randomTitle
from pagebotnano.toolbox.typesetter import Typesetter
from pagebotnano.toolbox import mm
from pagebotnano.templates.onecolumn import *

w, h = mm(130), mm(210) # Nice little booklet

title = randomTitle()
author = randomName()
contextPath = '../resources/PublishingVariables.md'
coverImagePath = choice([
    '../resources/images/PageBotSchema2.pdf',
    #'../resources/images/cookbot2.jpg',
])
coverColor = (random()*0.1,random()*0.1, random()*0.5)

# Styles for the tags that are used in the xml content.
styles = dict(
    h1=dict(font='Georgia-Bold', fontSize=14, lineHeight=16, 
        paragraphTopSpacing=3, language=EN, hyphenation=True),
    h2=dict(font='Georgia-Italic', fontSize=12, lineHeight=16, 
        paragraphTopSpacing=3, language=EN),
    h3=dict(font='Georgia-Italic', fontSize=10, lineHeight=13, 
        paragraphTopSpacing=3, language=EN),
    p=dict(font='Georgia', fontSize=9, lineHeight=13, language=EN, 
        align=JUSTIFIED),
    b=dict(font='Georgia-Italic', fontSize=9, lineHeight=13, 
        language=EN, align=JUSTIFIED),
    em=dict(font='Georgia-Bold', fontSize=9, lineHeight=13, 
        language=EN, align=JUSTIFIED),
    i=dict(font='Georgia-Italic', fontSize=9, lineHeight=13, 
        language=EN, align=JUSTIFIED),
    bi=dict(font='Georgia-BoldItalic', fontSize=9, lineHeight=13, 
        language=EN, align=JUSTIFIED),
)
print('Generating the manual “%s” by %s' % (title, author))

# Create the typesetter that will do content parsing into a “Galley”
ts = Typesetter()
# Do the typesetting. Galley is now another type of element
# that contains text and image elements in the sequence of the markdown.
galley = ts.typesetFile(contextPath, styles)

# Create templates for this book.
templates = [
    FrenchPage(),
    TitlePage(),
    OneColumnPage(),
    ColophonPage(),
]
# Create the Book publication and feed it with the processed galley content.
book = Book(w=w, h=h, title=title, author=author, galley=galley,
    coverImagePath=coverImagePath, coverColor=coverColor,
    templates=templates)

book.export('_export/MyManual.pdf')

print('Done')