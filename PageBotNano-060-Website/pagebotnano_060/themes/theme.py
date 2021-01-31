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

# Should be identical to pagebotnano_020-Themes
from pagebotnano_060.toolbox.color import color
from pagebotnano_060.constants import (EN, CENTER, LEFT, RIGHT, 
    DEFAULT_FONT, DEFAULT_BODYSIZE, LIGHT, DARK)

class BaseTheme:

    NAME = 'BaseTheme'

    def __init__(self, mood=LIGHT, name=None, fonts=None, styles=None):
        self.name = name or self.NAME
        self.colors = self.makeColorMatrix(mood)
        if mood == LIGHT:
            self.lowest = self.white = color(1) # White as lowest back-most layer = paper
            self.highest = self.black = color(0) # Black as front-most contrast
        else:
            self.lowest = self.black = color(0) # Black as lowest back-most layer = paper
            self.highest = self.white = color(1) # White as front-most contrast
        self.gray = color(0.5) # Default middle gray
        # Defines the relation between typographic functions and font names.
        if fonts is None:
            fonts = self.getDefaultFonts()
        self.fonts = fonts
        # Collection of typographic style dictionaries
        # At least implementing the set of tag names that come from the 
        # Typesetter parsing a markdown file.
        #if styles is None:
        #    styles = self.getDefaultStyles(self.fonts, self.colors) # To have basic set installed. 
        self.styles = styles

    def getStyle(self, name):
        return self.styles.get(name)

    # Optional coordinate as in chessboard (except for 9 rows and 9 cols :)
    # We need a "middle" shade, so the cols need to be uneven.
    # 9 base colors is just a coincidence to make the matrix square.
    CELL2ROW = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8}
    ROW2CELL = {0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8', 8: '9'}
    CELL2COL = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8}
    COL2CELL = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I'}

    LOGO1, LOGO2, LOGO3 = LOGO_NAMES = 'logo1', 'logo2', 'logo3'
    MAIN = 'main'
    ACCENT = 'accent'
    ALT1, ALT2 = 'alt1', 'alt2'
    SUPPORT1, SUPPORT2 = 'support1', 'support2'

    # Optional conversion of color base names to matrix row index number
    BASE2ROW = {
        LOGO1:8, LOGO2:7, LOGO3: 6, # Optional 
        MAIN:5,
        ACCENT:4, 
        ALT1:3, ALT2:2,
        SUPPORT1:1, SUPPORT2:0,
    }
    ROW2BASE = {} # Make x-ref
    for key, value in BASE2ROW.items():
        ROW2BASE[value] = key

    # Optional conversion of color shade names to matrix col index number
    # Note that we cannot use names as "darkest" and "lightest" since
    # those depend if the theme is "dark" or "light"
    # Instead we call them "background" and "foreground" and other layer names.
    BACK, BACKGROUND, BACKWARD,BEHIND = 'back', 'background', 'backward', 'behind',
    MIDDLE = 'middle'
    AHEAD, FORWARD, FOREGROUND, FRONT = 'ahead', 'forward', 'foreground', 'front'
    # Alias names
    HOVER = 'hover'
    TEXT = 'text'

    # Black & white equivalents, flipping is based o mood
    LOWEST = 'lowest' # Default generic white (for light mood) or black (for dark mood)
    HIGHEST = 'highest' # Default generic black (for light mood) or white (for dark mood)
    WHITE = 'white'
    BLACK = 'black'
    CONTRAST = (LOWEST, HIGHEST, WHITE, BLACK)

    SHADE2COL = {
        BACK:0,
        BACKGROUND:1,
        BACKWARD:2,
        BEHIND:3,
        MIDDLE:4,
        AHEAD:5,
        FORWARD:6,
        FOREGROUND:7, #HOVER:7,
        FRONT:8, #TEXT:8,
    }
    COL2SHADE = {} # Make x-ref
    for key, value in SHADE2COL.items():
        COL2SHADE[value] = key
    
    # Add aliases later, because they don't fit in the x-ref
    SHADE2COL[HOVER] = 7
    SHADE2COL[TEXT] = 8

    # Make the list of all possible color name (base + shade) combinations in the matrix
    COLOR_NAMES = []
    for base in BASE2ROW.keys():
        for shade in SHADE2COL.keys():
            colorName = base + ' ' + shade
            COLOR_NAMES.append(colorName)
            COLOR_NAMES.append(colorName + ' diap') # Add modifiers

    @classmethod
    def _getBaseShade2RowCol(cls, base, shade=None, diap=False):
        """Answer the (row, col) from interpreted (base, shade)

        >>> theme = BaseTheme()
        >>> theme._getBaseShade2RowCol('main', 'middle')
        (5, 4)
        >>> theme._getBaseShade2RowCol('main', -2)
        (5, -2)
        >>> theme._getBaseShade2RowCol('logo2 background')
        (7, 1)
        >>> theme._getBaseShade2RowCol('logo2 background diap')
        (7, 7)
        """
        mod = None # Optional modifier color filter name
        if isinstance(base, str) and len(base) == 2: # base = 'C4'?
            col = cls.CELL2COL.get(base[0])
            row = cls.CELL2ROW.get(base[1])
            if None not in (row, col):
                base, shade = col, row
        if shade is None:
            if isinstance(base, (list, tuple)):
                try:
                    base, shade = base
                except IndexError: 
                    shade = self.MIDDLE # Take middle shade color column on error
                    base = self.MAIN # Main color row
            elif isinstance(base, str):
                nameParts = base.split(' ')
                if len(nameParts) == 1: # Assume to be base, shade = MIDDLE
                    shade = cls.MIDDLE
                elif len(nameParts) == 2:
                    base, shade = nameParts
                elif len(nameParts) == 3:
                    base = nameParts[0]
                    shade = nameParts[1]
                    diap = nameParts[2] == 'diap' # Overwriting @diap attribute
                else:
                    raise ValueError('Theme base "%s" wrong format' % base)

        row = cls.BASE2ROW.get(base, base) # Translate name to row number if defined.
        col = cls.SHADE2COL.get(shade, shade) # Translate name to col number if defined.
        assert isinstance(row, int) and isinstance(col, int), ("Error in (base, shade): (%s, %s)" % (row, col))
        if diap: # Flip the col for diapositive.
            col = -col + 8
        return row, col

    def getColor(self, base, shade=None, diap=None, a=1):
        """Answer the color, at position (base=y, shade=x).
        If shade is None, then try to split shade into two values.

        >>> from pagebotnano_060.themes import BackToTheCity
        >>> theme = BackToTheCity()
        >>> theme.getColor(0, 0).hex # Color index at matrix left-bottom
        'FBECDC'
        >>> theme.getColor('B2').hex # Color as in "chessboard" coordinate
        'E5E3DF'
        >>> theme.getColor('C3') == theme.getColor(2, 2)
        True
        >>> theme.getColor(-1, 4).hex # 'logo1 middle' color by index from left-top
        '808080'
        >>> theme.getColor(-2, -2).hex # 'logo2 foreground' color by index from right-top
        '202020'
        >>> theme.getColor('main back').hex
        'DED8D5'
        >>> theme.getColor('support2 front').hex
        '2F2010'
        >>> theme.getColor('support1', 'hover').hex # Equals 'support1 foreground'
        '4C4A46'
        >>> theme.getColor(-4, 'text').hex # Equivalent to 'main front'
        '120C09'
        >>> theme.getColor('main hover').hex # Equivalent to 'main foreground'
        '241811'
        >>> theme.getColor('alt1 text').hex # Equivalent to 'alt1 front'
        '231701'
        >>> theme.getColor('accent front diap').hex # 'accent front' + 'diap' --> equivalent to 'accent back'
        'E1DAD0'
        >>> theme.getColor('main back diap').hex # 'main back' + 'diap' --> equivalent to 'main front'
        '120C09'
        >>> theme.getColor('main text', a=0.5).css
        'rgba(0.87, 0.85, 0.83, 0.50)'
        >>> theme.getColor('main text diap', a=0.5).css

        """
        if base in self.CONTRAST:
            c = getattr(self, base)
        else:
            row, col = self._getBaseShade2RowCol(base, shade, diap)
            c = copy(self.colors[row][col])
        c.a = a
        return c

    @classmethod
    def getCell(cls, base, shade=None):
        """Answer the chess-like cell name for this (base, shade) name

        >>> from pagebotnano_060.themes import BackToTheCity
        >>> theme = BackToTheCity()
        >>> theme.getCell('main front diap') 
        'A6'
        >>> theme.getCell('alt1 middle') 
        'E4'
        """
        row, col = cls._getBaseShade2RowCol(base, shade)
        return '%s%s' % (cls.COL2CELL[col], cls.ROW2CELL[row]) # Reversed order: "C4"

    @classmethod
    def getBaseShade(cls, row, col):
        """Answer the base-shade name, as defined by row and col

        >>> from pagebotnano_060.themes import BackToTheCity
        >>> theme = BackToTheCity()
        >>> theme.getBaseShade(2, 2) 
        'alt2 backward'
        """
        return '%s %s' % (cls.ROW2BASE[row], cls.COL2SHADE[col]) # Reversed order: "C4"

    # Recipe tables for dark/middle/light color transformation of base colors
    # This is the default behvior. Can be redefined by inheriting Theme classes.
    #              Darkest --------- self --------- Lightest 
    SHADE_RECIPE = (0.2, 0.4, 0.6, 0.8, 0, 0.2, 0.4, 0.6, 0.8) # Dark/middle/right recipe for main colors
    LOGO_RECIPE = (0, 0.25, 0.5, 0.75, 0, 0.25, 0.5, 0.75, 1) # Black/logo color/white recipe for logo colors
    # Standard recipes for conversion. Separate rows be altered by inhering Them classes
    RECIPES = { 
        8: LOGO_RECIPE,
        7: LOGO_RECIPE,
        6: LOGO_RECIPE,
        5: SHADE_RECIPE,
        4: SHADE_RECIPE,
        3: SHADE_RECIPE,
        2: SHADE_RECIPE,
        1: SHADE_RECIPE,
        0: SHADE_RECIPE,
    }
    # Base class colors, to be redefined by inheriting Theme classes
    baseLogo1 = baseLogo2 = baseLogo3 = baseMain = baseAccent = \
    baseAlt1 = baseAlt2 = baseSupport1 = baseSupport2 = color(0.5)

    def getThemeBase(self):
        """Answer the dictionary of base colors, unique for this Theme,
        using the class colors.

        >>> theme = BaseTheme()
        >>> theme.getThemeBase()['main']
        Color(r=0.5, g=0.5, b=0.5)
        """
        return dict(
            logo1=self.baseLogo1,
            logo2=self.baseLogo2,
            logo3=self.baseLogo3,
            main=self.baseMain,
            accent=self.baseAccent,
            alt1=self.baseAlt1,
            alt2=self.baseAlt2,
            support1=self.baseSupport1,
            support2=self.baseSupport2,
        )

    def makeColorMatrix(self, mood):
        """Create a 9 (base color) x 9 (shades) table, as source for theme styles.
        (white <--) lightest <-- light <-- lighter <-- base
        base --> darker --> dark --> darkest (--> black)

        self.colors[base][shade] In the matrix that self.colors[y][x]
        (Note the reverse order of (x, y))

        """
        if mood is None:
            mood = LIGHT
        # Make default matrix
        c = self.baseMain # Default is middle gray color
        matrix = [ # Matrix of 9 x 9
            [c, c, c, c, c, c, c, c, c],
            [c, c, c, c, c, c, c, c, c],
            [c, c, c, c, c, c, c, c, c],
            [c, c, c, c, c, c, c, c, c],
            [c, c, c, c, c, c, c, c, c],
            [c, c, c, c, c, c, c, c, c],
            [c, c, c, c, c, c, c, c, c],
            [c, c, c, c, c, c, c, c, c],
            [c, c, c, c, c, c, c, c, c],
        ] 
        # Now fill with the base colors and calculate the shade of the 
        # inheriting Theme clase
        themeBase = self.getThemeBase() # Re-defined by the inheriting Theme class
        for base, row in self.BASE2ROW.items():
            bc = themeBase.get(base, c) # Get base if defined, otherwise use c.
            # Select the shading recipe table.
            # This way the logo colors run all the way from black to white,
            # where the darkest and lightest shades keep a fraction of the base color
            # using self.SHADE_RECIPE or self.LOGO_RECIPE
            # These recipes can be redefined by the inheriting Theme class
            r = self.RECIPES[row]
            baseRow = [
                bc.lighter(r[8]), 
                bc.lighter(r[7]), 
                bc.lighter(r[6]), 
                bc.lighter(r[5]), 
                bc, 
                bc.darker(r[3]), 
                bc.darker(r[2]), 
                bc.darker(r[1]), 
                bc.darker(r[0]),
            ]
            if mood == DARK: # Mood decides if the colom shades should be flipped
                baseRow.reverse()
            matrix[row] = baseRow
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

    def textColor(self, base, shade=None):
        """Answer the shade of base color that words best as text front or back
        on the `shade` color.

        >>> from pagebotnano_060.themes import BackToTheCity
        >>> theme = BackToTheCity()
        >>> theme.textColor('logo1 front').name
        'white'
        """
        c = self.getColor(base, shade)
        if c.averageRgb >= 0.4:
            return c
        return self.getColor(base, shade, diap=True)

    def getDefaultStyles(self, fonts=None, colors=None):
        """Answer the default set of styles, to get any theme started.
        At least, implement the tags defined in HTML_TEXT_TAGS

        >>> theme = BaseTheme()
        >>> styles = theme.getDefaultStyles()

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

        textColor = self.textColor('main text') # base, shade
        accentColor = self.getColor('accent text')

        if fonts is None:
            fonts = self.getDefaultFonts()

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