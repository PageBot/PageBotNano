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
from pagebotnano.elements import Rect, Text
from pagebotnano.constants import A5
from pagebotnano.publications.book import Book
from pagebotnano.toolbox.loremipsum import loremipsum, randomName, randomTitle

w, h = A5
title = randomTitle()
author = randomName()
coverImagePath = choice([
    '../resources/images/cookbot1.jpg',
    '../resources/images/cookbot2.jpg',
])
coverColor = (random()*0.1,random()*0.1, random()*0.5)

print('Generating the book “%s” by %s' % (title, author))

content = (loremipsum() + ' ') * 50
pub = Book(w=w, h=h, title=title, author=author, 
    coverImagePath=coverImagePath, content=content,
    coverColor=coverColor)
pub.export('_export/MyBook.pdf')

print('Done')