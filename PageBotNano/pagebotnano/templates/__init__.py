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
    @classmethod
    def cover(cls, doc):
        raise NotImplementedError

    @classmethod
    def frenchTitle(cls, doc):
        raise NotImplementedError

    @classmethod
    def title(cls, doc):
        raise NotImplementedError

    @classmethod
    def tableOfContent(cls, doc):
        raise NotImplementedError

    @classmethod
    def page(cls, doc):
        raise NotImplementedError

    @classmethod
    def index(cls, doc):
        raise NotImplementedError

    @classmethod
    def colophon(cls, doc):
        raise NotImplementedError

