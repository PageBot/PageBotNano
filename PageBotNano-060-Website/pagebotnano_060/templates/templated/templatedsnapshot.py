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
#   Snapshot by TEMPLATED
#   templated.co @templatedco
#   Released for free under the Creative Commons Attribution 3.0 license (templated.co/license)
#   Modified to be used with PageBotNano
# -----------------------------------------------------------------------------
#
#   Templates are functions with a standard attribute interface, that
#   can be stored in elements to initialize and compose their content.
#
#   The TemplatedSnapshot class supports the following anchors
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

class TemplatedSnapshot(TemplatedBase):
    """    
    The TemplatedSnapshot reads all templates sources, ending with .css,
    .js and .html, and keeps them as strings that can be altered
    and queried.
    The Templated class is based on the structure of the https://templated.co
    template structure, Modified to be used with PageBotNano.

    >>> wt = TemplatedSnapshot()
    >>> len(wt.htmlTemplates) > 0
    True
    """
    TEMPLATE_NAME = 'templated-snapshot' # This class is optimised for this set of templates.

    def _menuLinks(self, siteData, pageData, index):
        """Answer the html chunk as menu to all pages of the site.
        """
        html = """\n<nav id="menu">\n\t<ul class="links">"""
        for pageData in siteData.pages:
            html += """\n\t\t<li><a href="%s.html">%s</a></li>""" % (pageData.id, pageData.title)
        html += """\n\t</ul>\n</nav>"""
        return html

    def _subscriptionForm(self, siteData, pageData, index):
        html = ''
        subscriptionFormHead = self._indexed('subscriptionFormHead', index)
        if (hasattr(pageData, subscriptionFormHead)):
            html += """<h3>%s</h3>""" % getattr(pageData, subscriptionFormHead)

        html += """
                                    <form action="#" method="post">
                                        <div class="field half first">
                                            <label for="name">Name</label>
                                            <input name="name" id="name" type="text" placeholder="Name">
                                        </div>
                                        <div class="field half">
                                            <label for="email">Email</label>
                                            <input name="email" id="email" type="email" placeholder="Email">
                                        </div>
                                        <div class="field">
                                            <label for="message">Message</label>
                                            <textarea name="message" id="message" rows="6" placeholder="Message"></textarea>
                                        </div>
                                        <ul class="actions">
                                            <li><input value="Send Message" class="button" type="submit"></li>
                                        </ul>
                                    </form>
            """
        return html

    def _gallery(self, siteData, pageData, index):
        html = """
                                <section id="galleries">

                            <!-- Photo Galleries -->
                                <div class="gallery">
                                    <header class="special">
                                        <h2>What's New</h2>
                                    </header>
                                    <div class="content">
                                        <div class="media">
                                            <a href="images/fulls/01.jpg"><img src="images/thumbs/01.jpg" alt="" title="This right here is a caption." /></a>
                                        </div>
                                        <div class="media">
                                            <a href="images/fulls/05.jpg"><img src="images/thumbs/05.jpg" alt="" title="This right here is a caption." /></a>
                                        </div>
                                        <div class="media">
                                            <a href="images/fulls/09.jpg"><img src="images/thumbs/09.jpg" alt="" title="This right here is a caption." /></a>
                                        </div>
                                        <div class="media">
                                            <a href="images/fulls/02.jpg"><img src="images/thumbs/02.jpg" alt="" title="This right here is a caption." /></a>
                                        </div>
                                        <div class="media">
                                            <a href="images/fulls/06.jpg"><img src="images/thumbs/06.jpg" alt="" title="This right here is a caption." /></a>
                                        </div>
                                        <div class="media">
                                            <a href="images/fulls/10.jpg"><img src="images/thumbs/10.jpg" alt="" title="This right here is a caption." /></a>
                                        </div>
                                        <div class="media">
                                            <a href="images/fulls/03.jpg"><img src="images/thumbs/03.jpg" alt="" title="This right here is a caption." /></a>
                                        </div>
                                        <div class="media">
                                            <a href="images/fulls/07.jpg"><img src="images/thumbs/07.jpg" alt="" title="This right here is a caption." /></a>
                                        </div>
                                    </div>
                                    <footer>
                                        <a href="gallery.html" class="button big">Full Gallery</a>
                                    </footer>
                                </div>
                        </section>
            """
        return html
        
if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]