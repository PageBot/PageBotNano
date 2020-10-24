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
    >>> pageData = parseMarkdownFile('../../PublishingVariables.md')
    >>> templatePath = '../templates/sources/templated-hielo'
    >>> #templatePath = '../templates/sources/templated-interphase'
    >>> #templatePath = '../templates/sources/px-layered-html-cyan'
    >>> templates = Templated(templatePath)
    >>> sorted(templates.getAnchors())
    >>> website = Website(theme=theme, templates=templates)
    >>> website.templates is templates
    True
    >>> website.compose(pageData)
    >>> # Start MAMP to see this website on localhost, port 80
    >>> website.export(website.MAMP_PATH + siteName)
    >>> url = 'http:localhost:%d/%s' % (website.PORT or 80, siteName) 
    >>> result = os.system(u'/usr/bin/open %s' % url)

    """  
    # Mamp 6 assumes Apache sites in user Site/localhost
    MAMP_PATH = '~/Sites/localhost/'  # MAMP v6
    MAMP_PATH = '/Applications/MAMP/htdocs/' # MAMP v5 and earlier  

    PORT = 8888
    #PORT = 80 # Default for self.port

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

    def compose(self, pages):
        """This is the core of a publication, composing the specific
        content of the document. The compose method gets called
        before building and exporting the self.doc document.

        pages is a dictionary of PageData instance, key is pageData.id
        There are some directions how the content is distributed on the 
        template anchors.

        Cross matching the pageData with the anchors in the template
        and the available methods define in the self.templates instance.

        """
        #print('Templates', self.templates.htmlTemplates.keys())
        anchors = self.templates.getAnchors() # {{Anchors}} of the website to be filled.
        for pageId, pageData in pages.items():
            if not pageData.id in self.templates.htmlTemplates:
                print('Cannot find page template', pageData.id)
                pageData.id = 'index.html'
            #print('==3=3=', pageData.elementData.get('logo'))
            print('+++++++', pageData.md)
            # Copy the template HTML into the page storage
            html = self.templates.htmlTemplates[pageData.id]
            #html = html.replace('{{logo}}', pageData.elementData['logo'])
            # html contains {{anchorName}} patterns.
            for anchorName in anchors:
                print(path, anchorName)
                pass

            self.templates.html[pageData.id] = html # Store the processed html

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