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
#   style.py
#
#   Defines the default style set and theme that every publication and document
#   can start with.
#
from copy import copy
import os # Import standard Python library to create the _export directory
import sys
sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano_060.toolbox.color import color
from pagebotnano_060.constants import (EN, CENTER, LEFT, RIGHT, 
    DEFAULT_FONT, DEFAULT_BODYSIZE, LIGHT, DARK)

class BaseTheme:
    def __init__(self, mood=LIGHT, name=None, fonts=None, styles=None):
        self.colors = self.makeColorMatrix(mood)
        # Defines the relation between typographic functions and font names.
        if fonts is None:
            fonts = self.getDefaultFonts()
        self.fonts = fonts
        # Collection of typographic style dictionaries
        # At least implementing the set of tag names that come from the 
        # Typesetter parsing a markdown file.
        if styles is None:
            styles = self.getDefaultStyles(self.fonts, self.colors) # To have basic set installed. 
        self.styles = styles
        self.name = name or self.NAME

    def getStyle(self, name):
        return self.styles.get(name)

    # Optional conversion of color base names to matrix row index number
    NAME2BASE = dict(
        main=5,
        accent=4,
        alt1=3,
        alt2=2,
        support1=1,
        support2=0,
    )
    # Optional conversion of color shade names to matrix col index number
    # Note that we cannot use names as "darkest" and "lightest" since
    # those depend if the theme is "dark" or "light"
    # Instead we call them "background" and "foreground" and other layer names.
    NAME2SHADE = dict(
        back=0,
        background=1,
        middle=4,
        foreground=7, hover=7,
        front=8, text=8,
    )
    def getColor(self, shade, base=None):
        """Answer the color, at position (shade=x, base=y).
        If base is None, then try to split shade into two values.

        >>> from pagebotnano_060.themes import BackToTheCity
        >>> theme = BackToTheCity()
        >>> theme.getColor(0, 0).hex # Color index at matrix left-bottom
        'DED8D5'
        >>> theme.getColor(4, -1).hex # Color index from left-top
        'EDA04F'
        >>> theme.getColor(-2, -2).hex # Color index from right-top
        '4C4A46'
        >>> theme.getColor('back main').hex
        'FBECDC'
        >>> theme.getColor('front support2').hex
        '120C09'
        >>> theme.getColor('hover', 'support1').hex
        '2B1C08'
        >>> theme.getColor('text', -3).hex
        '2A2521'
        """
        if base is None:
            if isinstance(shade, (list, tuple)):
                try:
                    shade, base = shade
                except IndexError: 
                    shade = 4 # Take middle shade color on error
                    base = 0 # 
            elif isinstance(shade, str):
                shade, base = shade.split(' ')
        if base in self.NAME2BASE:
            base = self.NAME2BASE.get(base, base) # Translate name to number if defined.
        if shade in self.NAME2SHADE:
            shade = self.NAME2SHADE.get(shade, shade) # Translate name to number if defined.
        # Clip to size of matrix
        return self.colors[base][shade]

    #              Darkest --------- self --------- Lightest 
    MATRIX_RECIPE = [0.8, 0.6, 0.4, 0.2, 0, 0.8, 0.6, 0.4, 0.2]
    
    def makeColorMatrix(self, mood):
        """Create a 9 (shades) x 6 (base color) table, as source for theme styles.
        (white <--) lightest <-- light <-- lighter <-- base
        base --> darker --> dark --> darkest (--> black)

        self.colors[base][shade] In matrix is that self.colors[y][x]
        (Note the reverse order of (x, y))

        >>> # Sample below, see also ColorSpeciment.py
        >>> from pagebotnano_060.document import Document
        >>> from pagebotnano_060.themes import AllThemes, BackToTheCity
        >>> from pagebotnano_060.constants import *
        >>> from pagebotnano_060.elements import Rect, Text
        >>> from pagebotnano_060.babelstring import BabelString
        >>> theme = BackToTheCity()
        >>> len(theme.colors)
        6
        >>> len(theme.colors[0])
        9
        >>> w = h = 800
        >>> doc = Document(w=w, h=h)
        >>> for Theme in AllThemes:
        ...     for mood in (DARK, LIGHT):
        ...         theme = Theme(mood=mood)
        ...         page = doc.newPage()
        ...         page.padding = 80
        ...         cw = page.pw/len(theme.colors[0]) # Column width
        ...         ch = page.ph/len(theme.colors) # Column height
        ...         for shade in range(len(theme.colors[0])):
        ...             for base in range(len(theme.colors)):
        ...                 c = theme.colors[base][shade]
        ...                 e = Rect(x=page.pl+shade*cw, y=page.pb+base*ch, w=cw, h=ch, fill=c)
        ...                 page.addElement(e)
        ...         # Add background rectangle on top with theme name and mood. getColor(shade, base)
        ...         e = Rect(x=page.pl, y=page.h-page.pt, w=page.pw, h=page.pt, fill=theme.getColor(0,2))
        ...         page.addElement(e)
        ...         style = dict(font='Georgia', fontSize=24, fill=theme.getColor(-2,2), indent=20)
        ...         bs = BabelString('%s – %s' % (theme.name, mood), style)
        ...         tw, th = bs.textSize
        ...         e = Text(bs, x=page.pl, y=page.h-page.pt*3/5)
        ...         page.addElement(e)
        >>> doc.export('_export/ThemeColors.pdf')
        """
        if mood is None:
            mood = LIGHT
        r = self.MATRIX_RECIPE # Defined by the inheriting class
        matrix = []
        for baseName, c in sorted(self.BASE_COLORS.items()):
            if mood == LIGHT:
                matrix.append(
                    (c.lighter(r[0]), 
                    c.lighter(r[1]), 
                    c.lighter(r[2]), 
                    c.lighter(r[3]), 
                    c, 
                    c.darker(r[5]), 
                    c.darker(r[6]), 
                    c.darker(r[7]), 
                    c.darker(r[8]),
                ))
            else: # mood == DARK:
                matrix.append(
                    (c.darker(r[8]), 
                    c.darker(r[7]), 
                    c.darker(r[6]), 
                    c.darker(r[5]), 
                    c, 
                    c.lighter(r[3]), 
                    c.lighter(r[2]), 
                    c.lighter(r[1]),
                    c.lighter(r[0]),
                ))
        return matrix

    def getDefaultFonts(self):
        regular = DEFAULT_FONT
        bold = DEFAULT_FONT+'-Bold'
        italic = DEFAULT_FONT+'-Italic'
        boldItalic = DEFAULT_FONT+'-BoldItalic'

        # Default font set, used by Theme
        return dict(
            regular=regular,
            bold=bold,
            italic=italic,
            boldItalic=boldItalic,
            monospaced='Courier-Regular'
        )
    def textColor(self, base, shade):
        """Answer the shade of base color that words best as text foreground
        on the `shade` color.

        >>> from pagebotnano_060.themes import BackToTheCity
        >>> theme = BackToTheCity()
        >>> theme.textColor(3, 0).name
        'black'
        """
        c = self.colors[base][shade]
        if c.averageRgb < 0.4:
            return color(1)
        return color(0)

    def getDefaultStyles(self, fonts, colors):
        """Answer the default set of styles, to get any theme started.
        At least, implement the tags defined in HTML_TEXT_TAGS
        """
        ps = DEFAULT_BODYSIZE
        ps5 = 3*ps
        ps4 = 2.5*ps
        ps3 = 2*ps
        ps2 = 1.5*ps
        lh11 = 1.1*ps
        lh12 = 1.2*ps
        lh13 = 1.3*ps
        lh14 = 1.4*ps

        textColor = self.textColor(4, 2)
        accentColor = self.getColor(3, 4)

        regular = fonts['regular']
        bold = fonts['bold']
        italic = fonts['italic']
        boldItalic = fonts['boldItalic']
        monospaced = fonts['monospaced']
        return {
            'h1': dict(font=bold, fontSize=ps5, lineHeight=lh11, fill=textColor),
            'h2': dict(font=bold, fontSize=ps4, lineHeight=lh12, fill=textColor),
            'h3': dict(font=italic, fontSize=ps3, lineHeight=lh13, fill=textColor), 
            'h3 b': dict(font=bold, fontSize=ps3, lineHeight=lh13, fill=textColor), 
            'h4': dict(font=regular, fontSize=ps2, lineHeight=lh14, fill=textColor), 
            'h5': dict(font=bold, fontSize=ps, lineHeight=lh14, fill=textColor), 
            'h6': dict(font=italic, fontSize=ps, lineHeight=lh14, fill=textColor), 
            'p': dict(font=regular, fontSize=ps, lineHeight=lh14, fill=textColor), 
            'b': dict(font=bold, fontSize=ps, lineHeight=lh14, fill=textColor), 
            'em': dict(font=italic, fontSize=ps, lineHeight=lh14, fill=textColor), 
            'i': dict(font=italic, fontSize=ps, lineHeight=lh14, fill=textColor), 
            'bi': dict(font=boldItalic, fontSize=ps, lineHeight=lh14, fill=textColor), 
            'img': dict(font=boldItalic, fontSize=ps, lineHeight=lh14, fill=textColor), 
            'strong': dict(font=bold, fontSize=ps, lineHeight=lh14, fill=textColor), 
            'a': dict(font=bold, fontSize=ps, lineHeight=lh14, fill=accentColor), 
            'a.hover': dict(font=bold, fontSize=ps, lineHeight=lh14, fill=accentColor.darker()), 
            'hr': dict(font=regular, fontSize=ps, lineHeight=lh14, fill=textColor),
            'python': dict(font=monospaced, fontSize=ps, lineHeight=lh14, fill=textColor), 
            'code': dict(font=monospaced, fontSize=ps, lineHeight=lh14, fill=textColor), 
            'blockquote': dict(font=italic, fontSize=ps, lineHeight=lh14, fill=textColor), 
            'ul': dict(font=regular, fontSize=ps, lineHeight=lh14, fill=textColor), 
            'ol': dict(font=regular, fontSize=ps, lineHeight=lh14, fill=textColor), 
            'li': dict(font=regular, fontSize=ps, lineHeight=lh14, fill=textColor), 
        }

if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]