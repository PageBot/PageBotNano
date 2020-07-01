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
#   Templates are functions with a standard attribute interface, that
#   can be stored in elements to initialize and compose their content.
#
import sys

if __name__ == "__main__":
    sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano_010.constants import MAIN, LEFT, RIGHT, CENTER, NONE
from pagebotnano_010.elements import Text, TextBox, Rect
from pagebotnano_010.babelstring import BabelString

def _initialize(doc, page, parent):
    if page is None:
        page = doc.newPage()
    if parent is None:
        parent = page
    page.w = doc.w
    page.h = doc.h
    page.padding = doc.padding
    return page

def coverPage(theme, doc, page=None, parent=None, **kwargs):
    page = _initialize(doc, page, parent)
    # Fill the cover page with a theme background color
    e = Rect(0, 0, page.w, page.h, fill=theme.getColor(1, 4)) # Dark cover color
    page.addElement(e) 

    # Add title and author, centered on top-half of the cover.
    e = TextBox('', name='Title', x=page.pl/2, y=page.h/2, w=page.pw, h=page.ph/2)
    page.addElement(e)

    e = Image(x=pad, y=pad, w=page.w-2*pad)
    page.addElement(e)

def tableOfContentPage(theme, doc, page=None, parent=None, **kwargs):
    page = _initialize(doc, page, parent)
    return page

def indexPage(theme, doc, page=None, parent=None, **kwargs):
    page = _initalize(doc, page, parent)
    return page

def oneColumnPage(theme, doc, page=None, parent=None, pageNumbers=None, **kwargs):
    """
    >>> from pagebotnano_010.document import Document
    >>> from pagebotnano_010.themes import BackToTheCity
    >>> theme = BackToTheCity()
    >>> doc = Document()
    >>> page = oneColumnPage(theme, doc, pageNumbers=NONE)
    >>> page.compose(doc)
    >>> page.find(MAIN)
    <TextBox name=mainText w=535 h=782>
    >>> page = doc.newPage(template=oneColumnPage)
    """
    page = _initialize(doc, page, parent)
    # Add text element with the main text column of this page
    e = TextBox('', name=MAIN, x=page.pl, y=page.pb, w=page.pw, h=page.ph)
    page.addElement(e)

    if pageNumbers is None:
        pageNumbers = [LEFT, RIGHT]
    if LEFT in pageNumbers and page.pn % 2 == 0: # Even page number?:
        bs = BabelString(str(page.pn), style)
        e = Text(bs, name=PN_LEFT, x=page.pl, y=page.pb/2)
        page.addElement(e)
    if CENTER in pageNumbers:
        e = Text('', name=PN_CENTER, x=page.pl+page.pw, y=page.pb/2)
        page.addElement(e)
    if RIGHT in pageNumbers:
        e = Text('', name=PN_RIGHT, x=page.pl+page.pw, y=page.pb/2)
        page.addElement(e)
    return page

def frenchPage(theme, doc, page=None, parent=None, **kwargs):
    """Compose the template page with the position of the “French” (or
    “Voordehandse”) text.
    Empty page, with only the title of the book centere on the page width.
    BabelString alignment should be CENTER.

    >>> from pagebotnano_010.document import Document
    >>> from pagebotnano_010.themes import BackToTheCity
    >>> theme = BackToTheCity()
    >>> doc = Document()
    >>> page = frenchPage(theme, doc)
    >>> page.compose(doc)
    >>> page.find(MAIN)
    <Text name=mainText w=None h=None>
    """
    page = _initialize(doc, page, parent)
    e = Text('', name=MAIN, x=page.pl+page.pw/2, y=page.h*4/5)
    page.addElement(e)
    return page

def titlePage(theme, doc, page=None, parent=None, **kwargs):
    """Compose the template page with the position of the TitlePage.
    Empty page, with only the title of the book centere on the page width.

    >>> from pagebotnano_010.document import Document
    >>> from pagebotnano_010.themes import BackToTheCity
    >>> theme = BackToTheCity()
    >>> doc = Document()
    >>> page = titlePage(theme, doc)
    >>> page.compose(doc)
    >>> page.find(MAIN)
    <TextBox name=mainText w=535 h=586.5>
    """
    page = _initialize(doc, page, parent)
    e = TextBox('', name=MAIN, x=page.pl, y=page.pb + page.ph*3/4, w=page.pw, h=page.ph*3/4)
    page.addElement(e)
    return page

def colophonPage(theme, doc, page=None, parent=None, **kwargs):
    """Compose the template page with the position of the ColophonPage.
    Empty page, with only the title of the book centere on the page width.

    >>> from pagebotnano_010.document import Document
    >>> from pagebotnano_010.themes import BackToTheCity
    >>> theme = BackToTheCity()
    >>> doc = Document()
    >>> page = colophonPage(theme, doc) # Creating a new page
    >>> page.compose(doc, page)
    >>> page.find(MAIN)
    <TextBox name=mainText w=535 h=782>
    """
    page = _initialize(doc, page, parent)
    e = TextBox('', name=MAIN, x=page.pl, y=page.pb, w=page.pw, h=page.ph)
    page.addElement(e)
    return page

# Combine all template functions into on set.
# Select the template functions for this manual.
class OneColumnTemplates:
    def __init__(self):
        self.cover = coverPage
        self.toc = tableOfContentPage
        self.main = oneColumnPage
        self.french = frenchPage
        self.title = titlePage
        self.colophon = colophonPage
        self.index = indexPage


if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]