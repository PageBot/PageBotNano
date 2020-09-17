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

from pagebotnano_008.constants import CENTER, LEFT, RIGHT, EN
from pagebotnano_008.publications.publication import Publication
from pagebotnano_008.document import Document
from pagebotnano_008.elements import Rect, Text, TextBox, Image
from pagebotnano_008.babelstring import BabelString
from pagebotnano_008.toolbox.typesetter import Typesetter

class Book(Publication):
    """A Book publication takes a volume of text/imges source
    as markdown document, composing book pages and export as
    PDF document.

    >>> from pagebotnano_008.elements import Rect, Text
    >>> from pagebotnano_008.constants import A5
    >>> from pagebotnano_008.toolbox.loremipsum import loremipsum, randomName, randomTitle
    >>> w, h = A5
    >>> title = randomTitle()
    >>> author = randomName()
    >>> ts = Typesetter()
    >>> xml = '<xml><h1>%s</h1><p>%s</p></xml>' % (title, (loremipsum() + ' ') * 50)
    >>> styles = {}
    >>> styles['h1'] = dict(font='Georgia-Bold', fontSize=18, lineHeight=20, paragraphBottomSpacing=18)
    >>> styles['p'] = dict(font='Georgia', fontSize=10, lineHeight=14)
    >>> g = ts.typeset(xml, styles)    
    >>> imagePath = '../../resources/images/cookbot2.jpg'
    >>> book = Book(w=w, h=h, title=title, author=author, galley=g, coverImagePath=imagePath)
    >>> book.export('_export/Book.pdf')
    """
    MAX_PAGES = 100
    
    def __init__(self, w, h, title, author, galley=None, coverImagePath=None, 
        coverImageBackgroundColor=None,
        coverColor=None, styles=None):
        Publication.__init__(self, w, h)
        self.title = title
        self.author = author
        self.galley = galley # Typesetter.galley
        self.coverImagePath = coverImagePath
        if coverColor is None:
            coverColor = random()*0.3, random()*0.1, random()*0.4 # Random dark blue
        self.coverColor = coverColor
        self.coverImageBackgroundColor = coverImageBackgroundColor
        if styles is None:
            styles = {}
        self.styles = styles

    def compose(self):
        """This is the core of a publication, composing the specific
        content of the document. The compose method gets called
        before building and exporting the self.doc document.
        """
        fontSize = 11
        headSize = fontSize*1.5
        titleSize = 36
        subTitleSize = titleSize * 0.5
        pad = 48 # Padding of the page.

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