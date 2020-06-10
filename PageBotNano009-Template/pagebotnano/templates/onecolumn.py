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
sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano.constants import MAIN, LEFT, RIGHT, CENTER, NONE
from pagebotnano.elements import Template, Text, TextBox

def coverPage(doc, page, parent, **kwargs):
    pass

def tableOfContentPage(doc, page, parent, **kwargs):
    pass

def oneColumnPage(doc, page, parent, pageNumber=None, **kwargs):
    """
    >>> from pagebotnano.document import Document
    >>> doc = Document()
    >>> t = OneColumnPage(pageNumbers=NONE)
    >>> t.compose(doc)
    >>> t.findElement(MAIN)
    <TextBox name=mainText w=535 h=782>
    >>> page = doc.newPage(template=t)
    >>> page.applyTemplate()
    """
    page.w = doc.w
    page.h = doc.h
    page.padding = doc.padding
    # Add text element with the main text column of this page
    e = TextBox('', name=MAIN, x=page.pl, y=page.pb, w=page.pw, h=page.ph)
    page.addElement(e)
        if page.pn % 2 == 0: # Even page number?

    if pageNumbers is None:
        pageNumbers = [LEFT, RIGHT]
    if LEFT in page.pageNumbers and page.pn % 2 == 0: # Even page number?:
        bs = BabelString(str(page.pn), style)
        e.Text(bs, name=PN_LEFT, x=page.pl, y=page.pb/2)
        page.addElement(e)
    if CENTER in page.pageNumbers:
        e.Text('', name=PN_CENTER, x=page.pl+page.pw, y=page.pb/2)
        page.addElement(e)
    if RIGHT in page.pageNumbers:
        e.Text('', name=PN_RIGHT, x=page.pl+page.pw, y=page.pb/2)
        page.addElement(e)

def frenchPage(doc, page, parent, **kwargs):
    """Compose the template page with the position of the “French” (or
    “Voordehandse”) text.
    Empty page, with only the title of the book centere on the page width.
    BabelString alignment should be CENTER.

    >>> from pagebotnano.document import Document
    >>> doc = Document()
    >>> t = FrenchPage()
    >>> t.compose(doc)
    >>> t.findElement(MAIN)
    <Text name=mainText w=None h=None>
    """
    page.w = doc.w
    page.h = doc.h
    page.padding = doc.padding
    e = Text('', name=MAIN, x=self.pl+self.pw/2, y=self.h*4/5)
    page.addElement(e)

def titlePage(doc, page, parent, **kwargs):
    """Compose the template page with the position of the TitlePage.
    Empty page, with only the title of the book centere on the page width.

    >>> from pagebotnano.document import Document
    >>> doc = Document()
    >>> t = TitlePage()
    >>> t.compose(doc)
    >>> t.findElement(MAIN)
    <TextBox name=mainText w=535 h=586.5>
    """
    page.w = doc.w
    page.h = doc.h
    page.padding = doc.padding
    e = TextBox('', name=MAIN, x=self.pl, y=self.pb + self.ph*3/4, w=self.pw, h=self.ph*3/4)
    page.addElement(e)

def colophonPage(doc, page, parent, **kwargs):
    """Compose the template page with the position of the ColophonPage.
    Empty page, with only the title of the book centere on the page width.

    >>> from pagebotnano.document import Document
    >>> doc = Document()
    >>> t = ColophonPage()
    >>> t.compose(doc)
    >>> t.findElement(MAIN)
    <TextBox name=mainText w=535 h=782>
    """
    page.w = doc.w
    page.h = doc.h
    page.padding = doc.padding
    e = TextBox('', name=MAIN, x=self.pl, y=self.pb, w=self.pw, h=self.ph)
    page.addElement(e)

if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]