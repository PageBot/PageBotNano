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

from pagebotnano_020.themes.theme import BaseTheme
from pagebotnano_020.toolbox.color import spotColor

class SeasoningTheDish(BaseTheme):
    """The SeasoningTheDish theme is ..."""

    NAME = 'Seasoning the Dish'
    THEME_COLORS = dict(
        #logo1
        #logo2
        #logo3
        main=spotColor(412),
        accent=spotColor(214),
        alt1=spotColor(369),
        alt2=spotColor(389),
        support1=spotColor(401), 
        support2=spotColor(103),
    )
    BASE_TYPE = dict(
        familyName='Georgia',
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
