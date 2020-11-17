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
#   seasoningthedish.py
#
import sys
sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano_060.themes.theme import BaseTheme
from pagebotnano_060.toolbox.color import spotColor

class SeasoningTheDish(BaseTheme):
    """The SeasoningTheDish theme is ...

    >>> theme = SeasoningTheDish()
    >>> theme.getColor('main').hex
    '3D3028'
    """

    NAME = 'Seasoning the Dish'
   
    #baseLogo1
    #baseLogo2
    #baseLogo3
    baseMain=spotColor(412)
    baseAccent=spotColor(214)
    baseAlt1=spotColor(369)
    baseAlt2=spotColor(389)
    baseSupport1=spotColor(401)
    baseSupport2=spotColor(103)

    BASE_TYPE = dict(
        familyName='Georgia',
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
