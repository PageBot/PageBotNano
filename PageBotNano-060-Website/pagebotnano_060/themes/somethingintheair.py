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
#   somethingintheair.py
#
import sys
sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano_060.themes.theme import BaseTheme
from pagebotnano_060.toolbox.color import spotColor

class SomethingInTheAir(BaseTheme):
    """The SomethingInTheAir theme is ...

    >>> theme = SomethingInTheAir()
    >>> theme.getColor('main').hex
    '000000'
    """

    NAME = 'Something in the Air'
    
    #baseLogo1
    #baseLogo2
    #baseLogo3
    baseMain=spotColor('reflexblueu')
    baseAccent=spotColor(540)
    baseAlt1=spotColor(542)
    baseAlt2=spotColor(306)
    baseSupport1=spotColor(245)
    baseSupport2=spotColor(190)

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
