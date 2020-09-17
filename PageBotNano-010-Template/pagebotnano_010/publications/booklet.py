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
#   booklet.py
#
import os # Import standard Python library to create the _export directory
from copy import copy
from random import random
import sys

if __name__ == "__main__":
    sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano_010.constants import CENTER, LEFT, RIGHT, EN, MAIN
from pagebotnano_010.publications.publication import Publication
from pagebotnano_010.document import Document
from pagebotnano_010.elements import Rect, Text, TextBox, Image
from pagebotnano_010.babelstring import BabelString
from pagebotnano_010.toolbox.typesetter import Typesetter
from pagebotnano_010.templates.onecolumn import OneColumnTemplates

class Booklet(Publication):
    """A Book publication takes a volume of text/imges source
    as markdown document, composing book pages and export as
    PDF document.

    >>> from pagebotnano_010.elements import Rect, Text
    >>> from pagebotnano_010.constants import A5
    >>> from pagebotnano_010.toolbox.loremipsum import loremipsum, randomName, randomTitle
    >>> from pagebotnano_010.templates.onecolumn import *
    >>> theme = BackToTheCity()
    >>> w, h = A5
    >>> title = randomTitle()
    >>> author = randomName()
    >>> ts = Typesetter()
    >>> galley = ts.galley
    >>> xml = '<xml><h1>%s</h1><p>%s</p></xml>' % (title, (loremipsum() + ' ') * 50)
    >>> styles = {}
    >>> styles['h1'] = dict(font='Georgia-Bold', fontSize=18, lineHeight=20, paragraphBottomSpacing=18)
    >>> styles['p'] = dict(font='Georgia', fontSize=10, lineHeight=14)
    >>> g = ts.typeset(xml, styles)    
    >>> imagePath = '../../resources/images/cookbot1.jpg'
    >>> booklet = Booklet(w=w, h=h, theme=theme, galley=galley, templates=OneColumnTemplates())
    >>> booklet.export('_export/Booklet.pdf')
    """
    MAX_PAGES = 100
    
    def compose(self):
        """This is the core of a publication, composing the specific
        content of the document. The compose method gets called
        before building and exporting the self.doc document.
        """
        fontSize = 11
        headSize = fontSize*1.5
        titleSize = 36
        subTitleSize = titleSize * 0.5
        pad = 48

        self.theme.styles['h1'] = dict(font='Georgia-Bold', 
            lineHeight=titleSize*1.1, 
            fontSize=titleSize,
            align=CENTER,
            fill=1, # White title on dark cover background
            language=EN, hyphenation=False,
        )
        self.theme.styles['h2'] = dict(font='Georgia-Italic',
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
        page = coverPage(self.doc, self.theme)

        # Make “French” “Voordehandse” page.
        page = self.doc.newPage() # No page number here.

        # CENTER text alignment overwrites the value in headStyle.
        # fontSize overwrites the value in headStyle
        bs = BabelString('AAAA'+'\n', headStyle, fontSize=fontSize, align=CENTER)
        e = Text(bs, x=page.w/2, y=page.h*4/5)
        page.addElement(e)

        # Make Title page.
        page = titlePage(self.theme, self.doc)
        page.compose(self.doc, page)
        bs = BabelString('VVVVV'+'\n', headStyle, align=CENTER)
        bs.append(BabelString('AUTHOR', subHeadStyle, align=CENTER))
        page.find(MAIN).bs = bs

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
                    self.addPageNumber(page, pad, pageNumberLeftStyle, pageNumberRightStyle)

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

            elif isinstance(ge, Image): # Images not supported yet
                page = self.doc.newPage()

                self.addPageNumber(page, pad, pageNumberLeftStyle, pageNumberRightStyle)
                page.addElement(ge)
                ge.w = page.w - pad
                iw, ih = ge.getSize(self.doc)
                ge.x = pad/2
                ge.y = page.h - pad - ih

    def addPageNumber(self, page, pad, leftStyle, rightStyle):
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