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
#   indesign/builder.py
#
import codecs
import os, shutil
import zipfile

import sys
sys.path.insert(0, "../../..") # So we can import pagebotnano without installing.

from pagebotnano_050.contexts.indesign.constants import JSX_LIB
from pagebotnano_050.toolbox.color import color, noColor
from pagebotnano_050.constants import *

class InDesignBuilder:
    """The InDesignBuilder is the interface between the InDesignContext and the 
    generated JavaScript files. It is on the same level as DrawBot builder/canvas.
    Similar to DrawBot, builders are not supposed to know anything about PageBotNano objects.

    >>> from pagebotnano_050.constants import A4
    >>> w, h = A4
    >>> b = InDesignBuilder()
    >>> b
    <InDesignBuilder>
    >>> b.newDocument(w=w, h=h)
    >>> b.docW, b.docH
    (595, 842)
    >>> b.newPage()
    >>> b.fill(color(1, 0, 0))
    >>> b.rect(100, 100, 200, 300)
    >>> b.newPage()
    >>> b.newPage()
    >>> b.saveDocument('InDesignBuilder.js')

    """
    PB_ID = 'inds'

    # Exporting directly into the InDesign 
    SCRIPT_PATH = '/Users/petr/Library/Preferences/Adobe InDesign/Version 14.0/en_US/Scripts/Scripts Panel/PageBot/'
    SCRIPT_PATH1 = '_export/'

    def __init__(self):
        self._fillColor = noColor
        self._strokeColor = noColor
        self._strokeWidth = 1
        self.pageIndex = None
        self.unit = 'pt'
        self.docW = self.docH = None # Defined by self.newDocument()

        self.jsOut = []

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

    def getXY(self, x, y, w, h):
        """Calculate positions, answer as rectangle of bounding box
        (topY, rightX, bottomY, leftX) to be used in origin-top setting of InDesign canvas.
        """
        return y+h, x+w, y, x  

    def _out(self, s):
        self.jsOut.append(s)

    def getOut(self):
        return '\n'.join(self.jsOut)

    def newDocument(self, w=None, h=None, numPages=1):

        self.docW = w or DEFAULT_WIDTH
        self.docH = h or DEFAULT_HEIGHT
        self._out('/* Document */')
        self._out(JSX_LIB)
        self._out('var pbDoc = app.documents.add();')
        self._out('pbDoc.documentPreferences.pagesPerDocument = %d;' % numPages)

        self._out('pbDoc.documentPreferences.pageWidth = "%s%s";' % (self.docW, self.unit))
        self._out('pbDoc.documentPreferences.pageHeight = "%s%s";' % (self.docH, self.unit))
        if w > h:
            self._out('pbDoc.documentPreferences.pageOrientation = PageOrientation.landscape;')
        else:
            self._out('pbDoc.documentPreferences.pageOrientation = PageOrientation.portrait;')

        self._out('pbDoc.documentPreferences.facingPages = false;')
        self._out('var pbPage;')
        self._out('var pbPageIndex;') # Index of the current page.
        self._out('var pbElement;') # Current parent element.

    def outStyles(self, styles):    
        """If there are @doc styles defined, then export them as paragraph styles JS such as
        pbDoc.paragraphStyles.add({name:"Title", appliedFont:"Upgrade", fontStyle:'Bold', 
            justification:Justification.CENTER_ALIGN,
            pointSize:300, leading:300, fillColor: pbGetColor(pbDoc, [255, 255, 255])});

        >>> from pagebotnano_050.toolbox.color import color
        >>> from pagebotnano_050.document import Document
        >>> from pagebotnano_050.contexts.indesign.context import InDesignContext
        >>> context = InDesignContext()
        >>> font = 'Geordgia'
        >>> styles = dict(h1=dict(font=font, fontSize=12, leading=14, textFillColor=color(1, 0, 0)))
        >>> styles = styles # Overwrite all default styles.
        >>> #context.b.outStyles(styles)
        >>> #context.b.getOut()
        """
        self._out('/* Paragraph styles */')
        for name, style in styles.items():
            self._out('pbDoc.paragraphStyles.add({name:"%s",' % name)
            if 'font' in style:
                font = style['font']
                if not isinstance(font, str): # For now, only with real Font objects.
                    self._out('\tappliedFont:"%s",' % font.info.familyName)
                    self._out('\tfontStyle:"%s",' % font.info.styleName)
            if 'fontSize' in style:
                fontSize = style['fontSize']
                self._out('\tpointSize:"%s",' % style['fontSize'])
            if 'leading' in style:
                leading = style.get('leading', fontSize*DEFAULT_LEADING)
                self._out('\tleading:"%s",' % leading)
            if 'textFill' in style:
                fillColor = style['textFill']
                if fillColor.isCmyk:
                    c, m, y, k = fillColor.cmyk
                    self._out('\tfillColor: pbGetColor(pbDoc, [%s, %s, %s, %s]),' % (c*100, m*100, y*100, k**100))
                else: # Round other colors to rgb output.
                    r, g, b = fillColor.rgb
                    self._out('\tfillColor: pbGetColor(pbDoc, [%s, %s, %s]),' % (r*255, g*255, b*255))
            if 'textStroke' in style:
                strokeColor = style['textStroke']
                if fillColor.isCmyk:
                    c, m, y, k = strokeColor.cmyk
                    self._out('\tstrokeColor: pbGetColor(pbDoc, [%s, %s, %s, %s]),' % (c*100, m*100, y*100, k**100))
                else: # Round other colors to rgb output.
                    r, g, b = strokeColor.rgb
                    self._out('\tstrokeColor: pbGetColor(pbDoc, [%s, %s, %s]),' % (r*255, g*255, b*255))
            self._out('});')

    def _outSelectPage(self):
        """Output code to select the e.page if it is not selected already."""
        self._out('pbPageIndex = %d' % self.pageIndex)
        self._out('pbPage = pbDoc.pages.item(pbPageIndex);')

    def newPage(self, w=None, h=None, padding=None):
        if self.pageIndex is None:
            self.pageIndex = 0
        else:
            self.pageIndex += 1
        self._out('/* Page %d */' % self.pageIndex)
        self._out('pbPageIndex = %d;' % self.pageIndex)
        self._out('pbPage = pbDoc.pages.add();')
        self._out('pbPage.resize(CoordinateSpaces.INNER_COORDINATES,')
        self._out('    AnchorPoint.CENTER_ANCHOR,')
        self._out('    ResizeMethods.REPLACING_CURRENT_DIMENSIONS_WITH,')
        self._out('    [%d, %d]);' % (w or self.docW, h or self.docH))

        pt, pr, pb, pl = padding or (30, 30, 30, 40) # Padding is called margin in InDesign script.
        self._out('pbPage.marginPreferences.top = "%s%s";' % (pt, self.unit))
        self._out('pbPage.marginPreferences.right = "%s%s";' % (pr, self.unit))
        self._out('pbPage.marginPreferences.bottom = "%s%s";' % (pb, self.unit))
        self._out('pbPage.marginPreferences.left = "%s%s";' % (pl, self.unit))
 
    def rect(self, x, y, w=None, h=None):
        w = w or DEFAULT_WIDTH
        h = h or DEFAULT_HEIGHT
        px1, py1, px2, py2 = self.getXY(x, y, w, h) # Calculate positions.
        self._out('/* Rect */')
        self._out('pbElement = pbPage.rectangles.add({geometricBounds:["%s%s", "%s%s", "%s%s", "%s%s"]});' % (py1, self.unit, px1, self.unit, py2, self.unit, px2, self.unit))
        self._outElementFillColor()
        self._outElementStrokeColor()

    def oval(self, x, y, w=None, h=None, e=None):
        w, h = self.getWH(w, h, e)
        px1, py1, px2, py2 = self.getXY(x, y, w, h) # Calculate positions.
        self._out('/* Oval */')
        self._outSelectPage(e)
        self._out('pbElement = pbPage.ovals.add({geometricBounds:["%s%s", "%s%s", "%s%s", "%s%s"]});' % (py1, self.unit, px1, self.unit, py2, self.unit, px2, self.unit))
        self._outElementFillColor(e)
        self._outElementStrokeColor(e)

    def fill(self, c):
        self._fillColor = c

    def stroke(self, c, w=None):
        self._strokeColor = c
        self.strokeWidth(w)

    def strokeWidth(self, w):
        if w is not None:
            self._strokeWidth = w
            
    def _outElementFillColor(self):
        """Set the fill color of pbElement to the current self._fillColor."""
        jsColor = None
        fillColor = self._fillColor
        if fillColor not in (None, noColor):
            if fillColor.isCmyk:
                c, m, y, k = fillColor.cmyk
                jsColor = [c*100, m*100, y*100, k*100]
            else: # All other color types default to fillColor.rgb:
                r, g, b = fillColor.rgb
                jsColor = [r*255, g*255, b*255]
        if jsColor is not None:
            self._out('pbElement.fillColor = pbGetColor(pbDoc, %s);' % (jsColor,))
        if fillColor is not None and fillColor.a < 1:
            self._out('pbElement.fillTransparencySettings.blendingSettings.opacity = %s' % (fillColor.a * 100))
        return None
            
    def _outElementStrokeColor(self):
        """Set the fill color of pbElement to the current self._strokeColor."""
        jsColor = None
        strokeColor = self._strokeColor
        strokeWidth = self._strokeWidth
        if strokeColor not in (None, noColor):
            if strokeColor.isCmyk:
                c, m, y, k = strokeColor.cmyk
                jsColor = [c*100, m*100, y*100, k*100]
            else: # All other color types default to strokeColor.rgb:
                r, g, b = strokeColor.rgb
                jsColor = [r*255, g*255, b*255]
        if jsColor is not None:
            self._out('pbElement.strokeColor = pbGetColor(pbDoc, %s);' % (jsColor,))
            self._out('pbElement.strokeWeight = "%s"' % strokeWidth)
        if strokeColor is not None and strokeColor.a < 1:
            self._out('pbElement.strokeTransparencySettings.blendingSettings.opacity = %s' % (strokeColor.a * 100))
        return None

    def image(self, path, p, alpha=None, pageNumber=1, w=None, h=None, scaleType=None):
        x, y = p
        px1, py1, px2, py2 = self.getXY(x, y, w, h) # Calculate positions.
        self._out('/* Image %s */' % path)
        self._outSelectPage(e)
        self._out('pbElement = pbPage.rectangles.add({geometricBounds:["%s", "%s", "%s", "%s"]});' % (py1, px1, py2, px2))
        self._outElementFillColor(e)
        self._outElementStrokeColor(e)
        #self._out('alert(myScriptPath() + "%s");' % path)
        self._out('pbElement.place(File(myScriptPath() + "%s"));' % path)
        # FitOptions: http://jongware.mit.edu/idcs4js/pe_FitOptions.html
        self._out('pbElement.fit(FitOptions.CONTENT_TO_FRAME);')
        self._out('pbElement.fit(FitOptions.CENTER_CONTENT);')
        if scaleType is None:
            scaleType = SCALE_TYPE_FITWH
        if scaleType  != SCALE_TYPE_FITWH:
            self._out('pbElement.fit(FitOptions.PROPORTIONALLY);')
      
    def textBox(self, bs, p, w=None, h=None, clipPath=None, e=None):
        w, h = self.getWH(w, h, e)
        x, y = point2D(p)
        px1, py1, px2, py2 = self.getXY(x, y, w, h) # Calculate positions.
        self._out('/* TextBox */')
        self._outSelectPage(e)
        self._out('pbElement = pbPage.textFrames.add({geometricBounds:["%s", "%s", "%s", "%s"]});' % (py1, px1, py2, px2))
        self._outElementFillColor(e)
        self._outElementStrokeColor(e)
        self._out('pbElement.contents = "%s";' % bs.s)
        if e is not None or e.style:
            self._out('pbElement.parentStory.paragraphs.item(0).appliedParagraphStyle = pbDoc.paragraphStyles.item("%s", false);' % e.style['name'])   
        self._out('pbElement.textFramePreferences.insetSpacing = ["%s", "%s", "%s", "%s"]; // top, left, bottom, right' % (e.pt, e.pl, e.pb, e.pr))

    def scale(self, sx, sy, center=None):
        pass

    def lineDash(self, line):
        pass

    def line(self, p1, p2):
        pass

    def save(self):
        pass

    def restore(self):
        pass
       
    def saveDocument(self, path):
        """Write the InDesign-JavaScript content to path.
        """
        for basePath in (self.SCRIPT_PATH, self.SCRIPT_PATH1):
            if not os.path.exists(basePath):
                os.makedirs(basePath)
            f = codecs.open(basePath + path, 'w', encoding='utf-8')
            f.write(self.getOut())
            f.write('\n' * 4)
            f.close()
         
     

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
