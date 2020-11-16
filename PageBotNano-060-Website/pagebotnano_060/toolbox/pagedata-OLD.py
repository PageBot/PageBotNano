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
#   pagedata.py
#
#   PageData is the container of parsed data reading from a markdown file
#   to be matched and substituting in the template {{anchorName}} anchors.
#
class BaseData:
    def __init__(self, id, title):
        self.id = (id or 'noname').strip()
        self.title = (title or 'Untitled').strip()

class SiteData(BaseData):
    """Collect all global site attributes and the list of PageData pages.

    >>> site = SiteData('domain', 'Site title')
    >>> site
    <SiteData id=domain title="Site title" pages=0 data=2>
    >>> site.newPage('index')
    <PageData id=index title="Untitled" elements=0 data=2>
    """
    def __init__(self, id, title):
        BaseData.__init__(self, id, title)
        self.id = id
        self.title = title or 'Untitled site'
        self._pages = [] # As list, to keep the order in menu and navigation

    def _get_pages(self):
        return self._pages
    pages = property(_get_pages)

    def __repr__(self):
        s = '<%s' % self.__class__.__name__
        if self.id:
            s += ' id=%s' % self.id
        if self.title:
            s += ' title="%s"' % self.title
        s += ' pages=%d' % len(self.pages)
        s += ' data=%d' % (len(self.__dict__)-1)
        s += '>'
        return s

    def newPage(self, id=None, title=None, template=None):
        page = PageData(id, title, template)
        self._pages.append(page)
        return page

class PageData(BaseData):
    def __init__(self, id, title, template):
        BaseData.__init__(self, id, title)
        self.template = template

    def __repr__(self):
        s = '<%s' % self.__class__.__name__
        if self.id:
            s += ' id=%s' % self.id
        if self.title:
            s += ' title="%s"' % self.title
        s += ' data=%d' % (len(self.__dict__)-2)
        s += '>'
        return s

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