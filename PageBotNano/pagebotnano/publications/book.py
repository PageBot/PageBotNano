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
#   book.py
#
import os # Import standard Python library to create the _export directory
from copy import copy
import sys
from random import random

if __name__ == "__main__":
    sys.path.insert(0, "../..") # So we can import pagebotnano002 without installing.

from pagebotnano.constants import CENTER, LEFT, RIGHT, EN
from pagebotnano.publications.publication import Publication
from pagebotnano.templates import BaseTemplates
from pagebotnano.document import Document
from pagebotnano.elements import Rect, Text, TextBox, Image, Marker, TemplateMarker
from pagebotnano.babelstring import BabelString
from pagebotnano.toolbox.typesetter import Typesetter
from pagebotnano.toolbox.units import pt

class Book(Publication):
    """A Book publication takes a volume of text/imges source
    as markdown document, composing book pages and export as
    PDF document.

    >>> from pagebotnano.elements import Rect, Text
    >>> from pagebotnano.constants import PENGUIN_POCKET
    >>> from pagebotnano.toolbox.loremipsum import loremipsum, randomName, randomTitle
    >>> from pagebotnano.templates.onecolumn import OneColumnTemplates
    >>> from pagebotnano.themes import IntoTheWoods
    >>> w, h = PENGUIN_POCKET 
    >>> title = randomTitle()
    >>> author = randomName()
    >>> ts = Typesetter()
    >>> xml = '<xml><title>%s</title><author>%s</author><h1>%s</h1><p>%s</p></xml>' % (title, author, title, (loremipsum() + ' ') * 50)
    >>> theme = IntoTheWoods()
    >>> theme.styles['h1'] = dict(font='Georgia-Bold', fontSize=18, lineHeight=20, paragraphBottomSpacing=18)
    >>> theme.styles['p'] = dict(font='Georgia', fontSize=10, lineHeight=14)
    >>> g = ts.typeset(xml, theme)    
    >>> templates = OneColumnTemplates()
    >>> book = Book(w=w, h=h, templates=templates, theme=theme)
    >>> book.doc.size
    (130mm, 203mm)
    >>> g.elements
    [<Flow id=0>]
    """
    MAX_PAGES = 100
    
    def __init__(self, w=None, h=None, templates=None, theme=None, context=None):
        Publication.__init__(self, w=w, h=h, templates=templates, theme=theme, context=context)

    def compose(self, galley):
        """This is the core of a publication, composing the specific content of the document, 
        from tags found in the gally.
        The compose method gets called before building and exporting the self.doc document.
        The templates class is supposed to know how to query for tags to be places on various types of pages. 
        Self (the Publications Book) is supposed to know which templates to call for certain page,
        if that is not already defined by the markdown input stream.

        self.doc.cd.page contains the optional current page to start the composing. Otherwise take first.
        self.doc.cd.galley contains the running galley

        >>> from pagebotnano.elements import Rect, Text
        >>> from pagebotnano.themes import HappyHolidays
        >>> from pagebotnano.constants import PENGUIN_POCKET_PLUS
        >>> from pagebotnano.toolbox.loremipsum import loremipsum, randomName, randomTitle
        >>> from pagebotnano.templates.onecolumn import OneColumnTemplates
        >>> w, h = PENGUIN_POCKET_PLUS 
        >>> ts = Typesetter()
        >>> theme = HappyHolidays()
        >>> theme.styles['h1'] = dict(font='Georgia-Bold', fontSize=18, lineHeight=20, paragraphBottomSpacing=18)
        >>> theme.styles['p'] = dict(font='Georgia', fontSize=10, lineHeight=14)
        >>> markdownPath = '../../MakeItSmall-TheBook.md'
        >>> g = ts.typesetFile(markdownPath, theme)  
        >>> templates = OneColumnTemplates()  
        >>> book = Book(w=w, h=h, templates=templates, theme=theme)
        >>> book.doc.size
        (140mm, 214mm)
        >>> page = templates.colorMatrix(book.doc)
        >>> book.export('_export/ColorMatrixBook.pdf')

        """
        # For all the elements that are collected in the galley, do process them.
        # If TextBoxes don't fit on the page, keep adding new pages from the
        # current template until all of the BabelString overfill is processed.

        cd = self.doc.cd # Contains current running composer data

        # The ComposerData instance contains running information for 
        # templates to compose their pages. 
        #
        # cd.page = Optional current page to start flows.
        # cd.pn = Optional current page number (if cd.page is defined, otherwise None)
        # cd.galley = Galley with content input to compose
        # cd.template = Current running template function
        # cd.elements = Selected galley elements for the current template
        # cd.errors = List or error messages during template/page composition
        # cd.verbose = List of verbose text lines during template/page composition
        #
        # Other info accessable by templates
        # doc.theme = Theme for colors and style
        # doc.theme.styles = Main set of styles for this publication
        # doc.templates = This class OneColumnTemplates
        #
        # Fill running doc composer data
        cd.galley = galley

        for e in galley.elements:

            if isinstance(e, TemplateMarker):
                # This is the marker for a new template. If there is a running template
                # then call it with the current set of scooped galley case.elements to be 
                # processed by the current template.
                if cd.template is not None:
                    self.processTemplate(self.doc)
                
                # Now we handled the running template, we can start with a clean template `e`.
                # Reset running flows and elements, as they all should have been processed here.
                cd.template = e.markerType # Name of the template to call
                cd.elements = []
            else:
                # In case there are galley elements, before a template is selected,
                # then set the default template (to make sure a page is created).
                if cd.template is None:
                    cd.template = doc.templates.page # Default template, page() always must be there.
                cd.elements.append(e) # To be processed by the current template.

        # Handle the last open template, at the end of the galley
        if cd.template is not None:
            self.processTemplate(self.doc)

    def processTemplate(self, doc):
        try:
            cd = doc.cd
            template = cd.template # Name of the template to call
            getattr(doc.templates, template)(doc)
        except AttributeError:
            print('%s.compose: No template call for "%s"' % (self.__class__.__name__, template.markerType))

    def XXX(self):

        """
        fontSize = pt(11)
        headSize = fontSize*1.5
        titleSize = pt(36)
        subTitleSize = titleSize * 0.5
        pad = pt(48)

        titleStyle = dict(font='Georgia-Bold', 
            lineHeight=titleSize*1.1, 
            fontSize=titleSize,
            align=CENTER,
            fill=1, # White title on dark cover background
            language=EN, hyphenation=False,
        )
        subTitleStyle = dict(font='Georgia-Italic',
            paragraphTopSpacing=subTitleSize/2,
            lineHeight=subTitleSize*1.2, 
            fontSize=subTitleSize,
            align=CENTER,
            fill=1, # White title on dark cover background
            language=EN, hyphenation=False,
        )
        headStyle = dict(font='Georgia', 
            lineHeight=headSize*1.3, 
            fontSize=headSize,
            fill=0, # Black text
            language=EN, hyphenation=False,
        )
        subHeadStyle = dict(font='Georgia-Italic', 
            lineHeight=headSize*0.8*1.4, 
            fontSize=headSize*0.8,
            fill=0, # Black text
            language=EN, hyphenation=False,
        )
        bodyStyle = dict(font='Georgia', 
            lineHeight=fontSize*1.4, 
            fontSize=fontSize,
            fill=0, # Black text
            language=EN, hyphenation=True,
        )
        pageNumberLeftStyle = dict(
            font='Georgia', 
            fontSize=9,
            fill=0, # Black text
            align=LEFT, 
        )
        pageNumberRightStyle = copy(pageNumberLeftStyle)
        pageNumberRightStyle['align'] = RIGHT

        # Make the cover page.
        page = self.doc.newPage()

        # Fill the cover page with a random dark color
        e = Rect(0, 0, page.w, page.h, fill=self.coverColor) # Dark cover color
        page.addElement(e) 

        # Add title and author, centered on top-half of the cover.
        titleBs = BabelString(self.title+'\n', titleStyle)
        authorBs = BabelString(self.author, subTitleStyle)
        bs = titleBs + authorBs
        e = TextBox(bs, x=pad/2, y=page.h/2, w=page.w-pad, h=page.h/2-pad)
        page.addElement(e)

        if self.coverImagePath is not None: # Only if not defined.
            e1 = Image(self.coverImagePath, x=pad, y=pad, w=page.w-2*pad)
            e2 = Rect(x=pad, y=pad, w=page.w-2*pad, h=e1.h, fill=1)
            page.addElement(e1)
            page.addElement(e2)

        # Make “French” “Voordehandse” page.
        page = self.doc.newPage() # No page number here.
        # CENTER text alignment overwrites the value in headStyle.
        # fontSize overwrites the value in headStyle
        bs = BabelString(self.title+'\n', headStyle, fontSize=fontSize, align=CENTER)
        e = Text(bs, x=page.w/2, y=page.h*4/5)
        page.addElement(e)

        # Make Title page.
        page = self.doc.newPage() # No page number here.
        bs = BabelString(self.title+'\n', headStyle, align=CENTER)
        bs.append(BabelString(self.author, subHeadStyle, align=CENTER))
        e = Text(bs, x=page.w/2, y=page.h*3/4)
        page.addElement(e)

        
        # Empty left page after title page
        page = self.doc.newPage() # No page number here.
        """
        
        # For all the elements that are collected in the galley, assume that
        # the TextBoxes are chapters, creating a new page for them.
        # If the TextBox does not fit on the page, keep adding new pages 
        # until all of the BabelString overfill is processed.

        for ge in self.galley.elements:

            if isinstance(ge, TextBox):

                bs = ge.bs # Get the BabelString from the galley box.

                for n in range(self.MAX_PAGES):
                    page = self.doc.newPage()

                    # Add text element with page number
                    self.templates.pageNumber(self.doc, page, self.styles)

                    """
                    # Add text element with the main text column of this page
                    e = TextBox(bs, x=pad, y=pad, w=page.w-2*pad, h=page.h-2*pad)
                    page.addElement(e)

                    # If there is overflow on this page, continue looping creating
                    # as many pages as needed to fill all the text in self.content.
                    # Otherwise break the loop, as we are done placing content.
                    bs = e.getOverflow(bs, doc=self.doc)
                    # Test on this “incomplete” BabelString, as it only has a cached FS
                    if not bs.fs:
                        break
                    """

            elif isinstance(ge, Image):
                page = self.doc.newPage()

                self.addPageNumber(page, pad, pageNumberLeftStyle, pageNumberRightStyle)
                iw, ih = ge.getSize(self.doc)
                ge.w = page.w - pad
                ge.x = pad/2
                ge.y = page.h - pad - ih
                #e = Rect(x=ge.x, y=ge.y, w=ge.w, h=ge.h, fill=(1, 0, 0))
                #page.addElement(e)
                page.addElement(ge)

    def addPageNumberXXX(self, page, pad, leftStyle, rightStyle):
        # Add text element with page number
        if page.pn % 2 == 0: # Even page number?
            style = leftStyle 
            x = pad
        else: # Odd page number
            style = rightStyle
            x = page.w - pad
        pn = BabelString(str(page.pn), style)
        # Center the page number.
        #e = Text(pn, page.w/2, pad/2)
        e = Text(pn, x=x, y=pad*3/4, w=page.w - 2*pad, fill=0.9)
        page.addElement(e)

if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]