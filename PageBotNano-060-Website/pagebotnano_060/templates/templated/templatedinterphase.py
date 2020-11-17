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
#   Interphase by TEMPLATED
#   templated.co @templatedco
#   Released for free under the Creative Commons Attribution 3.0 license (templated.co/license)
#   Modified to be used with PageBotNano
# -----------------------------------------------------------------------------
#
#   Templates are functions with a standard attribute interface, that
#   can be stored in elements to initialize and compose their content.
#
#   The TemplatedInterphase class supports the following anchors
#
#   siteData = SiteData(siteId, siteName)
#
#   siteData.menuName = 'Menu'
#   siteData.year = now().year
#   siteData.copyright = '<a href="https://typetr.typenetwork.com">TYPETR</a>'
#   siteData.fontFamily = 'Upgrade'
#   siteData.logo = """<img src="images/logo.png"/>"""
#   siteData.logoFontFamily = 'PepperTom'
#   siteData.monoFontFamily = 'Courier New'
#   siteData.menuLinks = True # Force call to templates._menuLinks()
#
import sys
sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano_060.templates.templated.templatedbase import TemplatedBase
from pagebotnano_060.toolbox.markdown import parseMarkdown

class TemplatedInterphase(TemplatedBase):
    """    
    The TemplatedInterphase reads all templates sources, ending with .css,
    .js and .html, and keeps them as strings that can be altered
    and queried.
    The Templated class is based on the structure of the https://templated.co
    template structure, Modified to be used with PageBotNano.

    >>> wt = TemplatedInterphase()
    >>> len(wt.htmlTemplates) > 0
    True
    """
    TEMPLATE_NAME = 'templated-interphase' # This class is optimised for this set of templates.

    def _menuLinks(self, siteData, pageData, index):
        """Answer the html chunk as menu to all pages of the site.
        """
        html = """\n<nav id="menu">\n\t<ul class="links">"""
        for pageData in siteData.pages:
            html += """\n\t\t<li><a href="%s.html">%s</a></li>""" % (pageData.id, pageData.title)
        html += """\n\t</ul>\n</nav>"""
        return html

if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]