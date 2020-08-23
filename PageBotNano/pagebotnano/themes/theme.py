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
#   theme.py
#
#   Defines the default style set and theme that every publication and document
#   can start with.
#
from copy import copy
import os # Import standard Python library to create the _export directory
import sys
sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano.toolbox.color import color
from pagebotnano.constants import (EN, CENTER, LEFT, RIGHT, 
    DEFAULT_FONT, DEFAULT_FONTSIZE, LIGHT, DARK)

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

    def getColor(self, shade, base):
        return self.colors[base][shade]

    #              Darkest --------- self --------- Lightest 
    MATRIX_RECIPE = [0.8, 0.6, 0.4, 0.2, 0, 0.8, 0.6, 0.4, 0.2]
    
    def makeColorMatrix(self, mood):
        """Create a 9 (shades) x 6 (base color) table, as source for theme styles.
        (white <--) lightest <-- light <-- lighter <-- base
        base --> darker --> dark --> darkest (--> black)

        self.colors[base][shade] In matrix is that self.colors[y][x]

        >>> # Sample below, see also ColorSpeciment.py
        >>> from pagebotnano.document import Document
        >>> from pagebotnano.themes import AllThemes, BackToTheCity
        >>> from pagebotnano.constants import *
        >>> from pagebotnano.elements import Rect, Text
        >>> from pagebotnano.babelstring import BabelString
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

        >>> from pagebotnano.themes import BackToTheCity
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
        if fonts is None:
            fonts = self.getDefaultFonts()

        ps = DEFAULT_FONTSIZE
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
            'leftPageNumber': None, # Undefined prevents from being drawn
            'centerPageNumber': dict(font=regular, fontSize=ps, lineHeight=lh14, fill=textColor),
            'rightPageNumber': None,
        }

if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]