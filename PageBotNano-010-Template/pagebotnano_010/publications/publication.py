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
#   publication.py
#
import os # Import standard Python library to create the _export directory
import sys

if __name__ == "__main__":
    sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano_010.document import Document
from pagebotnano_010.constants import CENTER
from pagebotnano_010.toolbox.typesetter import Galley
# Default set of template functions.
from pagebotnano_010.templates.onecolumn import OneColumnTemplates 

class Publication:
    """The Publication base class is a wrapper around a document.
    Inheriting publication classes implement specific knowledge
    about types of publications, such as Book, Type Specimen,
    Website or Corporate Identity.

    >>> from random import random
    >>> from pagebotnano_010.elements import Rect, Text
    >>> from pagebotnano_010.babelstring import BabelString
        >>> pub = Publication() # Default size A4
    >>> page = pub.doc.newPage()
    >>> e = Rect(0, 0, page.w, page.h, fill=random()*0.5) # Dark gray
    >>> page.addElement(e) 
    >>> style = dict(font='Georgia', fontSize=200, align=CENTER, fill=1)
    >>> bs = BabelString('Title', style)
    >>> e = Text(bs, x=page.w/2, y=page.h*2/3)
    >>> page.addElement(e)
    >>> pub.export('_export/Publication.pdf')
    """
    def __init__(self, w=None, h=None, galley=None, 
            templates=None, styles=None, context=None):
        
        if styles is None:
            styles = {}
        self.styles = styles
        
        # The galley is the main source of content, typically generated
        # by a Typesetter instance, reading from a markdown file.
        if galley is None:
            galley = Galley() # If not defined, create an empty Galley
        self.galley = galley

        # The TemplateSet dictionary contains a set of functions that
        # compose the pages and containing elements for a particular
        # type of publications.
        if templates is None:
            templates = OneColumnTemplates()
        self.templates = templates

        self.doc = Document(w=w, h=h, context=context)

    def compose(self):
        """Composing the publication allows inheriting class
        to create pages, fill them with elements and add content.
        """
        pass

    def export(self, path):
        """Export the publication as document, by passing the path
        on to self.document
        """
        self.compose() # Allow inheriting classes to compose all pages.
        self.doc.build() # Make sure to build the document
        self.doc.export(path)

if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]