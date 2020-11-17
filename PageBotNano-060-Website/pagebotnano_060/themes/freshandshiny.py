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
#   freshandshiny.py
#
import sys
sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano_060.themes.theme import BaseTheme
from pagebotnano_060.toolbox.color import spotColor, rgbColor

class FreshAndShiny(BaseTheme):
    """The FreshAndShiny theme is ...

    >>> theme = FreshAndShiny()
    >>> theme.getColor('main').hex
    '7A7D81'
     """
    NAME = 'Fresh and Shiny'
    
    #baseLogo1
    #baseLogo2
    #baseLogo3
    baseMain=spotColor('coolgray11u')
    baseAccent=spotColor('rhodamineredu')
    baseAlt1=spotColor(265)
    baseAlt2=spotColor(3005)
    baseSupport1=spotColor(375) 
    baseSupport2=spotColor('red032u')

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
