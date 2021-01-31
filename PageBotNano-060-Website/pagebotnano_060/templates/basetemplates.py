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
from pagebotnano_060.toolbox.markdown import parseMarkdown
from pagebotnano_060.toolbox.color import color

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
        self.jsOut = []

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
        if path.split('/')[-1].startswith('.'):
            return
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
        """Build the fonts css, based on what which parameters are
        defined in siteData.

        siteData.fonts = ('Bold', 'Bold_Italic', ...)
        """
        css = ''
        logoFontFamily = self._indexed('logoFontFamily', index) # Add index to anchor name if index > 0
        if hasattr(siteData, logoFontFamily):
            css += """
@font-face {
    font-family: '%(ff)s';
    src: url('../fonts/%(ff)s-Regular.eot') format('embedded-opentype'),
         url('../fonts/%(ff)s-Regular.woff2') format('woff2'),
         url('../fonts/%(ff)s-Regular.woff') format('woff'),
         url('../fonts/%(ff)s-Regular.ttf') format('truetype');
    font-weight: normal;
    font-style: normal
 }""" % dict(ff=getattr(siteData, logoFontFamily))

        # Build the @font-face for every font that is used in the side,
        # as defined by the siteData.fonts list.
        if hasattr(siteData, 'fontFamily') and hasattr(siteData, 'fonts'):
            for weightName in siteData.fonts:
                css += """
@font-face {
    font-family: '%(ff)s-%(wn)s';
    src: url('../fonts/%(ff)s-%(wn)s.eot?v=4.6.3');
    src: url('../fonts/%(ff)s-%(wn)s.eot?#iefix&v=4.6.3') format('embedded-opentype'),
         url('../fonts/%(ff)s-%(wn)s.woff2?v=4.6.3') format('woff2'),
         url('../fonts/%(ff)s-%(wn)s.woff?v=4.6.3') format('woff');
    font-weight: normal;
    font-style: normal;
}           """ % dict(ff=siteData.fontFamily, wn=weightName)
        return css


    def _slideShow(self, siteData, pageData, index):
        """Generate the HTML and JS for the slide show. 
        See options at: https://www.bbslider.com/options.php

        p = pageData
        p.slideShowAutoHeight = True # Automatically sets the height to the largest panel.
        p.slideShowDynamicHeight = False # Recalculates height based on current panel
        p.slideShowStart = 1 # Index of the panel to start on
        p.slideShowDuration = 1000 # Duration of transition animation.
        p.slideShowEasing = 'ease' # Easing of transition animation.
        p.slideShowControls = False # Creates prev/next controls.
        p.slideShowControlsText = '<a...' # HTML element output for controls
        p.slideShowPager = False # Creates pagination.
        p.slideShowPagerWeap = ".pager-wrap" # The element to append the pager to.
        p.slideShowPagerText = "..." # Function to return a single item of the pager
        p.slideShowMaskImage = "images/mask.png" # The mask image for the mask transition."
        p.slideShowMaskSteps = 23 # The number of steps in your mask image.
        p.slideShowAuto = True # Panels play automatically.
        p.slideShowTimer = 5000 # Timer between slides for auto play.
        p.slideShowLoop = True # Loops to beginning and end when controls are hit.
        p.slideShowLoopTrans = True # Use the forward animation when looping back to beginning.
        p.slideShowTransition = 'fade' # none, fade, slide, slideVert, blind, mask = Transition effects between slides.
        p.slideShowPauseOnHit = True # Pause autoplay when someone uses controls or pager
        p.slideShowRandomPlay = False # Slides are random on auto play
        p.slideShowTouch = False # Use touch controls for phones and tablets
        p.slideShowTouchoffset = 50 # Amount of pixels to touch drag before moving to new slide
        p.slideShowDragControls = False # Use mouse click-and-drag left / right controls
        p.slideShowDragoffset = 50 # Amount of pixels to mouse drag before moving to new slide
        p.slideShowCarousel = 2 # Number of slides to show simultaneously
        p.slideShowcarouselMove = 1 # Number of slides to move for next / previous functions
        p.slideShowCallbackStart = '...' # Function to call when slider initializes
        p.slideShowCallbackBefore = '...' # Function to call before every slide
        p.slideShowCallbackAfter = '...' # Function to call after every slide
        p.slideShowCallbackUpdate = '...' # Function to call whenever the update method is called
        """
        html = ''
        slideShowTitle = self._indexed('slideShowTitle', index) # Calculate the indexed attribute name
        slideShowImages = self._indexed('slideShowImages', index) # Add index to anchor name if index > 0
        slideShowHeight = self._indexed('slideShowHeight', index)
        cssClass = self._indexed('slideshow', index)
        captions = []
        if hasattr(pageData, slideShowImages):
            assert isinstance(pageData.slideShowImages, (list, tuple))
            html += """\n<section id="slideShowSection_%d" class="wrapper style2">""" % index
            html += """\n<div class="slideshowgroup clearfix" id="slideShowGroup_%d">""" % index
            if hasattr(pageData, slideShowTitle):
                html += """\n\t<div class="inner">""" 
                html += """\n<h2 class="slideshowtitle">%s</h2>""" % getattr(pageData, slideShowTitle)
                html += """\n\t</div>"""
            html += """\n\t<div class="%s clearfix" id="slideShow_%d">""" % (cssClass, index)
            images = getattr(pageData, slideShowImages)
            for imageIndex, imageData in enumerate(images):
                imagePosition = None
                if isinstance(imageData, str):
                    imageUrl = imageData
                elif isinstance(imageData, (tuple, list)) and len(imageData) == 2:
                    imageUrl, imagePosition = imageData
                elif isinstance(imageData, (tuple, list)) and len(imageData) == 3:
                    imageUrl, imagePosition, caption = imageData
                    parsedCaption = parseMarkdown(caption)
                    captions.append((imageIndex, parsedCaption))
                else:
                    raise ValueError('SlideShow-imageData has wrong format: %s' % imageData)

                if not imagePosition:
                   imagePosition = 'center center'
 
                if hasattr(pageData, slideShowHeight):
                    height = getattr(pageData, slideShowHeight)
                    heightSrc = 'height:%dpt;' % height
                else: 
                    height = 300 # In case using autoHeight
                    heightSrc = ''
                html += """\n\t\t<div style="background-image:url('%s');
                    width:100%%;
                    %sbackground-position:%s;
                    background-size:cover;"></div>""" % (imageUrl, heightSrc, imagePosition)
            #html += """\n\t</div>\n</div>"""
            html += """\n\t\t</div>"""

            captionFontSize = self._indexedValue(pageData, 'slideShowCaptionFontSize', index, 36)
            captionPaddingTop = self._indexedValue(pageData, 'slideShowCaptionPaddingTop', index, captionFontSize/3)
            captionPaddingRight = self._indexedValue(pageData, 'slideShowCaptionPaddingRight', index, captionFontSize/2)
            captionPaddingBottom = self._indexedValue(pageData, 'slideShowCaptionPaddingBottom', index, captionFontSize/3)
            captionPaddingLeft = self._indexedValue(pageData, 'slideShowCaptionPaddingLeft', index, captionFontSize/2)
            captionMarginLeft = self._indexedValue(pageData, 'slideShowCaptionMarginLeft', index, 40)
            captionMarginRight = self._indexedValue(pageData, 'slideShowCaptionMarginRight', index, 40)
            captionMarginBottom = self._indexedValue(pageData, 'slideShowCaptionMarginBottom', index, 50)
            captionBackgroundColor = self._indexedValue(pageData, 'slideShowCaptionBackgroundColor', index, color(1, a=0.8))
            captionColor = self._indexedValue(pageData, 'slideShowCaptionColor', index, siteData.theme.black)
            captionFont = self._indexedValue(pageData, 'slideShowCaptionFont', index, 'Upgrade-Light_Italic')

            for imageIndex, parsedCaption in captions:
                html += """<div id="slideShowCaption_%(index)d_%(imageIndex)d" 
                    style="position: absolute; bottom:%(y)dpx; visibility: hidden;
                    width:auto; 
                    padding-top: %(paddingTop)spx;
                    padding-right: %(paddingRight)spx;
                    padding-bottom: %(paddingBottom)spx;
                    padding-left: %(paddingLeft)spx;
                    margin-left: %(marginLeft)spx; 
                    margin-right: %(marginRight)spx;  
                    background-color: %(backgroundColor)s; 
                    color: %(color)s;
                    z-index: 10; font-size: %(fontSize)dpx; line-height: 1.1em; 
                    font-family: %(font)s;">%(parsedCaption)s</div>""" % dict(
                        paddingTop=captionPaddingTop,
                        paddingRight=captionPaddingRight, 
                        paddingBottom=captionPaddingBottom,
                        paddingLeft=captionPaddingLeft,
                        marginLeft=captionMarginLeft, 
                        marginRight=captionMarginRight,
                        backgroundColor=captionBackgroundColor.css,
                        fontSize=captionFontSize,
                        color=captionColor,
                        font=captionFont,
                        index=index, imageIndex=imageIndex, y=captionMarginBottom, parsedCaption=parsedCaption)
            html += """\n\t</div>\n</section>"""

            # Make slideShow starting javascript
            autoHeight = self._indexedValue(pageData, 'slideShowAutoHeight', index, True)
            dynamicHeight = self._indexedValue(pageData, 'slideShowDynamicHeight', index, False)
            startIndex = self._indexedValue(pageData, 'slideShowStartIndex', index, 1)
            easing = self._indexedValue(pageData, 'slideShowEasing', index, 'ease')
            pager = self._indexedValue(pageData, 'slideShowPager', index, False)
            carousel = self._indexedValue(pageData, 'slideShowCarousel', index, 2)
            controls = self._indexedValue(pageData, 'slideShowControls', index, False)
            controlsText = self._indexedValue(pageData, 'slideShowControlsText', index, False)
            touch = self._indexedValue(pageData, 'slideShowTouch', index, True)
            touchOffset = self._indexedValue(pageData, 'slideShowTouchOffset', index)
            dragControls = self._indexedValue(pageData, 'slideShowDragControls', index, True)
            dragOffset = self._indexedValue(pageData, 'slideShowDragOffset', index)
            pauseOnHit = self._indexedValue(pageData, 'slideShowPauseOnHit', index, True)
            randomPlay = self._indexedValue(pageData, 'slideShowRandomPlay', index)
            maskImage = self._indexedValue(pageData, 'slideShowMaskImage', index)
            jsCallbackStart = self._indexedValue(pageData, 'slideShowJsCallbackStart', index)
            jsCallbackBefore = self._indexedValue(pageData, 'slideShowJsCallbackBefore', index)
            jsCallbackAfter = self._indexedValue(pageData, 'slideShowJsCallbackAfter', index)
            jsCallbackUpdate = self._indexedValue(pageData, 'slideShowJsCallbackUpdate', index)
            duration = self._indexedValue(pageData, 'slideShowDuration', index, 0.7)
            auto = self._indexedValue(pageData, 'slideShowAuto', index, True)
            timer = self._indexedValue(pageData, 'slideShowTimer', index, 4)
            loop = self._indexedValue(pageData, 'slideShowLoop', index, True)
            transition = self._indexedValue(pageData, 'slideShowTransition', index, 'slide')

            js = "$('.%s').bbslider({" % cssClass
            options = []
            if autoHeight is None:
                options.append('autoHeight: false')
            else:
                options.append('autoHeight: true, dynamicHeight: %s' % str(bool(dynamicHeight)).lower())
            if startIndex is not None:
                options.append('start: %d' % startIndex)
            if easing is not None:
                options.append("easing: '%s'" % easing)
            if pager:
                options.append("pager: %s" % str(bool(pager)).lower())
            if carousel:
                assert isinstance(carousel, int)
                options.append("carousel: %d" % carousel)
            if controls:
                options.append("controls: %s" % str(bool(controls)).lower())
                if controlsText:
                    options.append("controlsText: %s" % str(controlsText))
            if touch:
                options.append("touch: true, touchoffset: %d" % (touchOffset or 50))
            if dragControls:
                options.append("dragControls: true, dragoffset: %d" % (dragOffset or 50))
            if not pauseOnHit:
                options.append('pauseOnHit: false')
            if randomPlay:
                options.append('randomPlay: true')
            if maskImage:
                options.append('maskImage: "%s"' % (maskImage))
            if jsCallbackStart:
                options.append('callbackStart: %s' % jsCallbackStart)
            if jsCallbackBefore:
                options.append('callbackBefore: %s' % jsCallbackBefore)
            if jsCallbackAfter:
                options.append('callbackAfter: %s' % jsCallbackAfter)
            if jsCallbackUpdate:
                options.append('callbackUpdate: %s' % jsCallbackUpdate)
            options.append("duration: %d" % ((duration or 1) * 1000)) # In seconds
            options.append("auto: %s" % str(bool(auto)).lower())
            options.append("timer: %d" % ((timer or 3) * 1000))
            options.append("loop: %s" % str(bool(loop)).lower())
            options.append("transition: '%s'" % transition)
            js += ', '.join(options) + '});\n\n'
            js += """function %(functioName)s(d){
                var caption;
                var slideShow = $('#slideShow_%(index)d');
                for (var i=0; i < %(length)s; i++){
                    caption = document.getElementById('slideShowCaption_%(index)d_'+(i-1));
                    if (caption){
                        /*
                        caption.innerHTML = 'slideShowCaption_%(index)d_'+i + ' $' + i + ' #' + slideShow.data('pIndex') + ' @' + %(start)d + ' '+ (i == slideShow.data('pIndex') + %(start)d);
                        */
                        if (i == slideShow.data('pIndex') + %(start)d){
                            caption.style.visibility = 'visible';
                        } else {
                            caption.style.visibility = 'hidden';
                        }
                    }
                }
                return 0;}""" % dict(functioName=jsCallbackBefore, index=index, start=carousel, length=len(images))
            self.jsOut.append(js)

        return html



if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]