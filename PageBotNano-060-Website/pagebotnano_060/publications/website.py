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
from pagebotnano_060.toolbox.pagedata import ElementData

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
            if port:
                domain += ':%d' % port
        if url is None:
            url = 'http:%s' % domain 
        self.url = url

    def compose(self, siteData):
        """This is the core of a publication, composing the specific
        content of the document. The compose method gets called
        before building and exporting the self.doc document.

        pages is a dictionary of PageData instance, key is pageData.id
        There are some directions how the content is distributed on the 
        template anchors.

        Cross matching the pageData with the anchors in the template
        and the available methods define in the self.templates instance.

        """
        for pageData in siteData.pages:
            # Copy the template HTML into the page html
            html = self.templates.getTemplate(pageData.template)

            # Replace all remaining anchors by their data
            for anchorSet in (pageData, siteData):
                for anchor, anchorContent in anchorSet.data.items():
                    if anchorContent:
                        if isinstance(anchorContent, ElementData):
                            anchorContent = '%s %s' % (anchorContent.title, anchorContent.content)
                        html = html.replace('{{%s}}' % anchor, anchorContent.strip())

            # Still unchanged anchors left that have implemented methods in the templates?
            # In case self.templates._<anchor> is implenented, then call it, with siteData as attribute.
            for anchor in self.templates.getAnchors(pageData.id):
                methodName = '_'+anchor
                if hasattr(self.templates, methodName): # Implemented as method?
                    anchorContent = str(getattr(self.templates, methodName)(siteData, pageData))
                    html = html.replace('{{%s}}' % anchor, anchorContent.strip())

            self.templates.html[pageData.id] = html

        # Convert the anchors in CSS and JS
        for d in (self.templates.css, self.templates.js):
            for path, src in d.items():
                for anchor, anchorContent in siteData.data.items():
                    if anchorContent:
                        methodName = '_'+anchor
                        if hasattr(self.templates, methodName): # Implemented as method?
                            anchorContent = str(getattr(self.templates, methodName)(siteData))
                        elif isinstance(anchorContent, ElementData):
                            anchorContent = anchorContent.html
                        src = src.replace('{{%s}}' % anchor, anchorContent.strip())

                d[path] = src

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