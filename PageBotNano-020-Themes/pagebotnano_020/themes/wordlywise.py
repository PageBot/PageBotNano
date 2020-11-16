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

from pagebotnano_020.themes.theme import BaseTheme
from pagebotnano_020.toolbox.color import spotColor

class WordlyWise(BaseTheme):
    """The WordlyWise theme is ...

    >>> theme = WordlyWise()
    """
    NAME = 'Wordly Wise'
    THEME_COLORS = dict(
        #logo1
        #logo2
        #logo3
        main=spotColor('warmgray8u'),
        accent=spotColor(286),
        alt1=spotColor(265),
        alt2=spotColor(258),
        support1=spotColor(278),
        supposrt2=spotColor(270),
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
