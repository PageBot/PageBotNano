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
from copy import copy
import drawBot

if __name__ == "__main__":
    sys.path.insert(0, "../..") # So we can import pagebotnano without installing.
  
from pagebotnano.elements import Element, Rect, Text
from pagebotnano.themes import DefaultTheme
from pagebotnano.babelstring import BabelString
from pagebotnano.toolbox.color import noColor, color
from pagebotnano.constants import *
from pagebotnano.toolbox.units import pt

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
CMYK_SHORT = 'cmykShort' # Show abbreviated CMYK color recipce
NAME = 'name' # Show approximated name
RAL = 'ral' # Show approximated closest RAL recipe.
THEME = 'theme' # (x=shade, y=base) Show theme position, if defined.
COLOR_LABELS = (HEX, RGB, NAME, CMYK, CMYK_SHORT, SPOT, RAL, THEME)

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
            elif label == CMYK_SHORT:
                Cmyk, cMyk, cmYk, cmyK = self.c.cmyk 
                recipe = 'c%dm%dy%dk%d' % (Cmyk*100, cMyk*100, cmYk*100, cmyK*100)
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
                    recipes.append('Theme %d %d' % self.themePosition) # shade, base (x, y)
        return '\n'.join(recipes)

    def compose(self, doc, page, parent=None):
        """Compose the cell as background color, with recipes text block on top.

        """
        label = self._getLabel()

        if self.layout == SPOTSAMPLE:
            # Mark abbreviated color recipes by parenthesis.
            # They are not an exact match, but closest known value for this color.

            bs = BabelString(label, self.style)
            tw, th = bs.textSize

            # Used padding-bottom (self.pb) also as gutter between color rectangle and labels
            e = Rect(x=self.pl, y=th+self.pb, w=self.pw, h=self.ph-th-self.pb, fill=self.c)
            self.addElement(e)

            e = Text(bs, x=self.w/2, y=th-self.style.get('fontSize') + self.pb, w=self.w, h=self.h)
            self.addElement(e)

        else: 
            # Default layout is OVERLAY. Check the text color to be enough contrast with the background.
            # Otherwise flip between black and white.
            style = copy(self.style) # Copy as we are going to alter it
            if self.c.gray < 0.33: # Dark color?
                style['fill'] = color(1) # White text
            else:
                style['fill'] = color(0)
            bs = BabelString(label, style)
            tw, th = bs.textSize

            e = Rect(x=self.pl, y=self.pb, w=self.pw, h=self.ph, fill=self.c)
            self.addElement(e)

            e = Text(bs, x=self.w/2, y=th-self.style.get('fontSize')*2/3 + self.pb, w=self.w, h=self.h)
            self.addElement(e)


class ColorMatrix(Element):
    """
    >>> from pagebotnano.document import Document
    >>> from pagebotnano.constants import A4
    >>> H, W = A4 # Use as landscape
    >>> theme = DefaultTheme()
    >>> doc = Document(w=W, h=H, theme=theme)
    >>> page = doc.newPage()
    >>> page.padding = 20
    >>> cellPadding = (0, 3, 0, 3)
    >>> labelStyle = labelStyle=dict(fontSize=8, font='Verdana', lineHeight=10, align=CENTER)
    >>> labels = (HEX, RAL, CMYK_SHORT, THEME)
    >>> cm = ColorMatrix(theme, x=page.pl, y=page.pn, w=page.pw, h=page.ph, 
    ...     labelStyle=labelStyle, labels=labels, layout=SPOTSAMPLE, cellPadding=cellPadding)
    >>> page.addElement(cm)
    >>> page = doc.newPage()
    >>> cm = ColorMatrix(theme, x=page.pl, y=page.pn, w=page.pw, h=page.ph, 
    ...     labelStyle=labelStyle, labels=labels, layout=OVERLAY, cellPadding=cellPadding)
    >>> page.addElement(cm)
    >>> page = doc.newPage()
    >>> page.w, page.h = page.h, page.w # Flip from landscape to portrait
    >>> cm = ColorMatrix(theme, x=page.pl, y=page.pn, w=page.pw, h=page.ph, 
    ...     labelStyle=labelStyle, labels=(HEX,), layout=SPOTSAMPLE, cellPadding=cellPadding)
    >>> page.addElement(cm)
    >>> len(doc)
    3
    >>> doc.export('_export/ColorMatrix.pdf')

    """
    FONT_NAME = 'Verdana'
    FONT_SIZE = 10
    LEADING = 1.2

    def __init__(self, theme=None, layout=None, labels=None, 
        labelStyle=None, titleStyle=True, captionStyle=True, cellPadding=None,
        **kwargs):
        Element.__init__(self, **kwargs)
        self.theme = theme # If None, take the theme of the doc.
        self.layout = layout # Type of layouts in COLOR_LAYOUTS
        self.labels = labels # Type of color labels to show in COLOR_LABELS
        self.labelStyle = labelStyle
        self.titleStyle = titleStyle
        self.captionStyle = captionStyle
        self.cellPadding = cellPadding or (0, 0, 0, 0)

    def compose(self, doc, page, parent=None):
        """Compose the self.elements with ColorCell instances, as now we 
        know the actual size of self.
        Draw the cells of the theme in the given element size.
        """
        if self.theme is None:
            self.theme = doc.theme or DefaultTheme()
        if self.labelStyle is None:
            self.labelStyle = dict(font=FONT_NAME, fontSize=self.FONT_SIZE, align=CENTER,
                lineHeight=self.FONT_SIZE*self.LEADING) 
        if self.labels is None:
            self.labels = (HEX,)

        fontName = self.labelStyle.get('fontName', self.FONT_NAME)
        fontSize = self.labelStyle.get('fontSize', self.FONT_SIZE)
        textFill = self.theme.colors[0][4]
        backgroundFill = self.theme.getColor(0,2)

        if self.titleStyle and not isinstance(self.titleStyle, dict):
            self.titleStyle = dict(font=fontName, fontSize=fontSize*2, 
                fill=textFill, lineHeight=fontSize*2*self.LEADING) 
        if self.captionStyle and not isinstance(self.captionStyle, dict):
            self.captionStyle = dict(font=fontName, fontSize=fontSize, 
                fill=textFill, lineHeight=self.LEADING) 

        #e = Rect(x=self.pl, y=self.pb, w=self.pw, h=self.ph, fill=backgroundFill)
        #self.addElement(e)

        cols = len(self.theme.colors[0])
        rows = len(self.theme.colors)
        cw = self.pw/cols # Column width
        ch = self.ph/rows # Column height
        for shade in range(cols):
            for base in range(rows):
                # Get the color from the theme color matrix and add as rectangle
                # This is the extened example, instead of using the ColorCell element.
                c = self.theme.colors[base][shade]
                # If textColor not defined, then get it from the theme, based on the
                # darkness of the current color.
                tc = self.theme.textColor(base, shade)

                # The ColorCell element takes care of showing the color as rectangle
                # and the lines of various recipes on top.
                e = ColorCell(c, x=self.pl+shade*cw, y=self.pb+base*ch, w=cw, h=ch, 
                    themePosition=(shade, base), layout=self.layout, labels=self.labels, 
                    style=self.labelStyle, padding=self.cellPadding)
                e.pb = self.labelStyle['lineHeight']
                self.addElement(e)
                e.compose(doc, page, parent=self) # Do recursive compose.

        if self.titleStyle:        
            # Add background rectangle on top with theme name and mood. getColor(shade, base)
            bs = BabelString('%s – %s' % (self.theme.name, self.theme.mood), self.titleStyle)
            tw, th = bs.textSize
            e = Text(bs, x=self.pl+fontSize/2, y=self.h-self.pt*2/3, w=self.w)
            self.addElement(e)

        if self.captionStyle:
            bs = BabelString('Colors with (parenthesis) are approximated to the closest recipe.', 
                self.captionStyle)
            tw, th = bs.textSize
            e = Text(bs, x=self.pl, y=self.pb-th, w=self.pw)
            self.addElement(e)

            captionStyle2 = copy(self.captionStyle)
            captionStyle2['align'] = RIGHT
            bs = BabelString('Generated by PageBotNano', captionStyle2)
            tw, th = bs.textSize
            e = Text(bs, x=self.pl+self.pw, y=self.pb-th, w=self.pw)
            self.addElement(e)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
