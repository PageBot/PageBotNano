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
    COLOR_NAMES = []
    for base in NAME2BASE.keys():
        for shade in NAME2SHADE.keys():
            colorName = base + ' ' + shade
            COLOR_NAMES.append(colorName)
            COLOR_NAMES.append(colorName + ' diap') # Add modifiers

    # Optional coordinate as in chessboard (except for 6 rows and 9 cols :)
    ROW2BASE = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5}
    BASE2ROW = {0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6'}
    COL2SHADE = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8}
    SHADE2COL = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I'}

    def _getBaseShade(self, base, shade):
        mod = None # Optional modifier color filter name
        if isinstance(base, str) and len(base) == 2:
            col = self.COL2SHADE.get(base[0])
            row = self.ROW2BASE.get(base[1])
            if None not in (row, col):
                base, shade = col, row
        if shade is None:
            if isinstance(base, (list, tuple)):
                try:
                    base, shade = base
                except IndexError: 
                    shade = 4 # Take middle shade color column on error
                    base = -1 # Main color row
            elif isinstance(base, str):
                nameParts = base.split(' ')
                base = nameParts[0]
                shade = nameParts[1]
                if len(nameParts) == 3:
                    mod = nameParts[2]

        base = self.NAME2BASE.get(base, base) # Translate name to number if defined.
        shade = self.NAME2SHADE.get(shade, shade) # Translate name to number if defined.
        assert isinstance(base, int) and isinstance(shade, int), ("Error in (base, shade): (%s, %s)" % (base, shade))
        if mod == 'diap': # Flip the shade
            shade = -shade + len(self.COL2SHADE) - 1
        return base, shade

    def getColor(self, base, shade=None):
        """Answer the color, at position (base=y, shade=x).
        If shade is None, then try to split shade into two values.

        >>> from pagebotnano_060.themes import BackToTheCity
        >>> theme = BackToTheCity()
        >>> theme.getColor(0, 0).hex # Color index at matrix left-bottom
        'DED8D5'
        >>> theme.getColor('B2').hex # Color as in "chessboard" coordinate
        'C4B5A1'
        >>> theme.getColor('C3') == theme.getColor(2, 2)
        True
        >>> theme.getColor(-1, 4).hex # Color index from left-top
        'EDA04F'
        >>> theme.getColor(-2, -2).hex # Color index from right-top
        '4C4A46'
        >>> theme.getColor('main back').hex
        'FBECDC'
        >>> theme.getColor('support2 front').hex
        '120C09'
        >>> theme.getColor('support1', 'hover').hex
        '2B1C08'
        >>> theme.getColor(-3, 'text').hex
        '2A2521'
        >>> theme.getColor('main hover').hex # By name/shade related as function name
        '5F4020'
        >>> theme.getColor('alt1 text').hex
        '2A2521'
        >>> theme.getColor('accent front diap').hex # Make diap
        'F2F1EF'
        >>> theme.getColor('main back diap').hex
        '2F2010'
        """
        base, shade = self._getBaseShade(base, shade)
        # Clip to size of matrix
        return self.colors[base][shade]

    def getCell(self, base, shade=None):
        """Answer the chess-like cell name for this (base, shade) name

        >>> from pagebotnano_060.themes import BackToTheCity
        >>> theme = BackToTheCity()
        >>> theme.getCell('main front diap') 
        'A6'
        >>> theme.getCell('alt1 middle') 
        'E4'
        """
        base, shade = self._getBaseShade(base, shade)
        return '%s%s' % (self.SHADE2COL[shade], self.BASE2ROW[base]) # Reversed order: "C4"

    #              Darkest --------- self --------- Lightest 
    MATRIX_RECIPE = [0.8, 0.6, 0.4, 0.2, 0, 0.8, 0.6, 0.4, 0.2]
    
    def makeColorMatrix(self, mood):
        """Create a 9 (shades) x 6 (base color) table, as source for theme styles.
        (white <--) lightest <-- light <-- lighter <-- base
        base --> darker --> dark --> darkest (--> black)

        self.colors[base][shade] In matrix is that self.colors[y][x]
        (Note the reverse order of (x, y))

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
    def textColor(self, shade, base=3):
        """Answer the shade of base color that words best as text foreground
        on the `shade` color.

        >>> from pagebotnano_060.themes import BackToTheCity
        >>> theme = BackToTheCity()
        >>> theme.textColor(0, 3).name
        'black'
        """
        c = self.getColor(shade, base)
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

        textColor = self.textColor(2, 4) # shade, base
        accentColor = self.getColor(4, 3)

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