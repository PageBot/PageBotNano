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
import sys
sys.path.insert(0, "../../..") # So we can import pagebotnano without installing.

from pagebotnano.contexts.basecontext import BaseContext
from pagebotnano.constants import *
    
class InDesignContext(BaseContext):

    # Used by the generic BaseContext.newString( )
    #EXPORT_TYPES = (FILETYPE_IDML,)

    def __init__(self):
        """Constructor of InDesignContext.

        >>> from pagebotnano.document import Document
        >>> from pagebotnano.toolbox.color import color
        >>> from pagebotnano.contexts.indesigncontext.context import InDesignContext
        >>> context = InDesignContext()

        """

        """
        >>> font = 'Georgia' # Is available in Adobe 
        >>> styles = {}
        >>> styles['h0'] = dict(name='h0', font=font, fontSize=pt(48), leading=em(0.9), textFill=color(1, 0, 0))
        >>> styles['h1'] = dict(name='h1', font=font, fontSize=pt(24), leading=em(0.9), textFill=color(1, 0, 0))
        >>> doc = Document(w=510, h=720, context=context, autoPages=8, padding=p(4), originTop=False)
        >>> doc.styles = styles # Overwrite all default styles.
        >>> page = doc[2]
        >>> scaleType = None #SCALE_TYPE_FITWH # for non-proportional
        >>> e = Image('resources/images/cookbot10.jpg', parent=page, x=page.pl, y=page.pt, w=page.pw, h=page.pw, scaleImage=False, fill=color(0.5), scaleType=scaleType)
        >>> page = doc[3]
        >>> e = Image('resources/images/cookbot10.jpg', parent=page, x=page.pl, y=page.pt, w=page.pw, h=page.pw, scaleImage=False, fill=color(0.2), scaleType=scaleType)
        >>> e = newRect(parent=page, w=p(16), h=p(16), x=p(20), y=p(41), stroke=color(1, 0, 0), strokeWidth=p(2), fill=color(c=1, m=0.5, y=0, k=0, a=0.8))
        >>> e = newRect(parent=page, w=p(16), h=p(16), x=page.pl, y=page.pt, fill=color(1, 0, 0))
        >>> e = newRect(parent=page, w=p(16), h=p(16), x=page.pl+p(2), y=p(50), fill=color(c=0.5, m=1, y=0, k=0, a=0.5))
        >>> e = newOval(parent=page, w=p(16), h=p(16), x=p(24), y=p(42), fill=color(c=0.5, m=0, y=1, k=0, a=0.5))
        >>> e = newTextBox('ABCD EFGH IJKL MNOP', style=doc.styles['h1'], parent=page, w=p(16), h=p(8), x=p(34), y=p(22), padding=p(1), fill=color(c=0, m=0.5, y=1, k=0, a=0.5))
        >>> page = page.next        
        >>> e = Image('resources/images/cookbot10.jpg', parent=page, x=page.pl, y=page.pt, w=page.pw, h=page.pw, scaleImage=False, fill=color(0.5), scaleType=scaleType)
        >>> e = newOval(parent=page, w=p(16), h=p(16), x=p(24), y=p(22), fill=color(c=0.5, m=0, y=1, k=0, a=0.5))
        >>> e = newTextBox('@XYZ', style=doc.styles['h0'], parent=page, w=p(26), h=p(8), x=p(14), y=p(22), padding=p(1), fill=color(c=0, m=0.5, y=1, k=0, a=0.5))
        >>> page = page.next
        >>> e = Image('resources/images/cookbot10.jpg', parent=page, x=page.pl, y=page.pt, w=page.pw, h=page.pw, scaleImage=False, fill=color(0, 0, 1), scaleType=scaleType)
        >>> e = newRect(parent=page, w=p(16), h=p(16), x=p(24), y=p(22), fill=color(c=0.5, m=1, y=1, k=0, a=0.5))
        >>> e = newTextBox('@EEE', style=doc.styles['h0'], parent=page, w=p(26), h=p(8), x=p(14), y=p(22), padding=p(1), fill=color(c=0, m=0.5, y=1, k=0, a=0.5))
        >>> page = page.next
        >>> e = Image('resources/images/cookbot10.jpg', parent=page, x=page.pl, y=page.pt, w=page.pw, h=page.pw, scaleImage=False, fill=color(1, 0, 0), scaleType=scaleType)
        >>> e = newRect(parent=page, w=p(16), h=p(16), x=p(24), y=p(22), fill=color(c=0.5, m=1, y=1, k=0, a=0.5))
        >>> e = newTextBox('@EEE', style=doc.styles['h0'], parent=page, w=p(26), h=p(8), x=p(14), y=p(22), padding=p(1), fill=color(c=0, m=0.5, y=1, k=0, a=0.5))
        >>> doc.export('Image.js')

        """
        super().__init__()
        self.b = InDesignBuilder() # cls.b builder for this context.
        self.name = self.__class__.__name__
      
    def newDocument(self, w=None, h=None, doc=None):
        self.b.newDocument(w, h, doc)

    def newDrawing(self):
        pass

    def newPage(self, w=None, h=None, e=None):
        """Have the builder create a new page in the document."""
        self.b.newPage(w, h, e)

    def frameDuration(self, frameDuration, e=None):
        """Ignore for now in this context."""
        pass

    # Basic shapes.

    def rect(self, x, y, w=None, h=None, e=None):
        """New rectangle by the builder"""
        self.b.rect(x, y, w=w, h=h, e=e)

    def oval(self, x, y, w=None, h=None, e=None):
        """Ignore for now in this context."""
        self.b.oval(x, y, w=w, h=h, e=e)

    def textBox(self, sOrBs, p, w=None, h=None, clipPath=None, e=None):
        self.b.textBox(sOrBs, p, w=w, h=h, clipPath=clipPath, e=e)

    def scaleImage(self, path, w, h, index=0, showImageLoresMarker=False, exportExtension=None):
        pass

    def image(self, path, p, alpha=1, pageNumber=None, w=None, h=None, scaleType=None, e=None):
        self.b.image(path, p, alpha=alpha, pageNumber=pageNumber, w=w, h=h, scaleType=scaleType, e=e)

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

    def imageSize(self, path):
        """Answers the (w, h) image size of the image file at path. If the path is an SVG
        image, then determine by parsing the SVG-XML.

        if path.lower().endswith('.'+FILETYPE_SVG):
            import xml.etree.ElementTree as ET
            svgTree = ET.parse(path)
            print(svgTree)
            return pt(1000, 1000)

        return pt(self.b.imageSize(path))
        """
        return pt(1000, 1000)

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
