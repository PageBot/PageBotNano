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
#   This source makes it possible to import other sources
#   from this directory/folder
#
class BaseTemplates:
    """Defines the mininum set of page generating/composing functions that a
    template should implement. Otherwise raise an error.
    """
    def __init__(self):
        pass

    def __repr__(self):
        return '<%s>' % self.__class__.__name__
        
    def cover(self, doc):
        raise NotImplementedError

    def frenchTitle(self, doc):
        raise NotImplementedError

    def title(self, doc):
        raise NotImplementedError

    def tableOfContent(self, doc):
        raise NotImplementedError

    def page(self, doc):
        """The "page" template always must be there.
        This default beavior.
        """
        return doc.newPage()

    def index(self, doc):
        raise NotImplementedError

    def colophon(self, doc):
        raise NotImplementedError

