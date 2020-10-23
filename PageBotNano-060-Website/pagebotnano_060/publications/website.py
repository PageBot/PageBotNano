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
    >>> theme = BackToTheCity()
    >>> title = randomTitle()
    >>> author = randomName()
    >>> xml = '<xml><h1>%s</h1><p>%s</p></xml>' % (title, (loremipsum() + ' ') * 50)
    >>> siteName = 'pagebotnano_demo'
    >>> templatePath = '../templates/sources/templated-hielo'
    >>> #templatePath = '../templates/sources/templated-interphase'
    >>> #templatePath = '../templates/sources/px-layered-html-cyan'
    >>> templates = Templated(templatePath)
    >>> sorted(templates.getAnchors())
    >>> website = Website(theme=theme, templates=templates)
    >>> website.templates is templates
    True
    >>> # Start MAMP to see this website on localhost, port 80
    >>> website.export(website.MAMP_PATH + siteName) 
    >>> result = os.system(u'/usr/bin/open %s' % 'http:localhost/' + siteName)

    """  
    # Mamp 6 assumes Apache sites in user Site/localhost
    MAMP_PATH = '~/Sites/localhost/'  

    def compose(self, pages):
        """This is the core of a publication, composing the specific
        content of the document. The compose method gets called
        before building and exporting the self.doc document.

        pageData is a dictionary of PageData instance, key is pageData.id
        There are some directions how the content is distributed on the 
        template anchors.

        Cross matching the pageData with the anchors in the template
        and the available methods define in the self.templates instance.

        """
        print(pages)
        anchors = self.templates.getAnchors()
        for path, html in self.templates.html.items():
            for anchorName in anchors:
                print(path, anchorName)
                pass
            pass
            #print(path)
        #print('Composing')

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