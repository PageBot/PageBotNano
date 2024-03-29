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
import sys
sys.path.insert(0, "..") # So we can import pagebotnano without installing.

from pagebotnano_020.constants import A4, EXPORT_DIR
from pagebotnano_020.elements import Element, Page
from pagebotnano_020.contexts.drawbotcontext import DrawBotContext
from pagebotnano_020.toolbox import makePadding
from pagebotnano_020.themes import DefaultTheme
from pagebotnano_020.templates.onecolumn import OneColumnTemplates

class ComposerData:
    """Collection of running resources, used while composing pages, 
    as passed over to templates. A ComposerData instance is created
    by Document and stored as doc.cd 

    >>> doc = Document()
    >>> page = doc.newPage()
    >>> page is doc.cd.page # Current page is stored in the ComposerData
    True
    >>> doc.pages[0] is doc.cd.page
    True
    """
    def __init__(self, page=None, galley=None, template=None):
        self.page = page
        self.galley = galley
        self.template = template  # Current running template name
        self.elements = [] # Selected galley elements for the current template
        self.errors = []
        self.verbose = []

    def _get_template(self):
        return self._template
    def _set_template(self, template):
        assert template is None or isinstance(template, str), ('%s:template: should be None or string "%s"' % (self.__class__.__name__, template))
        self._template = template
    template = property(_get_template, _set_template)

    def _get_pn(self):
        if self.page is not None:
            return self.page.pn
        return None
    pn = property(_get_pn)

class Document:
    # Class names start with a capital. See a class as a factory
    # of document objects (name spelled with an initial lower case.)
    
    def __init__(self, w=None, h=None, pt=None, pr=None, pb=None, pl=None,
        theme=None, templates=None, context=None):
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
        self.padding = pt, pr, pb, pl # Initialize the default padding
        # Storage for the pages in this document
        self.pages = [] # Simple list, the index is the page number (starting at 0)

        # The TemplateSet dictionary contains a set of functions that
        # compose the pages and containing elements for a particular
        # type of publications.
        if templates is None:
            templates = OneColumnTemplates()
        self.templates = templates

        # The theme contains (or can produce) all stylistic parameters
        # of a publication, such as color, typographic values and the 
        # selected mood (lightest, light, dark, darkest) to create
        # dark-on-light or light-on-dark moods with the same color palette.
        if theme is None: # If not default, we choose one here.
            theme = DefaultTheme()
        self.theme = theme

        # Storage of composer data, while a session runs with this document.
        self.cd = ComposerData() 

        # Keep the flag is self.build was already executed when calling self.export
        self.hasComposed = False
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

    def _get_padding(self):
        """Answer a tuple of the 4 padding values of the element

        >>> doc = Document(pl=10)
        >>> doc.padding # Other values are default PADDING
        (30, 30, 30, 10)
        """
        return self.pt, self.pr, self.pb, self.pl 
    def _set_padding(self, padding):
        self.pt, self.pr, self.pb, self.pl = makePadding(padding)
    padding = property(_get_padding, _set_padding)

    def _get_pw(self):
        """Answer the usable element space, withing the horizontal padding

        >>> doc = Document(w=500, pl=100, pr=50)
        >>> doc.pw
        350
        """
        return self.w - self.pl - self.pr
    pw = property(_get_pw)

    def _get_ph(self):
        """Answer the usable element space, withing the vertical padding

        >>> doc = Document(h=500, pt=100, pb=50)
        >>> doc.ph
        350
        """
        return self.h - self.pt - self.pb
    ph = property(_get_ph)

    def newPage(self, w=None, h=None, name=None, template=None):
        """Create a new page. If the (w, h) is undefined, then take the current
        size of the document.

        >>> doc = Document()
        >>> doc.newPage()
        <Page pn=1 w=595 h=842 elements=0>
        """
        # Make a new page and add the page number from the total number of pages.
        # Note that the page number is 1 higher (starting at 1) than its index
        # will be in self.pages.
        self.cd.page = Page(w=w or self.w, h=h or self.h, pn=len(self.pages)+1,
            name=name, template=template) 
        self.addPage(self.cd.page)
        return self.cd.page # Answer the new create page, so the caller add elements to it.

    def addPage(self, page):
        """Add the page to self.pages. If the page.w or page.h is undefined, then
        set them with the document size.

        >>> doc = Document()
        >>> page = Page()
        >>> page.w, page.h
        (None, None)
        >>> doc.addPage(page)
        >>> page.w, page.h
        (595, 842)
        >>> page is doc.cd.page # ComposerData stores current selected page
        True
        """
        if page.w is None:
            page.w = self.w
        if page.h is None:
            page.h = self.h
        self.cd.page = page
        self.pages.append(page)

    def compose(self):
        """Compose the document, by looking through the pages, and the recursively
        tell every page to compose itself (and its comtained elements).

        >>> doc = Document()
        >>> page = doc.newPage()
        >>> page = doc.newPage()
        >>> page = doc.newPage()
        >>> doc.compose()
        """
        for page in self.pages:
            self.cd.page = page
            page.compose(doc=self) # Passing self as document, in case the page needs more info
        self.hasComposed = True # Flag that we did this, in case called separate from self.export

    def build(self):
        """Build the document by looping trough the pages, and then recursively
        tell every page to build itself (and its contained elements).
        """
        # Clear all previous drawing in the context canvas.
        self.context.newDrawing()

        # Tell each page to build itself in context, including their child elements.
        for page in self.pages:
            self.cd.page = page # Store as current selected page
            page.build(doc=self) # Passing self as document, in case the page needs more info.
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
        if force or not self.hasComposed: # If forced or not done yet, compose the pages.
            self.compose()

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