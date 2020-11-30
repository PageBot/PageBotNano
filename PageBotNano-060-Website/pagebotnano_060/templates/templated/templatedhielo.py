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
#   Hielo by TEMPLATED
#   templated.co @templatedco
#   Released for free under the Creative Commons Attribution 3.0 license (templated.co/license)
#   Modified to be used with PageBotNano
# -----------------------------------------------------------------------------
#
#   Templates are functions with a standard attribute interface, that
#   can be stored in elements to initialize and compose their content.
#
#   The TemplatedHielo class supports the following anchors
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
#   siteData.iconFontFamily = 'FontAwesome'
#   siteData.menuLinks = True # Force call to templates._menuLinks()
#
#   p = siteData.newPage(id='index', title='Home', template='index')
#
#   p.bannerSlideShow = True # Force call to templates._bannerSlideShow()
#   p.bannerImage_# = 'images/image1.jpg'
#   p.bannerTitle_# = 'Title #1'
#   p.bannerSubtitle_# = Subtitle #1'
#   p.imageArticles = True # Triggers the templates._imageArticles() call
#
#   p.articleImage_# = 'images/image1.jpg'
#   p.articleSubhead_# = 'Subhead #1'
#   p.articleHead_# = 'Head #1'
#   p.article_# = """Long markdown text as article #1"""
#   p.articleFooter_# = 'Footer of article #1'
#
#   p.pullQuote = True # Triggers the template method templates._pullQuote()
#   p.pullQuoteImage_# = 'images/image1.jpg'
#   p.pullQuoteSubhead_# = 'Subhead #1'
#   p.pullQuoteHead_# = 'Pullquote head #1' 
#
#   p.gallery = True # Triggers the templates._gallery() method call
#   p.galleryHead = 'Gallery head'
#   p.gallerySubhead = 'Gallery subhead'
#   p.galleryImage_# = 'images/image1.jpg'
#   p.galleryCaption_# = """Markdown of caption #1'
#
import sys
sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano_060.templates.templated.templatedbase import TemplatedBase
from pagebotnano_060.toolbox.markdown import parseMarkdown

class TemplatedHielo(TemplatedBase):
    """    
    The TemplatedHielo reads all templates sources, ending with .css,
    .js and .html, and keeps them as strings that can be altered
    and queried.
    The Templated class is based on the structure of the https://templated.co
    template structure, Modified to be used with PageBotNano.

    >>> wt = TemplatedHielo()
    >>> len(wt.htmlTemplates) > 0
    True
    """
    TEMPLATE_NAME = 'templated-hielo' # This class is optimised for this set of templates.

    def _menuLinks(self, siteData, pageData, index):
        """Answer the html chunk as menu to all pages of the site.
         {{menuLinks}}
        """
        html = """\n<nav id="menu">\n\t<ul class="links">"""
        for pageData in siteData.pages:
            html += """\n\t\t<li><a href="%s.html">%s</a></li>""" % (pageData.id, pageData.title)
        html += """\n\t</ul>\n</nav>"""
        return html

    def _bannerSlideShow(self, siteData, pageData, index):
        """Answer a list of <article> html chunks, as slides in the slide show
        <section class="banner full">
            <article>
                <img src="{{bannerImage_1}}"/>
                <div class="inner">
                    <header>
                        <p>{{bannerSubtitle_1}}</p>
                        <h2>{{bannerTitle_1}}</h2>
                    </header>
                </div>
            </article>
            ...
        </section>

        """
        html = '\n<section class="banner full">'
        for n in range(1, 100): # Practical maximum amount of slides possible:
            bannerImage = self._indexed('bannerImage', index, n)
            bannerTitle = self._indexed('bannerTitle', index, n)
            bannerSubtitle = self._indexed('bannerSubtitle', index, n)
            if (hasattr(pageData, bannerImage) or 
                hasattr(pageData, bannerTitle) or 
                hasattr(pageData, bannerSubtitle)):
                html += """\n\t<article>"""
                if hasattr(pageData, bannerImage):
                    url = getattr(pageData, bannerImage)
                    html += """\n\t\t'<img src="%s"/>""" % url
                html += """\n\t\t<div class="inner">\n\t\t\t<header>"""
                if hasattr(pageData, bannerSubtitle):
                    parsed = parseMarkdown(getattr(pageData, bannerSubtitle))
                    html += """\n\t\t\t\t<p>%s</p>""" % parsed
                if hasattr(pageData, bannerTitle):
                    parsed = parseMarkdown(getattr(pageData, bannerTitle))
                    html += """\n\t\t\t\t<h2>%s</h2>""" % parsed
                html += """\n\t\t\t</header>\n\t\t</div>\n\t</article>\n"""
        html += '\n</section>'
        return html

    def _imagesArticle(self, siteData, pageData, index):
        """Answer the html chunk of imagesArticle "One" (style 2) in index.html template

        <section id="one" class="wrapper style2">
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
        </section>
        """
        html = """\n<section id="one" class="wrapper style2">\n\t<div class="inner">\n\t\t\t<div class="grid-style">"""
        for n in range(1, 21): # Partical maximum amount of images in an imageArticle possible
            articleImage = self._indexed('articleImage', index, n)
            articleHead = self._indexed('articleHead', index, n)
            articleSubhead = self._indexed('articleSubhead', index, n)
            articleText = self._indexed('articleText', index, n) # Double indexed achor name
            articleFooter = self._indexed('articleFooter', index, n)
            if (hasattr(pageData, articleImage) or 
                hasattr(pageData, articleHead) or
                hasattr(pageData, articleSubhead) or
                hasattr(pageData, articleText)):
                html += """\n\t\t\t\t<div>\n\t\t\t\t\t<div class="box">"""
                if hasattr(pageData, articleImage):
                    url = getattr(pageData, articleImage)
                    if isinstance(url, (list, tuple)):
                        if len(url) == 2:
                            url, alignment = url # TODO: add alignment in output
                        elif len(url) == 3:
                            url, alignment, caption = url # TODO: add alignment and caption in output 
                    html += """\n\t\t\t\t\t\t<div class="image fit">\n\t\t\t\t\t\t\t<img src="%s"/>\n\t\t\t\t\t\t</div>""" % url
                html += """\n\t\t\t\t\t\t<div class="content">"""
                if hasattr(pageData, articleHead) or getattr(pageData, articleSubhead):
                    html += """\n\t\t\t\t\t\t\t<header class="align-center">"""
                    if hasattr(pageData, articleSubhead):
                        parsed = parseMarkdown(getattr(pageData, articleSubhead))
                        html += """\n\t\t\t\t\t\t\t\t<p>%s</p>""" % parsed
                    if hasattr(pageData, articleHead):
                        parsed = parseMarkdown(getattr(pageData, articleHead))
                        html += """\n\t\t\t\t\t\t\t\t<h2>%s</h2>""" % parsed
                    html += """\n\t\t\t\t\t\t\t</header>"""
                if hasattr(pageData, articleText):
                    parsed = parseMarkdown(getattr(pageData, articleText))
                    html += """<p>%s</p>""" % parsed
                if hasattr(pageData, articleFooter):
                    parsed = parseMarkdown(getattr(pageData, articleFooter))
                    html += """\n\t\t\t\t\t\t\t<footer class="align-center">%s</footer>""" % parsed
                html += """\n\t\t\t\t\t</div><!-- class=content -->\n\t\t\t\t\t</div><!-- class=box -->\n\t\t\t\t</div>"""
        html += """\n\t</div>\n</section>"""
        return html

    def _gallery(self, siteData, pageData, index):
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
        galleryHead = self._indexed('galleryHead', index)
        gallerySubhead = self._indexed('gallerySubhead', index)
        if (hasattr(pageData, galleryHead) or
            hasattr(pageData, gallerySubhead)):
            html = """\n<section id="three" class="wrapper style2">\n\t<div class="inner">\n\t\t<header class="align-center">"""
            if hasattr(pageData, gallerySubhead):
                parsed = parseMarkdown(getattr(pageData, gallerySubhead))
                html += """\n\t\t\t<p class="special">%s</p>""" % parsed
            if hasattr(pageData, galleryHead):
                parsed = parseMarkdown(getattr(pageData, galleryHead))
                html += """\n\t\t\t<h2>%s</h2>""" % parsed
            html += """\n\t</header>\n\t\t\t<div class="gallery">"""
            for n in range(1, 100): # Partical maximum amount of imageArticles possible
                galleryImage = self._indexed('galleryImage', index, n)
                if hasattr(pageData, galleryImage):
                    html += """\n\t\t\t<div>\n\t\t\t\t<div class="image fit">"""
                    url = getattr(pageData, galleryImage)
                    html += """\n\t\t\t\t\t<a href="#"><img src="%s"/></a>""" % url
                    html += """\n\t\t\t\t</div>"""
                    galleryCaption = 'galleryCaption_%d' % n
                    if hasattr(pageData, galleryCaption):
                        parsed = parseMarkdown(getattr(pageData, galleryCaption))
                        html += """\n\t\t\t\t<div class="caption">%s</div>""" % parsed
                    html += """\n\t\t\t</div>"""

            html += """\n\t\t\t</div>\n\t</div>\n</section>"""
        return html

    def _pullQuote(self, siteData, pageData, index):
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
        pullQuoteImage = self._indexed('pullQuoteImage', index)
        pullQuoteSubhead = self._indexed('pullQuoteSubhead', index)
        pullQuoteHead = self._indexed('pullQuoteHead', index)
        if (hasattr(pageData, pullQuoteImage) or 
            hasattr(pageData, pullQuoteSubhead) or 
            hasattr(pageData, pullQuoteHead)):
            html +=  """\n\t<section class="wrapper style3" """
            if hasattr(pageData, pullQuoteImage):
                url = getattr(pageData, pullQuoteImage)
                html += """ style="background-image: url(%s);" """ % url
            html += '>'
            if hasattr(pageData, pullQuoteSubhead) or hasattr(pageData, pullQuoteHead):
                html += """\n\t\t<div class="inner">\n\t\t<header class="align-center">"""
                if hasattr(pageData, pullQuoteSubhead):
                    parsed = parseMarkdown(getattr(pageData, pullQuoteSubhead))
                    html += """\n\t\t\t<p>%s</p>""" % parsed
                if hasattr(pageData, pullQuoteHead):
                    parsed = parseMarkdown(getattr(pageData, pullQuoteHead))
                    html += """\n\t\t\t<h2>%s</h2>""" % parsed
                html += """\n\t\t</header>\n\t</div>"""
            html += """\n\t</section>"""
        return html

    def _articlePageHeader(self, siteData, pageData, index):
        html = ''
        articlePageHeaderTitle = self._indexed('articlePageHeaderTitle', index)
        articlePageHeaderSubhead = self._indexed('articlePageHeaderSubhead', index)
        if (hasattr(pageData, articlePageHeaderTitle) or 
            hasattr(pageData, articlePageHeaderSubhead)):
            html += """<section id="articlePageHeader%d" class="wrapper style3">\n\t<div class="inner">\n\t\t<header class="align-center">""" % index
            if hasattr(pageData, articlePageHeaderSubhead):
                html += """\n\t\t\t<p>%s</p>""" % getattr(pageData, articlePageHeaderSubhead)
            if hasattr(pageData, articlePageHeaderTitle):
                html += """\n\t\t\t<h2>%s</h2>""" % getattr(pageData, articlePageHeaderSubhead)
            html += """\n\t\t</header>\n\t</div>\n</section>"""
        return html

    def _deck(self, siteData, pageData, index):
        """Add numbered deck with background images
        <section id="two" class="wrapper style3" style="background-image: url({{deckImage 1}});">
            <div class="inner">
                <header class="align-center">
                    <h1>{{deckHead}}</h1>
                </header>
            </div>
        </section>
        """
        html = ''
        deckImage = self._indexed('deckImage', index)
        deckHead = self._indexed('deckHead', index)
        if (hasattr(pageData, deckImage) or 
            hasattr(pageData, deckHead)):
            html +=  """\n\t<section class="wrapper style3 deck" """
            if hasattr(pageData, deckImage):
                url = getattr(pageData, deckImage)
                html += """ style="background-image: url(%s);" """ % url
            html += '>'
            if hasattr(pageData, deckHead):
                html += """\n\t\t<div class="inner">\n\t\t<header class="align-center">"""
                if hasattr(pageData, deckHead):
                    parsed = parseMarkdown(getattr(pageData, deckHead))
                    html += """\n\t\t\t<h1>%s</h1>""" % parsed
                html += """\n\t\t</header>\n\t</div>"""
            html += """\n\t</section>"""
        return html

    def _articlePageHeader(self, siteData, pageData, index):
        html = ''
        articlePageHeaderTitle = self._indexed('articlePageHeaderTitle', index)
        articlePageHeaderSubhead = self._indexed('articlePageHeaderSubhead', index)
        if (hasattr(pageData, articlePageHeaderTitle) or 
            hasattr(pageData, articlePageHeaderSubhead)):
            html += """<section id="articlePageHeader%d" class="wrapper style3">\n\t<div class="inner">\n\t\t<header class="align-center">""" % index
            if hasattr(pageData, articlePageHeaderSubhead):
                html += """\n\t\t\t<p>%s</p>""" % getattr(pageData, articlePageHeaderSubhead)
            if hasattr(pageData, articlePageHeaderTitle):
                html += """\n\t\t\t<h2>%s</h2>""" % getattr(pageData, articlePageHeaderSubhead)
            html += """\n\t\t</header>\n\t</div>\n</section>"""
        return html

    def _article(self, siteData, pageData, index):
        html = ''
        articleSubhead = self._indexed('articleSubhead', index) # Add index to anchor name if index > 0
        articleHead = self._indexed('articleHead', index)
        articleText = self._indexed('articleText', index)
        if (hasattr(pageData, articleSubhead) or 
            hasattr(pageData, articleHead) or
            hasattr(pageData, articleText)):
            html += """<section id="article%d" class="wrapper style2">\n\t<div class="inner">\n\t\t<div class="box">\n\t\t\t<div class="content">""" % index
            if (hasattr(pageData, articleSubhead) or 
                hasattr(pageData, articleHead)):
                html += """\n\t\t\t\t<header class="align-center">"""
                if hasattr(pageData, articleSubhead):
                    html += """\n\t\t\t\t\t<p>%s</p>""" % getattr(pageData, articleSubhead)
                if hasattr(pageData, articleHead):
                    parsed = parseMarkdown(getattr(pageData, articleHead))
                    html += """\n\t\t\t\t\t<h2>%s</h2>""" % parsed
                html += """\n\t\t\t\t</header>"""
            if hasattr(pageData, articleText):
                parsed = parseMarkdown(getattr(pageData, articleText))
                html += """\n\t\t\t\t<p>%s</p>""" % parsed
            html += """\n\t\t\t</div>\n\t\t</div>\n\t</div>\n</section>"""
        return html

 
if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]