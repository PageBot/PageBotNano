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
#   intothewoods.py
#
import sys
sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano_060.themes.theme import BaseTheme
from pagebotnano_060.toolbox.color import spotColor, rgbColor, color

class IntoTheWoods(BaseTheme):
    """The IntoTheWoods theme is ...

    >>> theme = IntoTheWoods()
    """

    NAME = 'Into the Woods'
    THEME_COLORS = dict(
        # Example logo colors, to be modified by an inheriting class.
        logo1=spotColor(300),
        logo2=color(1, 0, 0),
        logo3=color(0, 1, 0),
        # Theme colors
        main=spotColor('gray10u'),
        accent=spotColor(348),
        alt1=spotColor(376),
        alt2=spotColor(381),
        support1=spotColor(392), 
        support2=spotColor(398),
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
