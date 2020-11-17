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
    """The BackToTheCity theme is ...

    >>> theme = BackToTheCity()
    >>> theme.getColor('main back').hex
    'DED8D5'
    """

    NAME = 'Back to the City'

    #baseLogo1
    #baseLogo2
    #baseLogo3
    baseMain = spotColor(476)
    baseAccent = spotColor(1405)
    baseAlt1 = spotColor(139) 
    baseAlt2 = spotColor(480) 
    baseSupport1 = spotColor(421)
    baseSupport2 = spotColor(157)

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
