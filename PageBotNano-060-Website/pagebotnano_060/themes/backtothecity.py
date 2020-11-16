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
#   backtothecity.py
#
import sys
sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano_060.themes.theme import BaseTheme
from pagebotnano_060.toolbox.color import spotColor

class BackToTheCity(BaseTheme):
    """The BackToTheCity theme is ..."""

    NAME = 'Back to the City'
    THEME_COLORS = dict(
        #logo1
        #logo2
        #logo3
        main=spotColor(476),
        accent=spotColor(1405),
        alt1=spotColor(139), 
        alt2=spotColor(480), 
        support1=spotColor(421),
        support2=spotColor(157),
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
