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

class BaseData:
    def __init__(self, id=None, title=None):
        self.id = id or 'untitledSiteId'
        self.title = title or 'untitledPageName'

class SiteData(BaseData):
    def __init__(self, id=None, title=None, theme=None):
        BaseData.__init__(self, id, title)
        self.theme = theme or DefaultTheme()
        self.pages = [] # As list, to keep the order in menu and navigation

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
        self.elements = {}

    def __repr__(self):
        s = '<%s' % self.__class__.__name__
        if self.id:
            s += ' id=%s' % self.id
        if self.title:
            s += ' title="%s"' % self.title
        s += ' elements=%d' % len(self.elements)
        s += '>'
        return s

class ElementData(BaseData):
    def __init__(self, id=None, title=None, content=None):
        BaseData.__init__(self, id, title)
        self.content = content or ''

    def __repr__(self):
        s = '<%s' % self.__class__.__name__
        if self.id:
            s += ' id=%s' % self.id
        if self.title:
            s += ' title="%s"' % self.title
        if self.content:
            s += ' content="%s">' % self.content[:40]
        return s

    def _get_html(self):
        html = self.title
        if self.content:
            html += ' '+self.content
        return html
    html = property(_get_html)

    def _get_url(self):
        url = self.title # Plain url or <img src="path">?
        if '"' in url:
            url = re.findall('src=\"([^\"]*)', url)[0]
        return url
    url = property(_get_url)
        
if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]