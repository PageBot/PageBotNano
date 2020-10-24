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

from pagebotnano_060.themes import HappyHolidays as DefaultTheme
from pagebotnano_060.templates.templated import Templated

class Publication:
    """The Publication base class is a wrapper around a document.
    Inheriting publication classes implement specific knowledge
    about types of publications, such as Book, Type Specimen,
    Website or Corporate Identity.

    >>> from random import random
    >>> pub = Publication() # Default size A4
    >>> pub.export('_export/website')
    """
    def __init__(self, theme=None, templates=None, context=None):       
        # In this approach there is no self.doc Document.
        if templates is None:
            templates = Templated()
        self.templates = templates

    def compose(self):
        """Composing the publication allows inheriting class
        to create pages, fill them with elements and add content.
        """
        pass

    def build(self):
        pass

    def export(self, path):
        """Export the publication as document, by passing the path
        on to self.document
        """
        pass

if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]