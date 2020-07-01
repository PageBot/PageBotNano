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

if __name__ == "__main__":
    sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano_010.themes.theme import BaseTheme
from pagebotnano_010.toolbox.color import spotColor

class IntoTheWoods(BaseTheme):
    """The IntoTheWoods theme is ...

    >>> theme = IntoTheWoods
    """

    NAME = 'Into the Woods'
    BASE_COLORS = dict(
        base0=spotColor('gray10u'),
        base1=spotColor(348),
        base2=spotColor(376),
        base3=spotColor(381),
        base4=spotColor(392), # Supporter1
        base5=spotColor(398),
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
