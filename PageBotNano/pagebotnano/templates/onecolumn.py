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
    """
    Provide a set of class methods that construct pages, using the 
    resources available in the case container:
    case.publication = The Publication instance, e.g. Book
    case.doc = The current document, containing all pages 
    case.page = Optional current page to start flows.
    case.galley = Galley with content input to compose
    case.theme = Theme for colors and style
    case.styles = Main set of styles for this publication
    case.templates = This class OneColumnTemplates
    case.errors = List with exported error strings.
    case.verbose = List with exported verbose strings.
    """
    @classmethod
    def _initialize(cls, case): # Standard API for all templates
        if case.page is None:
            page = case.doc.newPage()
        else:
            page = case.page
        page.w = case.doc.w
        page.h = case.doc.h
        page.padding = case.doc.padding
        return page

    @classmethod
    def pageNumber(cls, case):
        print('OneColumnTemplates doing pageNumber for', page)

    @classmethod
    def cover(cls, case):
        page = cls._initialize(case)
        print(case.template)
        print(case.elements[0].bs)
        # Fill the cover page with a theme background color
        e = Rect(0, 0, page.w, page.h, fill=case.theme.getColor(1, 4)) # Dark cover color
        page.addElement(e) 

        # Add title and author, centered on top-half of the cover.
        e = TextBox(case.elements[0].bs, name='Title', x=page.pl/2, y=page.h/2, w=page.pw, h=page.ph/2)
        page.addElement(e)

        e = Image(x=page.pl, y=page.pb, w=page.pw)
        page.addElement(e)

    @classmethod
    def frenchTitle(cls, case):
        page = cls._initialize(case)
        # Fill the cover page with a theme background color
        e = Rect(0, 0, page.w, page.h, fill=case.theme.getColor(1, 4)) # Dark cover color
        page.addElement(e) 

        # Add title and author, centered on top-half of the cover.
        e = TextBox('', name='Title', x=page.pl/2, y=page.h/2, w=page.pw, h=page.ph/2)
        page.addElement(e)

        e = Image(x=page.pl, y=page.pb, w=page.pw)
        page.addElement(e)

    @classmethod
    def title(cls, case, page=None):
        page = cls._initialize(case)
        # Fill the cover page with a theme background color
        e = Rect(0, 0, page.w, page.h, fill=case.theme.getColor(1, 4)) # Dark cover color
        page.addElement(e) 

        # Add title and author, centered on top-half of the cover.
        e = TextBox('', name='Title', x=page.pl/2, y=page.h/2, w=page.pw, h=page.ph/2)
        page.addElement(e)

        e = Image(x=page.pl, y=page.pb, w=page.pw)
        page.addElement(e)

    @classmethod
    def tableOfContent(cls, case):
        page = cls._initialize(case)
        return page

    @classmethod
    def page(cls, case):
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
        page = cls._initialize(case)
        # Add text element with the main text column of this page
        e = TextBox('', name=MAIN, x=page.pl, y=page.pb, w=page.pw, h=page.ph)
        page.addElement(e)

        leftPageNumberStyle = case.theme.getStyle('leftPageNumber')
        centerPageNumberStyle = case.theme.getStyle('centerPageNumber')
        rightPageNumberStyle = case.theme.getStyle('rightPageNumber')

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
    def chapter(cls, case):
        """If this template is called, a new chapter starts.
        Create a new page, select is as doc.page, create a new text box and make select it
        as case.flow.
        """
        page = case.newPage()
        e = TextBox('', name=MAIN, x=page.pl, y=page.pb, w=page.pw, h=page.ph)
        page.addElement(e)
        return page

    @classmethod
    def index(cls, case):
        page = cls._initialize(case)
        return page

    @classmethod
    def colophon(cls, case):
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
        page = cls._initialize(case)
        e = TextBox('', name=MAIN, x=page.pl, y=page.pb, w=page.pw, h=page.ph)
        page.addElement(e)
        return page

    @classmethod
    def footnote(cls, case):
        print('=== footnote')

    @classmethod
    def literature(cls, case):
        print('=== literature')

if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]