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
import sys

if __name__ == "__main__":
    sys.path.insert(0, "../..") # So we can import pagebotnano without installing.
 
from pagebotnano_060.publications.publication import Publication
from pagebotnano_060.toolbox.color import Color

class Website(Publication):
    """A Website publication takes a volume of text/imges source
    as markdown document, and merges that into an existing HTML website
    that contains markers where to place the context.

    >>> from pagebotnano_060.toolbox.loremipsum import loremipsum, randomName, randomTitle
    >>> from pagebotnano_060.templates.templated import Templated
    >>> from pagebotnano_060.themes import BackToTheCity
    >>> from pagebotnano_060.toolbox.markdown import parseMarkdownFile
    >>> theme = BackToTheCity()
    >>> title = randomTitle()
    >>> author = randomName()
    >>> siteName = 'pagebotnano_demo'
    >>> pageData = parseMarkdownFile('../../TestPageContent.md')
    >>> #pageData = parseMarkdownFile('../../PublishingVariables.md')
    >>> templatePath = '../templates/sources/templated-hielo'
    >>> #templatePath = '../templates/sources/templated-interphase'
    >>> #templatePath = '../templates/sources/px-layered-html-cyan'
    >>> templates = Templated(templatePath)
    >>> website = Website(theme=theme, templates=templates)
    >>> website.templates is templates
    True
    >>> website.compose(pageData)
    >>> # Start MAMP to see this website on localhost, port 80
    >>> website.export(website.MAMP_PATH + siteName)
    >>> url = 'http:localhost:%d/%s' % (website.PORT or 80, siteName) 
    >>> result = os.system(u'/usr/bin/open %s' % url)

    """  
    # Mamp 6 assumes Apache sites in user Sites/localhost
    MAMP_PATH = os.path.expanduser('~/Sites/localhost/')  # MAMP v6
    #MAMP_PATH = '/Applications/MAMP/htdocs/' # MAMP v5 and earlier  

    #PORT = 8888
    PORT = 80 # Default for self.port

    def __init__(self, url=None, domain=None, port=None, **kwargs):
        Publication.__init__(self, **kwargs)
        self.port = port
        if domain is None:
            domain = 'localhost'
            if port and port != 80:
                domain += ':%d' % port
        if url is None:
            url = 'http:%s' % domain 
        self.url = url

    def compose(self, siteData):
        """This is the core of a publication, composing the specific
        content of the document. The compose method gets called
        before building and exporting the self.doc document.

        siteData is an attributed container also contains a list of PageData instances.
        There are some directions how the content is distributed on the 
        template anchors.

        Cross matching the siteData+pageData with the anchors in the template
        and the available methods define in the self.templates instance.

        """
        for pageData in siteData.pages:
            # Copy the template HTML into the page html
            html = self.templates.getTemplate(pageData.template)

            # Replace all remaining anchors by their data
            html = self.replaceAnchors(html, siteData, pageData)
            self.templates.html[pageData.id] = html

        # Convert the anchors in CSS and JS
        for d in (self.templates.css, self.templates.js):
            for path, src in d.items():
                src = self.replaceAnchors(src, siteData, clearAnchors=False)
                d[path] = src

    def replaceAnchors(self, src, siteData, pageData=None, clearAnchors=True):
        for data in (siteData, pageData):
            if data is None:
                continue
            for anchor, anchorContent in data.__dict__.items(): # Check on all attributes
                if anchorContent: # Can be just boolean, check on existing method first
                    anchorParts = anchor.split('_')
                    if len(anchorParts) > 1:
                        anchorIndex = int(anchorParts[1])
                    else:
                        anchorIndex = 0
                    anchorBase = anchorParts[0]
                    # In case self.templates._<anchor> is implenented, then call it, with siteData as attribute.
                    methodName = '_'+anchorBase
                    if hasattr(self.templates, methodName): # Implemented as method?
                        anchorContent = str(getattr(self.templates, methodName)(siteData, pageData, anchorIndex))
                        src = src.replace('{{%s}}' % anchor, anchorContent) # Replace, even if content produced empty string.
                    elif isinstance(anchorContent, Color):
                        src = src.replace('{{%s}}' % anchor, anchorContent.css) # Export in best CSS format
                    else: # Otherwise, try to use the content to replace the template anchor
                        src = src.replace('{{%s}}' % anchor, str(anchorContent))
                elif clearAnchors: # Content is set to False or None, remove all anchors.
                    src = src.replace('{{%s}}' % anchor, '')

        # Now try the remaining anchors to be replaced from the theme colors
        for colorName in siteData.theme.COLOR_NAMES: # Check on all theme attributes
            color = siteData.theme.getColor(colorName)
            cell = siteData.theme.getCell(colorName) # Chess-like color code
            src = src.replace('{{%s}}' % colorName, '#%s /* Theme: (%s) %s */' % (color.hex, cell, colorName))


        return src

    def build(self):
        pass

    def export(self, path=None):
        if path is None:
            path = '_export/'
        path = os.path.expanduser(path)
        #self.compose()
        #self.build()
        self.templates.export(path)

if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]