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

from pagebotnano_060.themes.theme import BaseTheme
from pagebotnano_060.toolbox.color import spotColor

class WordlyWise(BaseTheme):
    """The WordlyWise theme is ...

    >>> theme = WordlyWise()
    >>> theme.getColor('main').hex
    '928981'
    """
    NAME = 'Wordly Wise'
    
    #baseLogo1
    #baseLogo2
    #baseLogo3
    baseMain=spotColor('warmgray8u')
    baseAccent=spotColor(286)
    baseAlt1=spotColor(265)
    baseAlt2=spotColor(258)
    baseSupport1=spotColor(278)
    baseSupport2=spotColor(270)

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
