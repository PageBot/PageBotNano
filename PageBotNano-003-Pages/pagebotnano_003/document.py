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
#   document.py
#
#   This source contains the class with knowledge about a generic document.
#
import sys # Import access to some deep Python functions
import os # Import standard Python library to create the _export directory
import drawBot

if __name__ == "__main__":
    sys.path.insert(0, "..") # So we can import pagebotnano003 without installing.

from pagebotnano_003.constants import *
from pagebotnano_003.page import Page
from pagebotnano_003.elements import Element

class Document:
    # Class names start with a capital. See a class as a factory
    # of document objects (name spelled with an initial lower case.)
    
    def __init__(self, w=None, h=None):
        """This is the "constructor" of a Document instance (=object).
        It takes two attributes: `w` is the general width of pages and
        `h` is the general height of pages.
        If omitted, a default A4 page size is taken.

        >>> doc = Document()
        >>> doc
        I am a Document(w=595 h=842 pages=0)
        """
        if w is None: # If not defined, take the width of A4
            w, _ = A4
        if h is None: # If not defined, then take the height of A4
            _, h = A4
        # Store the values in the document instance.
        self.w = w
        self.h = h
        # Storage for the pages in this document
        self.pages = [] # Simple list, the index is the page number (starting at 0)

    def __repr__(self):
        # This method is called when print(document) is executed.
        # It shows the name of the class, which can be different, if the
        # object inherits from Document.
        return 'I am a %s(w=%d h=%d pages=%d)' % (self.__class__.__name__, 
            self.w, self.h, len(self.pages))

    def newPage(self, w=None, h=None):
        """Create a new page. If the (w, h) is undefined, then take the current
        size of the document.
        """
        # Make a new page and add the page number from the total number of pages.
        page = Page(w or self.w, h or self.h, pn=len(self.pages)+1) 
        self.pages.append(page)
        return page # Return the created page as convenience for the caller.
        
    def build(self):
        """Build the document by looping trough the pages, an then recursively
        tell every page to build itself (and its contained elements).
        """
        # Tell each page to build itself in DrawBot.
        for page in self.pages:
            page.build(self) # Passing self as document, in case the page needs more info.

    def export(self, path, multipage=True):
        """Export the document into the _export folder. We assume that the 
        document and pages are built. We don't do that here, in case multiple
        formats are saved from the same build.

        """
        if path.startswith(EXPORT_DIR) and not os.path.exists(EXPORT_DIR):
            os.mkdir(EXPORT_DIR)
        # Now all the pages drew them themselfs, we can export to the path.
        # let DrawBot do its work, saving it.
        # The optional `multipage` parametes saves “single page file formats”
        # (such as PNG and JPG) into a numbered sequence of image files.
        drawBot.saveImage(path, multipage=multipage)

if __name__ == "__main__":
    import doctest
    doctest.testmod()[0]
