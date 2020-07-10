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
class BaseTemplate:
    """Defines the mininum set of page generating/composing functions that a
    template should implement. Otherwise raise an error.
    """
    @classmethod
    def coverPage(cls, theme, doc, page=None, parent=None, **kwargs):
        raise NotImplementedError

    @classmethod
    def tableOfContentPage(cls, theme, doc, page=None, parent=None, **kwargs):
        raise NotImplementedError

    @classmethod
    def indexPage(cls, theme, doc, page=None, parent=None, **kwargs):
        raise NotImplementedError

    @classmethod
    def oneColumnPage(cls, theme, doc, page=None, parent=None, **kwargs):
        raise NotImplementedError

    @classmethod
    def oneColumnPage(cls, theme, doc, page=None, parent=None, **kwargs):
        raise NotImplementedError

