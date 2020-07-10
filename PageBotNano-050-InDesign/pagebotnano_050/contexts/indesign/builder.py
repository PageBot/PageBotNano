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
from pagebotnano_050.toolbox.color import noColor
from pagebotnano_050.constants import *

class InDesignBuilder:

    PB_ID = 'inds'

    # Exporting directly into the InDesign 
    SCRIPT_PATH = '/Users/petr/Library/Preferences/Adobe InDesign/Version 14.0/en_US/Scripts/Scripts Panel/PageBot/'
    SCRIPT_PATH1 = '_export/'

    def __init__(self):
        self._fillColor = noColor
        self._strokeColor = noColor
        self._strokeWidth = 1

        self.jsOut = []

    def getWH(self, w, h, e):
        if e is not None:
            w = w or e.w
            h = h or e.h
        else:
            w = w or DEFAULT_WIDTH
            h = h or DEFAULT_HEIGHT
        return w, h

    def getXY(self, x, y, w, h):
        """Calculate positions, answer as rectangle of bounding box
        (topY, rightX, bottomY, leftX) to be used in origin-top setting of InDesign canvas.
        """
        return y+h, x+w, y, x  

    def _out(self, s):
        self.jsOut.append(s)

    def getOut(self):
        return '\n'.join(self.jsOut)

    def newDocument(self, w=None, h=None, doc=None):
        if doc is not None:
            w = w or doc.w
            h = h or doc.h
        else:
            w = w or DEFAULT_WIDTH
            h = h or DEFAULT_HEIGHT
        self._out('/* Document */')
        self._out(JSX_LIB)
        self._out('var pbDoc = app.documents.add();')
        self._out('pbDoc.documentPreferences.pagesPerDocument = %d;' % len(doc.pages))
        if w is not None and h is not None:
            self._out('pbDoc.documentPreferences.pageWidth = "%s";' % w)
            self._out('pbDoc.documentPreferences.pageHeight = "%s";' % h)
            if w > h:
                self._out('pbDoc.documentPreferences.pageOrientation = PageOrientation.landscape;')
            else:
                self._out('pbDoc.documentPreferences.pageOrientation = PageOrientation.portrait;')
        self._out('pbDoc.documentPreferences.facingPages = false;')
        self._out('var pbPage;')
        self._out('var pbPageIndex = 0;')
        self._out('var pbElement;')
        self.outDocumentStyles(doc)

    def outDocumentStyles(self, doc):    
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
        >>> doc = Document(w=500, h=800, context=context)
        >>> doc.styles = styles # Overwrite all default styles.
        >>> context.b.outDocumentStyles(doc)
        >>> #context.b.getOut()
        """
        self._out('/* Paragraph styles */')
        for name, style in doc.styles.items():
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

    def _outSelectPage(self, e):
        """Output code to select the e.page if it is not selected already."""
        if e is not None:
            self._out('pbPageIndex = %d' % (e.page.index))
            self._out('pbPage = pbDoc.pages.item(pbPageIndex);')

    def newPage(self, w=None, h=None, page=None):
        w, h = self.getWH(w, h, page)
        self._out('/* Page */')
        if page is not None:
            self._outSelectPage(page)
        else:
            self._out('if (pbPage) pbPageIndex += 1;')
            self._out('pbPage = pbDoc.pages.item(pbPageIndex);')
        self._out('pbPage.resize(CoordinateSpaces.INNER_COORDINATES,')
        self._out('    AnchorPoint.CENTER_ANCHOR,')
        self._out('    ResizeMethods.REPLACING_CURRENT_DIMENSIONS_WITH,')
        self._out('    [%d, %d]);' % (w.pt, h.pt))
        if page is not None:
            pt, pr, pb, pl = page.padding # Padding is called margin in InDesign script.
            self._out('pbPage.marginPreferences.top = "%s";' % pt)
            self._out('pbPage.marginPreferences.right = "%s";' % pr)
            self._out('pbPage.marginPreferences.bottom = "%s";' % pb)
            self._out('pbPage.marginPreferences.left = "%s";' % pl)
 
    def rect(self, x, y, w=None, h=None, e=None):
        w, h = self.getWH(w, h, e)
        px1, py1, px2, py2 = self.getXY(x, y, w, h) # Calculate positions.
        self._out('/* Rect */')
        self._outSelectPage(e)
        self._out('pbElement = pbPage.rectangles.add({geometricBounds:["%s", "%s", "%s", "%s"]});' % (py1, px1, py2, px2))
        self._outElementFillColor(e)
        self._outElementStrokeColor(e)

    def oval(self, x, y, w=None, h=None, e=None):
        w, h = self.getWH(w, h, e)
        px1, py1, px2, py2 = self.getXY(x, y, w, h) # Calculate positions.
        self._out('/* Oval */')
        self._outSelectPage(e)
        self._out('pbElement = pbPage.ovals.add({geometricBounds:["%s", "%s", "%s", "%s"]});' % (py1, px1, py2, px2))
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
            
    def _outElementFillColor(self, e):
        """Set the fill color of pbElement to the current self._fillColor."""
        jsColor = None
        if e is not None:
            fillColor = e.fill
        else:
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
            
    def _outElementStrokeColor(self, e):
        """Set the fill color of pbElement to the current self._strokeColor."""
        jsColor = None
        if e is not None:
            strokeColor = e.stroke
            strokeWidth = e.strokeWidth
        else:
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
            f = codecs.open(basePath + path, 'w', encoding='utf-8')
            f.write(self.getOut())
            f.write('\n' * 4)
            f.close()
         
     

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
