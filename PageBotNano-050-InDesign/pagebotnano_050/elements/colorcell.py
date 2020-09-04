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
#   colorcell.py
#
#   This source contains the class with knowledge about elements that
#   can be placed on a page.
#
import sys
sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

import drawBot

from pagebotnano_050.elements import Element, Rect, Text
from pagebotnano_050.babelstring import BabelString
from pagebotnano_050.toolbox.color import noColor, color
from pagebotnano_050.constants import CENTER

FONT_NAME = 'Verdana'
LABEL_SIZE = 10
LEADING = 12

class ColorCell(Element):
    """The ColorCell offers various options to display the recipe of a color.

    >>> from pagebotnano_050.document import Document
    >>> doc = Document(w=120, h=120)
    >>> page = doc.newPage()
    >>> page.padding = 10
    >>> c = color(name='orange')
    >>> e = ColorCell(c, x=page.pl, y=page.pb, w=page.pw, h=page.ph)
    >>> page.addElement(e)
    >>> doc.export('_export/ColorCell.png')
    """
    def __init__(self, c, style=None, themePosition=None, **kwargs):
        Element.__init__(self, **kwargs)
        self.c = c
        if style is None:
            style = dict(font=FONT_NAME, fontSize=LABEL_SIZE, lineHeight=LEADING, 
                fill=0, align=CENTER)
        self.style = style
        self.themePosition = themePosition

    def compose(self, doc, page, parent=None):
        """Compose the cell as background color, with recipes text block on top.

        """
        e = Rect(x=0, y=0, w=self.w, h=self.h, fill=self.c)
        self.addElement(e)

        # Mark approximated color recipes by parenthesis.
        # They are not an exact match, but closest known value for this color.
        Cmyk, cMyk, cmYk, cmyK = self.c.cmyk 
        s = '#%s\n(%s)\n(cmyk %d %d %d %d)\n(Spot %s)\n(RAL %s)' % \
            (self.c.hex, self.c.name.capitalize(), Cmyk*100, cMyk*100, cmYk*100, cmyK*100, 
                self.c.spot, self.c.ral)
        if self.themePosition is not None:
            s += '\nColor[%d][%d]' % (base, shade)
        bs = BabelString(s, self.style)
        tw, th = bs.textSize
        e = Text(bs, x=self.w/2, y=th-self.style.get('lineHeight', 0)/2, w=self.w, h=self.h)
        self.addElement(e)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
