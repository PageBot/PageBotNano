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
        self.id = id.strip()
        self.title = title.strip()

class SiteData(BaseData):
    def __init__(self, id, title):
        BaseData.__init__(self, id, title)
        self.data = {}
        self.pages = [] # As list, to keep the order in menu and navigation

    def __repr__(self):
        s = '<%s' % self.__class__.__name__
        if self.id:
            s += ' id=%s' % self.id
        if self.title:
            s += ' title="%s"' % self.title
        s += ' pages=%d' % len(self.pages)
        s += ' data=%d' % len(self.data)
        s += '>'
        return s

class PageData(BaseData):
    def __init__(self, id, title, template):
        BaseData.__init__(self, id, title)
        self.template = template
        self.data = {}
        self.elements = {}

    def __repr__(self):
        s = '<%s' % self.__class__.__name__
        if self.id:
            s += ' id=%s' % self.id
        if self.title:
            s += ' title="%s"' % self.title
        s += ' elements=%d' % len(self.elements)
        s += ' data=%d' % len(self.data)
        s += '>'
        return s

class ElementData(BaseData):
    def __init__(self, id, title, content):
        BaseData.__init__(self, id, title)
        self.content = content

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