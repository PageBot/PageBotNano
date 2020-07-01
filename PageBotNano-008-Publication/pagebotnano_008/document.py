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
import os # Import standard Python library to create the _export directory
import sys # Import access to some deep Python functions

if __name__ == "__main__":
    sys.path.insert(0, "..") # So we can import pagebotnano002 without installing.

from pagebotnano_008.constants import A4, EXPORT_DIR
from pagebotnano_008.page import Page
from pagebotnano_008.elements import Element
from pagebotnano_008.contexts.drawbotcontext import DrawBotContext

class Document:
    # Class names start with a capital. See a class as a factory
    # of document objects (name spelled with an initial lower case.)
    
    def __init__(self, w=None, h=None, context=None):
        """This is the "constructor" of a Document instance (=object).
        It takes two attributes: `w` is the general width of pages and
        `h` is the general height of pages.
        If omitted, a default A4 page size is taken.

        >>> doc = Document()
        >>> doc
        <Document w=595 h=842 pages=0>
        >>> page = doc.newPage()
        >>> page = doc.newPage()
        >>> doc
        <Document w=595 h=842 pages=2>
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
        # Keep the flag is self.build was already executed when calling self.export
        self.hasBuilt = False
        # Store the context in the Document. Use DrawBotContext by default.
        if context is None:
            context = DrawBotContext()
        self.context = context

    def __repr__(self):
        # This method is called when print(document) is executed.
        # It shows the name of the class, which can be different, if the
        # object inherits from Document.
        return '<%s w=%d h=%d pages=%d>' % (self.__class__.__name__, 
            self.w, self.h, len(self.pages))

    def newPage(self, w=None, h=None):
        """Create a new page. If the (w, h) is undefined, then take the current
        size of the document.

        >>> doc = Document()
        >>> doc.newPage()
        <Page pn=1 w=595 h=842 elements=0>
        """
        # Make a new page and add the page number from the total number of pages.
        # Note that the page number is 1 higher (starting at 1) than its index
        # will be in self.pages.
        page = Page(w or self.w, h or self.h, pn=len(self.pages)+1) 
        self.pages.append(page)
        return page # Answer the new create page, so the caller add elements to it.

    def build(self):
        """Build the document by looping trough the pages, an then recursively
        tell every page to build itself (and its contained elements).
        """
        # Clear all previous drawing in the context canvas.
        self.context.newDrawing()

        # Tell each page to build itself in context, including their child elements.
        for page in self.pages:
            page.build(self) # Passing self as document, in case the page needs more info.
        self.hasBuilt = True # Flag that we did this, in case called separate from self.export.

    def export(self, path, force=False, multipage=True):
        """Export the document into the _export folder. We assume that the 
        document and pages are built. We don't do that here, in case multiple
        formats are saved from the same build.
        If `force` is True or if build has not been done yet, then call
        self.build anyway.

        >>> doc = Document()
        >>> doc.newPage()
        <Page pn=1 w=595 h=842 elements=0>
        >>> doc.export('_export/Document-export.pdf')
        """
        if force or not self.hasBuilt: # If forced or not done yet, build the pages.
            self.build()

        if path.startswith(EXPORT_DIR) and not os.path.exists(EXPORT_DIR):
            os.mkdir(EXPORT_DIR)
        # Now all the pages drew them themselfs, we can export to the path.
        # let the context do its work, saving it.
        self.context.saveImage(path, multipage=multipage)

if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]