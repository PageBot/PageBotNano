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
from pagebotnano.document import Document
from pagebotnano.elements import Rect, Text, TextBox, Image, Marker
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
    >>> w, h = PENGUIN_POCKET 
    >>> title = randomTitle()
    >>> author = randomName()
    >>> ts = Typesetter()
    >>> xml = '<xml><title>%s</title><author>%s</author><h1>%s</h1><p>%s</p></xml>' % (title, author, title, (loremipsum() + ' ') * 50)
    >>> styles = {}
    >>> styles['h1'] = dict(font='Georgia-Bold', fontSize=18, lineHeight=20, paragraphBottomSpacing=18)
    >>> styles['p'] = dict(font='Georgia', fontSize=10, lineHeight=14)
    >>> g = ts.typeset(xml, styles)    
    >>> book = Book(w=w, h=h, templates=OneColumnTemplates, styles=styles, galley=g)
    >>> book.galley.elements
    [<Marker type=author index=None>, <TextBox name=TextBox w=100pt h=None>]
    >>> book.export('_export/TestBook.pdf')
    """
    MAX_PAGES = 100
    
    def __init__(self, w=None, h=None, templates=None, styles=None, galley=None, context=None):
        Publication.__init__(self, w=w, h=h, templates=templates, styles=styles, galley=galley, context=context)

    def compose(self, page=None, targets=None):
        """This is the core of a publication, composing the specific content of the document, 
        from tags found in the gally.
        The compose method gets called before building and exporting the self.doc document.
        The templates class is supposed to know how to query for tags to be places on various types of pages. 
        Self (the Publications Book) is supposed to know which templates to call for certain page,
        if that is not already defined by the markdown input stream.

        >>> from pagebotnano.elements import Rect, Text
        >>> from pagebotnano.constants import PENGUIN_POCKET
        >>> from pagebotnano.toolbox.loremipsum import loremipsum, randomName, randomTitle
        >>> from pagebotnano.templates.onecolumn import OneColumnTemplates
        >>> w, h = PENGUIN_POCKET 
        >>> ts = Typesetter()
        >>> styles = {}
        >>> styles['h1'] = dict(font='Georgia-Bold', fontSize=18, lineHeight=20, paragraphBottomSpacing=18)
        >>> styles['p'] = dict(font='Georgia', fontSize=10, lineHeight=14)
        >>> markdownPath = '../../MakeItSmall-TheBook.md'
        >>> g = ts.typesetFile(markdownPath, styles)    
        >>> book = Book(w=w, h=h, templates=OneColumnTemplates, styles=styles, galley=g)
        >>> book.galley.find(cls='Marker')
        <Marker type=chapter index=None>
        >>> book.export('_export/Book.pdf')

        """
        # For all the elements that are collected in the galley, assume that
        # the TextBoxes are chapters, creating a new page for them.
        # If the TextBox does not fit on the page, keep adding new pages 
        # until all of the BabelString overfill is processed.

        if targets is None:
            if page is None:
                if not self.doc.pages:
                    pages = self.doc.newPage()
                else:
                    page = self.doc.pages[0] # Select the first page of the document, unless defined otherwise.

            # Transfer a whole packages of current resources to the stream parsing,
            # so that information is accessable from the galley code block processing.
            targets = dict(composer=self, doc=self.doc, page=page, styles=self.styles,
                theme=self.theme, templates=self.templates)

            if page is not None:
                targets['box'] = page.select('main')

        elif page is not None:
            targets['page'] = page

        if 'errors' not in targets:
            targets['errors'] = []
        errors = targets['errors']

        if 'verbose' not in targets:
            targets['verbose'] = []
        verbose = targets['verbose']

        composerName = self.__class__.__name__

        for e in self.galley.elements:

            if isinstance(e, Marker): # Marker can select a new page, chapter, footnote, etc.
                if e.markerType == 'page': # $page$ in markdown file
                    page = self.doc.newPage()
                    verbose.append('%s.compose: Marker new page' % composerName)

            elif targets.get('box') is not None and targets.get('box').isText and targets.get('box').bs is not None and e.isText:
                # If new content and last content are both text boxes, then merge the string.
                targets.get('box').bs += e.bs

            elif targets.get('box') is not None:
                # Otherwise just paste the galley-element onto the target box.
                #e.parent = targets.get('box')
                pass
            else:
                errors.append('%s.compose: No valid box or image selected "%s - %s"' % (composerName, page, e))

        return targets
        """
        for ge in self.galley.elements:
            print('Galley Element', ge.__class__.__name__)
            continue
            if isinstance(ge, TextBox):

                bs = ge.bs # Get the BabelString from the galley box.

                for n in range(self.MAX_PAGES):
                    page = self.doc.newPage()

                    # Add text element with page number
                    self.templates.pageNumber(self.theme, self.doc, page, self.styles)

                    
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