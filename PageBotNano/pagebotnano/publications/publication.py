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
    sys.path.insert(0, "../..") # So we can import pagebotnano002 without installing.

from pagebotnano.document import Document
from pagebotnano.constants import CENTER

class Case:
    """Case of resources, used while composing pages, as passed over to templates.
    """
    pass

class Publication:
    """The Publication base class is a wrapper around a document.
    Inheriting publication classes implement specific knowledge
    about types of publications, such as Book, Type Specimen,
    Website or Corporate Identity.

    >>> from random import random
    >>> from pagebotnano.elements import Rect, Text
    >>> from pagebotnano.babelstring import BabelString
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
    def __init__(self, w=None, h=None, templates=None, theme=None, context=None):
        self.doc = Document(w=w, h=h, context=context)
        self.templates = templates
        self.theme = theme

    def newCase(self, galley=None, page=None):
        case = Case()
        case.publication = self 
        case.doc = self.doc 
        case.page = page # Optional current page to start flows.
        case.galley = galley
        case.theme = self.doc.theme
        case.styles = self.doc.theme.styles
        case.templates = self.doc.templates
        case.template = None
        case.elements = [] # Selected galley elements for the current template
        case.errors = []
        case.verbose = []
        return case

    def compose(self, galley):
        """Composing the publication allows inheriting class
        to create pages, fill them with elements and add content.
        """
        raise NotImplementedError

    def export(self, path):
        """Export the publication as document, by passing the path
        on to self.document
        """
        self.doc.build() # Make sure to build the document
        self.doc.export(path)

if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]