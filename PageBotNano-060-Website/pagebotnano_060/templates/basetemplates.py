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

from pagebotnano_060.toolbox import path2DirectoryName, path2CoreFileName

class BaseTemplates:
    """    
    The WebTemplates reads all templates sources, ending with .css,
    .js and .html, and keeps them as objects that can be altered
    and queried.
    """
    TEMPLATE_NAME = None # To be defined by inheriting template classes.

    def __init__(self, path=None): # Standard API for all templates
        if path is None:
            path = self.TEMPLATE_NAME # Use the default template name for this class.
            assert path is not None
        # Find the template, otherwise select one in the local resources
        path = self.locateTemplate(path)
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
        return '<%s html=%d css=%d js=%d images=%d fonts=%d>' % (self.__class__.__name__,
            len(self.html), len(self.css), len(self.js), len(self.images), len(self.fonts))

    @classmethod
    def locateTemplate(cls, path):
        """Try to locate the template folder from path. If the template
        cannot be found, then answer the path to a local default template.
        """
        if path is None:
            path = cls.TEMPLATE_NAME
        if not path.endswith('/'):
            path += '/'
        tryPaths = (
            path,
            'sources/' + path,
            'sources/' + cls.TEMPLATE_NAME,
            path2DirectoryName(__file__) + path,
            path2DirectoryName(__file__) + 'sources/' + path,
            path2DirectoryName(__file__) + 'sources/' + cls.TEMPLATE_NAME,
            )
        for tryPath in tryPaths: 
            if os.path.exists(tryPath):
                return tryPath
        return None

    def getTemplate(self, templateId):
        if not templateId in self.htmlTemplates:
            print('Templated warning: Cannot find template "%s". Using "index" instead' % templateId)
            templateId = 'index'
        return self.htmlTemplates[templateId]

    def keys(self):
        return self.htmlTemplates.keys()

    def __getitem__(self, templateId, pageData):
        return self.htmlTemplates.get(templateId)

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
        elif path.lower().endswith('.js'):
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

    def getAnchors(self):
        anchorPattern = re.compile('{{([^}]*)}}')
        anchors = set()
        for d in (self.html, self.css, self.js):
            for src in d.values():
                for anchor in anchorPattern.findall(src):
                    anchors.add(anchor)
        return anchors

    # Generic anchor replacements for all templates

    def _fontsCss(self, siteData, pageData, index):
        css = ''
        """
        logoFontFamily = self._indexed('imagesArticle', index) # Double indexed achor name
        if hasattr(siteData, logoFontFamily):
            css +=
        """
        css = """
 @font-face {
    font-family: '{{logoFontFamily}}';
    src: url('../fonts/{{logoFontFamily}}-Regular.eot') format('embedded-opentype'),
         url('../fonts/{{logoFontFamily}}-Regular.woff2') format('woff2'),
         url('../fonts/{{logoFontFamily}}-Regular.woff') format('woff'),
         url('../fonts/{{logoFontFamily}}-Regular.ttf') format('truetype');
    font-weight: normal;
    font-style: normal
 }
 @font-face {
    font-family: '{{fontFamily}}';
    src: url('../fonts/{{fontFamily}}-Regular.eot?v=4.6.3');
    src: url('../fonts/{{fontFamily}}-Regular.eot?#iefix&v=4.6.3') format('embedded-opentype'),
         url('../fonts/{{fontFamily}}-Regular.woff2?v=4.6.3') format('woff2'),
         url('../fonts/{{fontFamily}}-Regular.woff?v=4.6.3') format('woff');
    font-weight: normal;
    font-style: normal
 }
@font-face {
    font-family: '{{fontFamily}}';
    src: url('../fonts/{{fontFamily}}-Bold.eot?v=4.6.3');
    src: url('../fonts/{{fontFamily}}-Bold.eot?#iefix&v=4.6.3') format('embedded-opentype'),
         url('../fonts/{{fontFamily}}-Bold.woff2?v=4.6.3') format('woff2'),
         url('../fonts/{{fontFamily}}-Bold.woff?v=4.6.3') format('woff');
    font-weight: bold;
    font-style: normal;
 }
        """
        return css



if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]