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

from pagebotnano.constants import (MAIN, LEFT, RIGHT, CENTER, NONE,
    PN_LEFT, PN_CENTER, PN_RIGHT)
from pagebotnano.elements import Text, TextBox, Rect, Image
from pagebotnano.babelstring import BabelString
from pagebotnano.templates import BaseTemplates

class OneColumnTemplates(BaseTemplates):

    @classmethod
    def _initialize(cls, doc): # Standard API for all templates
        if doc.page is None:
            page = doc.newPage()
        else:
            page = doc.page
        page.w = doc.w
        page.h = doc.h
        page.padding = doc.padding
        return page

    @classmethod
    def pageNumber(cls, doc):
        print('OneColumnTemplates doing pageNumber for', page)

    @classmethod
    def cover(cls, doc):
        page = cls._initialize(doc)
        # Fill the cover page with a theme background color
        e = Rect(0, 0, page.w, page.h, fill=theme.getColor(1, 4)) # Dark cover color
        page.addElement(e) 

        # Add title and author, centered on top-half of the cover.
        e = TextBox('', name='Title', x=page.pl/2, y=page.h/2, w=page.pw, h=page.ph/2)
        page.addElement(e)

        e = Image(x=page.pl, y=page.pb, w=page.pw)
        page.addElement(e)

    @classmethod
    def frenchTitle(cls, doc):
        page = cls._initialize(doc)
        # Fill the cover page with a theme background color
        e = Rect(0, 0, page.w, page.h, fill=theme.getColor(1, 4)) # Dark cover color
        page.addElement(e) 

        # Add title and author, centered on top-half of the cover.
        e = TextBox('', name='Title', x=page.pl/2, y=page.h/2, w=page.pw, h=page.ph/2)
        page.addElement(e)

        e = Image(x=page.pl, y=page.pb, w=page.pw)
        page.addElement(e)

    @classmethod
    def title(cls, doc, page=None):
        page = cls._initialize(doc)
        # Fill the cover page with a theme background color
        e = Rect(0, 0, page.w, page.h, fill=theme.getColor(1, 4)) # Dark cover color
        page.addElement(e) 

        # Add title and author, centered on top-half of the cover.
        e = TextBox('', name='Title', x=page.pl/2, y=page.h/2, w=page.pw, h=page.ph/2)
        page.addElement(e)

        e = Image(x=page.pl, y=page.pb, w=page.pw)
        page.addElement(e)

    @classmethod
    def tableOfContent(cls, doc):
        page = _cls.initialize(theme, doc, page, parent, styles)
        return page

    @classmethod
    def page(cls, doc):
        """
        >>> from pagebotnano.document import Document
        >>> from pagebotnano.themes import BackToTheCity
        >>> templates = OneColumnTemplates()
        >>> theme = BackToTheCity()
        >>> doc = Document(theme=theme, templates=templates)
        >>> page = templates.page(doc)
        >>> page.compose(doc)
        >>> page.find(MAIN)
        <TextBox name=mainText w=535pt h=782pt>
        >>> page = doc.newPage()
        """
        page = cls._initialize(doc)
        # Add text element with the main text column of this page
        e = TextBox('', name=MAIN, x=page.pl, y=page.pb, w=page.pw, h=page.ph)
        page.addElement(e)

        leftPageNumberStyle = doc.theme.getStyle('leftPageNumber')
        centerPageNumberStyle = doc.theme.getStyle('centerPageNumber')
        rightPageNumberStyle = doc.theme.getStyle('rightPageNumber')

        if leftPageNumberStyle is not None and page.pn % 2 == 0: # Even page number?:
            bs = BabelString(str(page.pn), style)
            e = Text(bs, name=PN_LEFT, x=page.pl, y=page.pb/2)
            page.addElement(e)
        if centerPageNumberStyle is not None:
            e = Text('', name=PN_CENTER, x=page.pl+page.pw, y=page.pb/2)
            page.addElement(e)
        if rightPageNumberStyle is not None and page.pn % 2 != 0: # Odd page number?:
            e = Text('', name=PN_RIGHT, x=page.pl+page.pw, y=page.pb/2)
            page.addElement(e)
        return page

    @classmethod
    def index(cls, doc):
        page = _cls.initialize(doc)
        return page

    @classmethod
    def colophon(cls, doc):
        """Compose the template page with the position of the ColophonPage.
        Empty page, with only the title of the book centere on the page width.

        >>> from pagebotnano.document import Document
        >>> from pagebotnano.themes import BackToTheCity
        >>> template = OneColumnTemplates()
        >>> theme = BackToTheCity()
        >>> doc = Document(theme=theme)
        >>> page = template.colophon(doc) # Creating a new page
        >>> page.compose(doc, page)
        >>> page.find(MAIN)
        <TextBox name=mainText w=535pt h=782pt>
        """
        page = cls._initialize(doc)
        e = TextBox('', name=MAIN, x=page.pl, y=page.pb, w=page.pw, h=page.ph)
        page.addElement(e)
        return page

    @classmethod
    def footnote(cls, doc):
        print('=== footnote')

    @classmethod
    def literature(cls, doc):
        print('=== literature')

    @classmethod
    def footnote(cls, doc):
        print('=== footnote')

    @classmethod
    def chapter(cls, doc):
        print('=== chapter')

if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]