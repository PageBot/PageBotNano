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
 
from pagebotnano_060.constants import CENTER, LEFT, RIGHT, EN, MAIN
from pagebotnano_060.publications.publication import Publication
from pagebotnano_060.document import Document
from pagebotnano_060.elements import Rect, Text, TextBox, Image
from pagebotnano_060.babelstring import BabelString
from pagebotnano_060.toolbox.typesetter import Typesetter

class Website(Publication):
    """A Website publication takes a volume of text/imges source
    as markdown document, and merges that into an existing HTML website
    that contains markers where to place the context.

    >>> from pagebotnano_060.constants import A5
    >>> from pagebotnano_060.toolbox.loremipsum import loremipsum, randomName, randomTitle
    >>> from pagebotnano_060.templates.webtemplates import WebTemplates
    >>> from pagebotnano_060.themes import BackToTheCity
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
    >>> templatePath = '../../../templates/templated-hielo'
    >>> templates = WebTemplates(templatePath)
    >>> website = Website(w=w, h=h, theme=theme, galley=galley, templates=templates)
    >>> website.export('_export/website')
    """
    MAX_PAGES = 100
    
    def compose(self):
        """This is the core of a publication, composing the specific
        content of the document. The compose method gets called
        before building and exporting the self.doc document.
        """
        print('Composing')

if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]