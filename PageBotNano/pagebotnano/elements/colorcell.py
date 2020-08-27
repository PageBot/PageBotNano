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
import drawBot

if __name__ == "__main__":
    sys.path.insert(0, "../..") # So we can import pagebotnano without installing.
  
from pagebotnano.elements import Element, Rect, Text
from pagebotnano.babelstring import BabelString
from pagebotnano.toolbox.color import noColor, color
from pagebotnano.constants import CENTER

FONT_NAME = 'Verdana'
LABEL_SIZE = 10
LEADING = 13

# Names of layout options
OVERLAY = 'Overlay' # Rectangle with recipes overlay. Make sure that label color is right.
SPOTSAMPLE = 'SpotSample' # As standard spot color layout: color rectangle on top, recipes in white below.
COLOR_LAYOUTS = (None, OVERLAY, SPOTSAMPLE)

# Options for showing recipe labels
HEX = 'hex' # Show CSS hex color recipe
RGB = 'rgb' # Show RGB color recipe
SPOT = 'spot' # Show approximated closest spot color recipe
CMYK = 'cmyk' # Show CMYK color recipce
NAME = 'name' # Show approximated name
RAL = 'ral' # Show approximated closest RAL recipe.
THEME = 'theme' # (x=shade, y=base) Show theme position, if defined.
COLOR_LABELS = (HEX, RGB, NAME, CMYK, SPOT, RAL, THEME)

class ColorCell(Element):
    """The ColorCell offers various options to display the recipe of a color.

    >>> from pagebotnano.document import Document
    >>> doc = Document(w=120, h=200)
    >>> page = doc.newPage()
    >>> page.padding = 10
    >>> c = color(name='yellow')
    >>> e = ColorCell(c, x=page.pl, y=page.pb, w=page.pw, h=page.ph)
    >>> page.addElement(e)
    >>> page = doc.newPage()
    >>> page.padding = 10
    >>> c = color(name='cyan')
    >>> e = ColorCell(c, x=page.pl, y=page.pb, w=page.pw, h=page.ph, layout=SPOTSAMPLE, labels=COLOR_LABELS)
    >>> page.addElement(e)
    >>> page = doc.newPage()
    >>> page.padding = 10
    >>> c = color(spot=300)
    >>> e = ColorCell(c, x=page.pl, y=page.pb, w=page.pw, h=page.ph, layout=SPOTSAMPLE, labels=(SPOT, HEX, NAME))
    >>> page.addElement(e)
    >>> page = doc.newPage()
    >>> page.padding = 10
    >>> c = color(0.15)
    >>> e = ColorCell(c, x=page.pl, y=page.pb, w=page.pw, h=page.ph, labels=(HEX, NAME, CMYK))
    >>> e.style['fill'] = color(1) # Change the label color
    >>> page.addElement(e)
    >>> doc.export('_export/ColorCell.pdf')
    """
    def __init__(self, c, style=None, themePosition=None, layout=None, labels=None, **kwargs):
        Element.__init__(self, **kwargs)
        self.c = c
        if style is None:
            style = dict(font=FONT_NAME, fontSize=LABEL_SIZE, lineHeight=LEADING, 
                fill=0, align=CENTER)
        self.style = style
        self.themePosition = themePosition
        assert layout in COLOR_LAYOUTS
        self.layout = layout # Default layout is OVERLAY
        # The labels define which color recipe(s) will be shown 
        if not labels:
            labels = (HEX,)
        self.labels = labels

    def _getLabel(self):
        """Answer the label text, depending on the selected recipe options.
        """
        recipes = []
        for label in self.labels:
            if label == HEX:
                recipe = '#%s' % self.c.hex
                if not (self.c.isRgb or self.c.isRgba): # In case abbreviation
                    recipe = '(%s)' % recipe # then add parenthesis.
                recipes.append(recipe)
            elif label == NAME:
                recipe = self.c.name.capitalize()
                if not self.c.isName: # In case abbreviation
                    recipe = '(%s)' % recipe # then add parenthesis
                recipes.append(recipe)
            elif label == SPOT: # Can be name or number
                recipe = 'Spot %s' % str(self.c.spot).capitalize() 
                if not self.c.isSpot: # In case abbreviation
                    recipe = '(%s)' % recipe # then add parenthesis
                recipes.append(recipe)
            elif label == RGB:
                r, g, b = self.c.rgb 
                recipe = 'rgb %d %d %d' % (r*255, g*255, b*255)
                if not self.c.isRgb: # In case abbreviation
                    recipe = '(%s)' % recipe # then add parenthesis
                recipes.append(recipe)
            elif label == CMYK:
                Cmyk, cMyk, cmYk, cmyK = self.c.cmyk 
                recipe = 'cmyk %d %d %d %d' % (Cmyk*100, cMyk*100, cmYk*100, cmyK*100)
                if not self.c.isCmyk: # In case abbreviation
                    recipe = '(%s)' % recipe # then add parenthesis
                recipes.append(recipe)
            elif label == RAL:
                recipe = 'Ral %s' % self.c.ral
                if not self.c.isRal: # In case abbreviation
                    recipe = '(%s)' % recipe # then add parenthesis
                recipes.append(recipe)
            elif label == THEME:
                if self.themePosition:
                    recipes.append('Theme %d %d' % self.themePosition) # shade, base

        return '\n'.join(recipes)

    def compose(self, doc, page, parent=None):
        """Compose the cell as background color, with recipes text block on top.

        """
        label = self._getLabel()
        bs = BabelString(label, self.style)
        tw, th = bs.textSize

        if self.layout == SPOTSAMPLE:
            # Mark abbreviated color recipes by parenthesis.
            # They are not an exact match, but closest known value for this color.

            # Used padding-bottom (self.pb) also as gutter between color rectangle and labels
            e = Rect(x=0, y=th+self.pb, w=self.w, h=self.h-th-self.pb, fill=self.c)
            self.addElement(e)

            e = Text(bs, x=self.w/2, y=th-self.style.get('lineHeight', 0) + self.pb, w=self.w, h=self.h)
            self.addElement(e)

        else: # Default layout is OVERLAY
            e = Rect(x=0, y=0, w=self.w, h=self.h, fill=self.c)
            self.addElement(e)

            e = Text(bs, x=self.w/2, y=th-self.style.get('lineHeight', 0) + self.pb, w=self.w, h=self.h)
            self.addElement(e)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
