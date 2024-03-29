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
#   MyBook.py
#
#   This MyBook.py shows an example how to import
#   existing libaries, that contain knowledge about a publication,
#   document, pages and the elements on the pages.
#
from random import choice, random
from pagebotnano_009.elements import Rect, Text
from pagebotnano_009.publications.book import Book
from pagebotnano_009.toolbox.loremipsum import loremipsum, randomName, randomTitle
from pagebotnano_009.toolbox.typesetter import Typesetter
from pagebotnano_009.toolbox import mm

w, h = mm(130), mm(210)

title = randomTitle()
author = randomName()
coverImagePath = choice([
    'resources/images/cookbot1.jpg',
    'resources/images/cookbot2.jpg',
])
coverColor = (random()*0.1,random()*0.1, random()*0.5)

# Styles for the tags that are used in the xml content.
styles = dict(
    h1=dict(font='Georgia-Bold', fontSize=18, lineHeight=20, paragraphBottomSpacing=10),
    h2=dict(font='Georgia-Italic', fontSize=14, lineHeight=16, paragraphBottomSpacing=10),
    p=dict(font='Georgia', fontSize=10, lineHeight=14)
)
print('Generating the book “%s” by %s' % (title, author))

# Construct the content as “xml” document.
xml = """<xml>
<h1>%s</h1>
<p>%s</p>
<h1>Another headline</h1>
<p>%s</p>
</xml>""" % (title, (loremipsum() + ' ') * 20,  loremipsum())

#print(xml)
# Create the typesetter that will do content parsing into a “Galley”
ts = Typesetter()
# Do the typesetting. Galley is now another type of element
# that contains text and image elements in a sequence.
# Passing styles as dictionary. In later versions this will be come a Theme object.
galley = ts.typeset(xml, styles)
print(galley, len(galley.elements))

# Create the Book publication and feed it with the processed galley content.
book = Book(w=w, h=h, title=title, author=author, galley=galley,
    coverImagePath=coverImagePath, 
    coverColor=coverColor)
book.export('_export/MyBook.pdf')

print('Done 009')