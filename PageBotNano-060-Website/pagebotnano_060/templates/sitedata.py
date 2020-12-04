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
#   sitedata.py
#
#   SiteData and PageData are the containers of parsed data, defined from a Python
#   content file for a sizes. The attributes of SiteData and PageData instances
#   are matched matched and substituting in the template {{anchorName}} anchors.
#
import sys
sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano_060.themes import DefaultTheme
from pagebotnano_060.toolbox.color import color

class BaseData:
    def __init__(self, id=None, title=None):
        self.id = id or 'untitledSiteId'
        self.title = title or 'untitledPageName'

class SiteData(BaseData):
    def __init__(self, id=None, title=None, theme=None):
        """Initialize the default attributes, incase a Templated instance
        doesn't do it.

        >>> sd = SiteData()
        >>> sd.page # No pages yet
        []
        >>> sd.footerFontSize
        '1em'
        """
        BaseData.__init__(self, id, title)
        self.theme = theme or DefaultTheme()
        self.pages = [] # As list, to keep the order in menu and navigation

        # Initialize defaults that always should be filled for CSS
        # Default values as used in templates Hielo
        self.footerFont = 'Verdana'
        self.footerFontSize = '1em'
        self.footerColor = color(0)

        self.bannerFullHeight = '100vh' # Height of banners
        self.bannerFullHeightMax980 = '50vh' # Height of banner in media
        self.bannerFullHeightMax1280 = '75vh' # Height of banner in media
        self.bannerHalfHeight = '50vh' # Half height of banner

    def __repr__(self):
        s = '<%s' % self.__class__.__name__
        if self.id:
            s += ' id=%s' % self.id
        if self.title:
            s += ' title="%s"' % self.title
        s += ' pages=%d' % len(self.pages)
        s += '>'
        return s

    def newPage(self, id=None, title=None, template=None):
        page = PageData(id, title, template)
        self.pages.append(page)
        return page
        
class PageData(BaseData):
    def __init__(self, id=None, title=None, template=None):
        BaseData.__init__(self, id, title)
        self.template = template or 'index'

    def __repr__(self):
        s = '<%s' % self.__class__.__name__
        if self.id:
            s += ' id=%s' % self.id
        if self.title:
            s += ' title="%s"' % self.title
        s += '>'
        return s

     
if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]