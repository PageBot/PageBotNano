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
#   context.py
#
#   InDesign JavaScript file specifications here:
#   https://www.adobe.com/content/dam/acom/en/devnet/indesign/sdk/cs6/scripting/InDesign_ScriptingGuide_JS.pdf
#
import os
import sys
sys.path.insert(0, "../../..") # So we can import pagebotnano without installing.

from pagebotnano_050.contexts.basecontext import BaseContext
from pagebotnano_050.contexts.indesign.builder import InDesignBuilder
from pagebotnano_050.constants import *
from pagebotnano_050.toolbox.color import Color
    
class InDesignContext(BaseContext):

    # Used by the generic BaseContext.newString( )
    #EXPORT_TYPES = (FILETYPE_IDML,)

    def __init__(self):
        """Constructor of InDesignContext.

        >>> from pagebotnano_050.document import Document
        >>> from pagebotnano_050.elements.element import Image, Rect, Text
        >>> from pagebotnano_050.toolbox.color import color
        >>> from pagebotnano_050.toolbox import p
        >>> context = InDesignContext()
        >>> font = 'Georgia' # Is available in Adobe 
        >>> styles = {}
        >>> styles['h0'] = dict(name='h0', font=font, fontSize=48, leading=44, textFill=color(1, 0, 0))
        >>> styles['h1'] = dict(name='h1', font=font, fontSize=24, leading=22, textFill=color(1, 0, 0))
        >>> doc = Document(w=510, h=720, context=context)

        """
        """
        >>> doc.styles = styles # Overwrite all default styles.
        >>> pad = p(4) # 4 pica padding on all sides.
        >>> page = doc.newPage()
        >>> scaleType = None #SCALE_TYPE_FITWH # for non-proportional
        >>> e = Image('../../resources/images/cookbot10.jpg', parent=page, x=page.pl, y=page.pt, w=page.pw, h=page.pw, fill=color(0.5))
        >>> page = doc.newPage()
        >>> e = Image('../resources/images/cookbot10.jpg', parent=page, x=page.pl, y=page.pt, w=page.pw, h=page.pw, fill=color(0.2))
        >>> e = Rect(parent=page, w=p(16), h=p(16), x=p(20), y=p(41), stroke=color(1, 0, 0), strokeWidth=p(2), fill=color(c=1, m=0.5, y=0, k=0, a=0.8))
        >>> e = Rect(parent=page, w=p(16), h=p(16), x=page.pl, y=page.pt, fill=color(1, 0, 0))
        >>> e = Rect(parent=page, w=p(16), h=p(16), x=page.pl+p(2), y=p(50), fill=color(c=0.5, m=1, y=0, k=0, a=0.5))
        >>> e = Oval(parent=page, w=p(16), h=p(16), x=p(24), y=p(42), fill=color(c=0.5, m=0, y=1, k=0, a=0.5))
        >>> bs = BabelString('ABCD EFGH IJKL MNOP', style=doc.styles['h1'])
        >>> e = Text(bs, parent=page, w=p(16), h=p(8), x=p(34), y=p(22), padding=p(1), fill=color(c=0, m=0.5, y=1, k=0, a=0.5))
        >>> page = page.newPage()       
        >>> e = Image('../resources/images/cookbot10.jpg', parent=page, x=page.pl, y=page.pt, w=page.pw, h=page.pw, fill=color(0.5))
        >>> bs = BabelString('@XYZ', style=doc.styles['h0'])
        >>> e = Text(bs, parent=page, w=p(26), h=p(8), x=p(14), y=p(22), padding=p(1), fill=color(c=0, m=0.5, y=1, k=0, a=0.5))
        >>> page = page.newPage()
        >>> e = Image('../resources/images/cookbot10.jpg', parent=page, x=page.pl, y=page.pt, w=page.pw, h=page.pw, fill=color(0, 0, 1))
        >>> e = Rect(parent=page, w=p(16), h=p(16), x=p(24), y=p(22), fill=color(c=0.5, m=1, y=1, k=0, a=0.5))
        >>> bs = BabelString('@EEE', style=doc.styles['h0'])
        >>> e = Text(bs, parent=page, w=p(26), h=p(8), x=p(14), y=p(22), padding=p(1), fill=color(c=0, m=0.5, y=1, k=0, a=0.5))
        >>> page = page.newPage()
        >>> e = Image('../resources/images/cookbot10.jpg', parent=page, x=page.pl, y=page.pt, w=page.pw, h=page.pw, fill=color(1, 0, 0))
        >>> e = Rect(parent=page, w=p(16), h=p(16), x=p(24), y=p(22), fill=color(c=0.5, m=1, y=1, k=0, a=0.5))
        >>> bs = BabelString('@EEE', style=doc.styles['h0'])
        >>> e = TextBox(bs, parent=page, w=p(26), h=p(8), x=p(14), y=p(22), padding=p(1), fill=color(c=0, m=0.5, y=1, k=0, a=0.5))
        >>> doc.export('export/Image_init.js')

        """
        super().__init__()
        self.b = InDesignBuilder() # cls.b builder for this context.
        self.name = self.__class__.__name__
        self._stroke = None
        self._strokeWidth = 1
        self._fill = None
        self.sx = self.sy = 1 # Drawing scale

    def newDocument(self, w=None, h=None):
        self.b.newDocument(w, h)

    def newDrawing(self):
        pass

    def newPage(self, w=None, h=None):
        """Have the builder create a new page in the document."""
        self.b.newPage(w, h)

    def frameDuration(self, frameDuration, e=None):
        """Ignore for now in this context."""
        pass

    # Drawing values

    def fill(self, c):
        """Set the fill mode of the context. `c` can be None, a number,
        a name or a Color instance. 

        >>> context = InDesignContext()
        >>> context
        <InDesignContext>
        >>> context.fill(None)
        >>> context.fill('red')
        >>> context.fill((1, 0, 0))
        >>> context.fill(Color(1, 0, 0))
        >>> context.fill(0.5)
        """
        self.b.fill(c)
        
    def stroke(self, c, strokeWidth=None):
        """Set the stroke mode of the context. `c` can be None, a number,
        a name or a Color instance. 

        >>> context = InDesignContext()
        >>> context
        <InDesignContext>
        >>> context.stroke(None)
        >>> context.stroke('red')
        >>> context.stroke((1, 0, 0))
        >>> context.stroke(Color(1, 0, 0))
        >>> context.stroke(0.5, 1)
        """
        if strokeWidth is not None:
            self.b.strokeWidth(strokeWidth)
        self.b.stroke(c)
        
    def strokeWidth(self, strokeWidth):
        """Set the current stroke witdh.

        >>> context = InDesignContext()
        >>> context.strokeWidth(None)
        >>> context.strokeWidth(10)
        """
        self.b.strokeWidth(strokeWidth)

    # Basic shapes.

    def rect(self, x, y, w=None, h=None):
        """Draw new rectangle by the builder

        >>> context = InDesignContext()
        >>> context.newPage(500, 500)
        >>> context.rect(100, 200)
        >>> context.rect(100, 200, 300, 400)
        """
        self.b.rect(x, y, w=w or DEFAULT_WIDTH, h=DEFAULT_HEIGHT)

    def oval(self, x, y, w=None, h=None):
        """Draw new oval by the builde that fits in this bounding box

        >>> context = InDesignContext()
        >>> context.newPage(500, 500)
        >>> context.oval(100, 200)
        >>> context.oval(100, 200, 300, 400)
        """
        self.b.oval(x, y, w=w or DEFAULT_WIDTH, h=h or DEFAULT_HEIGHT)

    def textBox(self, sOrBs, p, w=None, h=None, clipPath=None):
        self.b.textBox(sOrBs, p, w=w, h=h, clipPath=clipPath)

    def scaleImage(self, path, w, h, index=0, showImageLoresMarker=False, exportExtension=None):
        pass

    def image(self, path, p, alpha=1, pageNumber=None, w=None, h=None, scaleType=None):
        """Draw the image

        >>> context = InDesignContext()
        >>> context.image('../../../../resources/images/cookbot10.jpg', (100, 200))
        """
        self.b.image(path, p, alpha=alpha, pageNumber=pageNumber, w=w, h=h, scaleType=scaleType)

    def newString(self, s, e=None, style=None, w=None, h=None, pixelFit=True):
        """Creates a new styles BabelString instance of self.STRING_CLASS from
        `s` (converted to plain unicode string), using e or style as
        typographic parameters. Ignore and just answer `s` if it is already a
        self.STRING_CLASS instance and no style is forced. PageBot function.
        """
        return self.STRING_CLASS(s, context=self, style=style)

    def text(self, sOrBs, p):
        """Ignore for now in this context."""
        pass

    def scale(self, sx, sy=None):
        """Set the scale of drawing."""
        self.sx = sx
        self.sy = sy or sx

    def imageSize(self, path):
        """Answers the (w, h) image size of the image file at path. If the path is an SVG
        image, then determine by parsing the SVG-XML.

        >>> context = InDesignContext()
        >>> context.imageSize('../../../../resources/images/cookbot10.jpg')
        (2058, 946)
        >>> context.imageSize('../../../../resources/images/Berthold-Grid.pdf')
        (590, 842)
        >>> context.imageSize('../../../NOTEXIST.pdf') is None
        True
        """
        return self.b.imageSize(path)

    def saveDocument(self, path, multiPage=True):
        self.b.saveDocument(path)

    saveImage = saveDocument

    def getFlattenedPath(self, path=None):
        pass

    def getFlattenedContours(self, path=None):
        pass

    def getGlyphPath(self, glyph, p=None, path=None):
        pass

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
