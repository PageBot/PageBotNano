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
#   wordlywise.py
#
import sys
sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano_050.themes.theme import BaseTheme
from pagebotnano_050.toolbox.color import spotColor

class WordlyWise(BaseTheme):
    """The WordlyWise theme is ...

    >>> theme = WordlyWise()
    """

    NAME = 'Wordly Wise'
    BASE_COLORS = dict(
        base0=spotColor('warmgray8u'),
        base1=spotColor(286),
        base2=spotColor(265),
        base3=spotColor(258),
        base4=spotColor(278), # Supporter1
        base5=spotColor(270),
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
