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

from pagebotnano_030.constants import (MAIN, LEFT, RIGHT, CENTER, NONE,
    PN_LEFT, PN_CENTER, PN_RIGHT)
from pagebotnano_030.elements import Text, TextBox, Rect, Image
from pagebotnano_030.babelstring import BabelString
from pagebotnano_030.templates import BaseTemplates

class OneColumnTemplates(BaseTemplates):
    """
    The doc.cd ComposerData instance contains running information for 
    templates to compose their pages. 

    cd.page = Optional current page to start flows.
    cd.page.pn = Optional current page number
    cd.galley = Galley with content input to compose
    cd.template = Current running template function
    cd.elements = Selected galley elements for the current template
    cd.errors = List or error messages during template/page composition
    cd.verbose = List of verbose text lines during template/page composition
    
    Other info accessable by templates
    doc.theme = Theme for colors and style
    doc.theme.styles = Main set of styles for this publication
    doc.templates = This class OneColumnTemplates
    """
    def _initialize(self, doc, makeNewPage=False): # Standard API for all templates
        page = doc.cd.page
        if makeNewPage or page is None:
            page = doc.newPage()
        page.w = doc.w
        page.h = doc.h
        page.padding = doc.padding
        return page

    def pageNumber(self, doc):
        print('OneColumnTemplates doing pageNumber for', doc.cd.page)

    def cover(self, doc):
        page = self._initialize(doc, True)
        # Fill the cover page with a theme background color
        e = Rect(0, 0, page.w, page.h, fill=doc.theme.getColor(1, 4)) # Dark cover color
        page.addElement(e) 

        # Add title and author, centered on top-half of the cover.
        try:
            title = doc.cd.elements[0].bs
        except (IndexError, AttributeError):
            title = BabelString('Untitled')
        e = TextBox(title, name='Title', x=page.pl/2, y=page.h/2, w=page.pw, h=page.ph/2)
        page.addElement(e)

        e = Image(x=page.pl, y=page.pb, w=page.pw)
        page.addElement(e)
        return page

    def frenchTitle(self, doc):
        page = self._initialize(doc, True)
        # Fill the cover page with a theme background color
        e = Rect(0, 0, page.w, page.h, fill=doc.theme.getColor(1, 4)) # Dark cover color
        page.addElement(e) 

        # Add title and author, centered on top-half of the cover.
        e = TextBox('', name='Title', x=page.pl/2, y=page.h/2, w=page.pw, h=page.ph/2)
        page.addElement(e)

        e = Image(x=page.pl, y=page.pb, w=page.pw)
        page.addElement(e)
        return page

    def title(self, doc):
        page = self._initialize(doc, True)
        # Fill the cover page with a theme background color
        e = Rect(0, 0, page.w, page.h, fill=doc.theme.getColor(1, 4)) # Dark cover color
        page.addElement(e) 

        # Add title and author, centered on top-half of the cover.
        e = TextBox('', name='Title', x=page.pl/2, y=page.h/2, w=page.pw, h=page.ph/2)
        page.addElement(e)

        e = Image(x=page.pl, y=page.pb, w=page.pw)
        page.addElement(e)
        return page

    def tableOfContent(self, doc):
        page = self._initialize(doc, True)
        return page

    def page(self, doc):
        """
        >>> from pagebotnano_030.document import Document
        >>> from pagebotnano_030.themes import BackToTheCity
        >>> templates = OneColumnTemplates()
        >>> templates
        <OneColumnTemplates>
        >>> theme = BackToTheCity()
        >>> doc = Document(theme=theme, templates=templates)
        >>> page = templates.cover(doc) # The "page" template always must be there.
        >>> page.compose(doc)
        """
        page = self._initialize(doc, True)
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

    def chapter(self, doc):
        """If this template is called, a new chapter starts.
        Create a new page, select is as doc.page, create a new text box and make select it
        as case.flow.
        """
        page = self._initialize(doc, True)
        e = TextBox('', name=MAIN, x=page.pl, y=page.pb, w=page.pw, h=page.ph)
        page.addElement(e)
        return page

    def index(self, doc):
        page = self._initialize(doc, True)
        return page

    def colophon(self, doc):
        """Compose the template page with the position of the ColophonPage.
        Empty page, with only the title of the book centere on the page width.

        >>> from pagebotnano_030.document import Document
        >>> from pagebotnano_030.themes import BackToTheCity
        >>> templates = OneColumnTemplates()
        >>> theme = BackToTheCity()
        >>> doc = Document(theme=theme)
        >>> page = templates.colophon(doc) # Creating a new page
        >>> page.compose(doc)
        """
        page = self._initialize(doc, True)
        e = TextBox('', name=MAIN, x=page.pl, y=page.pb, w=page.pw, h=page.ph)
        page.addElement(e)
        return page

    def footnote(self, doc):
        page = self._initalize(doc) # Take current doc.cd.page if defined.
        print('=== footnote')

    def literature(self, doc):
        page = self._initalize(doc) # Take current doc.cd.page if defined.
        print('=== literature')

if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]