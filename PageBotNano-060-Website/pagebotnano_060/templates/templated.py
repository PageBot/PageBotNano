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
#   Templates are functions with a standard attribute interface, that
#   can be stored in elements to initialize and compose their content.
#
import os, codecs, shutil, re
import sys
sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano_060.templates.base import BaseTemplates
from pagebotnano_060.toolbox import path2DirectoryName, path2CoreFileName
from pagebotnano_060.toolbox.dating import now

class Templated(BaseTemplates):
    """    
    The Templated reads all templates sources, ending with .css,
    .js and .html, and keeps them as strings that can be altered
    and queried.
    The Templated class is based on the structure of the https://templated.co
    template structure, adapted to be used with PageBotNano.

    >>> wt = Templated()
    >>> wt
    <Templated templates=3 css=2 js=5 images=11 fonts=6>
    """
    def __init__(self, path=None): # Standard API for all templates
        if path is None:
            path = 'sources/templated-hielo/'
        if not path.endswith('/'):
            path += '/'
        self.path = path
        self.pageName = None # Name key of current selected page
        self.htmlTemplates = {} # Key is file path, value is file text content.
        self.html = {} # Key is file path, value is file procesed page content.
        self.css = {} # Anchor substitution directly on this file content.
        self.js = {} # Anchor substitution directly on this file content.
        self.images = []
        self.pdf = []
        self.fonts = []
        self.otherFiles = [] # List with other files that need to be copied

        self.read(path)

    def __repr__(self):
        return '<%s templates=%d css=%d js=%d images=%d fonts=%d>' % (self.__class__.__name__,
            len(self.htmlTemplates), len(self.css), len(self.js), len(self.images), len(self.fonts))

    def keys(self):
        return self.htmlTemplates.keys()

    def __getitem__(self, templateId, pageData):
        return htmlTemplates.get(templateId)


    def _menuLinks(self, siteData, pageData=None):
        """Answer the html chunk as menu to all pages of the site.
        """
        html = """\n\t<ul class="links">"""
        for pageData in siteData.pages:
            html += """\n\t\t<li><a href="%s.html">%s</a></li>""" % (pageData.id, pageData.title)
        html += """\n\t</ul>\n"""
        return html

    def _bannerSlideShow(self, siteData, pageData):
        """Answer a list of <article> html chunks, as slides in the slide show
        <article>
            <img src="{{bannerImage 1}}"/>
            <div class="inner">
                <header>
                    <p>{{bannerSubtitle 1}}</p>
                    <h2>{{bannerTitle 1}}</h2>
                </header>
            </div>
        </article>
        """
        html = ''
        for n in range(1, 100): # Practical maximum amount of slides possible:
            bannerImage = 'bannerImage %d' % n
            bannerTitle = 'bannerTitle %d' % n
            bannerSubtitle = 'bannerSubtitle %d' % n
            if bannerImage in pageData.data or bannerTitle in pageData.data or bannerSubtitle in pageData.data:
                html += """\n\t<article>"""
                if bannerImage in pageData.data:
                    url = pageData.data[bannerImage].title
                    html += """\n\t\t'<img src="%s"/>""" % url
                html += """\n\t\t<div class="inner">\n\t\t\t<header>"""
                if bannerSubtitle in pageData.data:
                    html += """\n\t\t\t\t<p>%s</p>""" % pageData.data[bannerSubtitle].html # title + content
                if bannerTitle in pageData.data:
                    html += """\n\t\t\t\t<h2>%s</h2>""" % pageData.data[bannerTitle].html # title + content
                html += """\n\t\t\t</header>\n\t\t</div>\n\t</article>\n"""
        return html

    def _imageArticles(self, siteData, pageData):
        """Answer the html chunk of imageArticles "One" (style 2) in index.html template

        <div class="inner">
            <div class="grid-style">

                <div>
                    <div class="box">
                        <div class="image fit">
                            <img src="{{image 1}}" alt="" />
                        </div>
                        <div class="content">
                            <header class="align-center">
                                <p>subHead 1</p>
                                <h2>head 1</h2>
                            </header>
                            <p> {{article 1}}</p>
                            <footer class="align-center">
                                <a href="#" class="button alt">more1</a>                                
                            </footer>
                        </div>
                    </div>
                </div>
                ...
            </div>
        </div>
        """
        html = """\n<div class="inner">\n\t\t<div class="grid-style">"""
        for n in range(1, 100): # Partical maximum amount of imageArticles possible
            article = 'article %d' % n
            articleImage = 'articleImage %d' % n
            articleHead = 'articleHead %d' % n
            articleSubhead = 'articleSubhead %d' % n
            articleFooter = 'articleFooter %d' %n
            if (articleImage in pageData.data or 
                articleHead in pageData.data or 
                articleSubhead in pageData.data or
                article in pageData.data):
                html += """\n\t\t\t<div>\n\t\t\t\t<div class="box">"""
                if articleImage in pageData.data:
                    html += """\n\t\t\t\t\t<div class="image fit">\n\t\t\t\t\t\t<img src="%s"/>\n\t\t\t\t\t</div>""" % pageData.data[articleImage].title
                html += """\n\t\t\t\t\t<div class="content">"""
                if articleHead in pageData.data or articleSubhead in pageData.data:
                    html += """\n\t\t\t\t\t\t<header class="align-center">"""
                    if articleSubhead in pageData.data:
                        html += """\n\t\t\t\t\t\t\t<p>%s</p>""" % pageData.data[articleSubhead].html
                    if articleHead in pageData.data:
                        html += """\n\t\t\t\t\t\t\t<h2>%s</h2>""" % pageData.data[articleHead].html
                    html += """\n\t\t\t\t\t\t</header>"""
                if article in pageData.data:
                    html += """<p>%s</p>""" % pageData.data[article].html
                if articleFooter in pageData.data:
                    html += """\n\t\t\t\t\t\t<footer class="align-center">%s</footer>""" % pageData[articleFooter].html
                html += """\n\t\t\t\t</div>\n\t\t\t</div>"""
        html += """</div>"""
        return html

    def _gallery(self, siteData, pageData=None):
        """
        <div class="inner">
            <header class="align-center">
                <p class="special">{{gallerySubhead}}</p>
                <h2>{{galleryHead}}</h2>
            </header>
            <div class="gallery">
                <div>
                    <div class="image fit">
                        <a href="#"><img src="images/pic01.jpg" alt="" /></a>
                    </div>
                </div>
                ...
            </div>
        </div>
        """
        html = """\n<div class="inner">"""
        galleryHead = 'galleryHead'
        gallerySubhead = 'gallerySubhead'
        if galleryHead in pageData.data or gallerySubhead in pageData.data:
            html += """\n\t<header class="align-center">"""
            if gallerySubhead in pageData.data:
                html += """\n\t\t<p class="special">%s</p>""" % pageData.data[gallerySubhead].html
            if galleryHead in pageData.data:
                html += """\n\t\t<h2">%s</h2>""" % pageData.data[galleryHead].html
            html += """\n\t</header>\n\t\t<div class="gallery">"""
            for n in range(1, 100): # Partical maximum amount of imageArticles possible
                galleryImage = 'galleryImage %d' % n
                if galleryImage in pageData.data:
                    html += """\n\t\t<div>\n\t\t\t<div class="image fit">"""
                    html += """\n\t\t\t\t<a href="#"><img src="%s"/></a>""" % pageData.data[galleryImage].title
                    html += """\n\t\t\t</div>"""
                    galleryCaption = 'galleryCaption %d' % n
                    if galleryCaption in pageData.data:
                        html += """\n\t\t\t<div class="caption">%s</div>""" % pageData.data[galleryCaption].title
                    html += """\n\t\t</div>"""

            html += """\n\t\t</div>"""
        html += """\n</div>"""
        return html

    def _pullQuote(self, siteData, pageData):
        """Add numbered pullquote with background images
        <section id="two" class="wrapper style3" style="background-image: url({{pullQuoteImage 1}});">
            <div class="inner">
                <header class="align-center">
                    <p>{{pullQuoteSubhead 1}}</p>
                    <h2>{{pullQuoteHead 1}}</h2>
                </header>
            </div>
        </section>
        """
        html = ''
        for n in range(1, 100): # Partical maximum amount of imageArticles possible
            pullQuoteImage = 'pullQuoteImage %d' % n
            pullQuoteSubhead = 'pullQuoteSubhead %d' % n
            pullQuoteHead = 'pullQuoteHead %d' % n
            if pullQuoteImage in pageData.data or pullQuoteSubhead in pageData.data or pullQuoteHead in pageData.data:
                html +=  """\n\t<section class="wrapper style3" """
                if pullQuoteImage in pageData.data:
                    html += """ style="background-image: url(%s);" """ % pageData.data[pullQuoteImage].url
                html += '>'
                if pullQuoteSubhead in pageData.data or pullQuoteHead in pageData.data:
                    html += """\n\t\t<div class="inner">\n\t\t<header class="align-center">"""
                    if pullQuoteSubhead in pageData.data:
                        html += """\n\t\t\t<p>%s</p>""" % pageData.data[pullQuoteSubhead].html
                    if pullQuoteHead in pageData.data:
                        html += """\n\t\t\t<h2>%s</h2>""" % pageData.data[pullQuoteHead].html
                    html += """\n\t\t</header>\n\t</div>"""
                html += """\n\t</section>"""
        return html

    def _year(self, siteData, pageData=None):
        return now().year

    def _readFile(self, path):
        f = codecs.open(path, 'r', encoding='utf-8')
        txt = f.read()
        f.close()
        return txt

    def _writeFile(self, path, data):
        fileDir = path2DirectoryName(path)
        if not os.path.exists(fileDir):
            os.makedirs(fileDir)
        f = codecs.open(path, 'w', encoding='utf-8')
        f.write(data)
        f.close()

    def _copyFile(self, srcPath, dstPath):
        dstDir = path2DirectoryName(dstPath)
        if not os.path.exists(dstDir):
            os.makedirs(dstDir)
        shutil.copyfile(srcPath, dstPath)

    def read(self, path):
        """Read all files in the templated folder, holding the templates
        for a (simple) website, such as .html files, .css and .js,
        For images and fonts, just the path name is stored, for later 
        reference to copy to the target folder.
        """
        if os.path.isdir(path): 
            if not path.endswith('/'):
                path += '/'
            for fileName in os.listdir(path):
                self.read(path + fileName)
        elif path.lower().endswith('.html'):
            fileId = path2CoreFileName(path)
            self.htmlTemplates[fileId] = self._readFile(path)
        elif path.lower().endswith('.css'):
            self.css[path] = self._readFile(path)
        elif path.lower().endswith('.js') or path.lower().endswith('script'):
            self.js[path] = self._readFile(path)
        elif path.split('.')[-1] in ('gif', 'jpg', 'jpeg', 'png'):
            self.images.append(path)
        elif path.lower().endswith('pdf'):
            self.pdf.append(path)
        elif path.lower().split('.')[-1] in ('eot', 'svg', 'ttf', 'otf', 'woff', 'woff2'):
            self.fonts.append(path)
        else:
            self.otherFiles.append(path)

    def export(self, path):
        if not path.endswith('/'):
            path += '/'
        if not os.path.exists(path):
            os.makedirs(path)
        # Export the (possibly modified) file
        for pageId, html in self.html.items():
            filePath = path + pageId.split(self.path)[-1] + '.html'
            self._writeFile(filePath, html)
        for cssPath, css in self.css.items():
            filePath = path + cssPath.split(self.path)[-1]
            self._writeFile(filePath, css)
        for jsPath, js in self.js.items():
            filePath = path + jsPath.split(self.path)[-1]
            self._writeFile(filePath, js)
        # Copy these files by path to export path
        for srcPaths in (self.images, self.pdf, self.fonts, self.otherFiles):
            for srcPath in srcPaths:
                dstPath = path + srcPath.split(self.path)[-1]
                self._copyFile(srcPath, dstPath)

    def getTemplate(self, templateId):
        if not templateId in self.htmlTemplates:
            print('Templated warning: Cannot find template "%s". Using "index" instead' % templateId)
            templateId = 'index'
        return self.htmlTemplates[templateId]

    def getAnchors(self, templateId):
        anchorPattern = re.compile('{{([^}]*)}}')
        anchors = set()
        if not templateId in self.htmlTemplates:
            templateId = 'index'
        template = self.htmlTemplates[templateId]
        for anchor in anchorPattern.findall(template):
            anchors.add(anchor)

        for d in (self.css, self.js):
            for src in d.values():
                for anchor in anchorPattern.findall(src):
                    anchors.add(anchor)
        return anchors



if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]