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

if __name__ == "__main__":
    sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano_010.themes.theme import BaseTheme
from pagebotnano_010.toolbox.color import spotColor

class SeasoningTheDish(BaseTheme):
    """The SeasoningTheDish theme is ..."""

    NAME = 'Seasoning the Dish'
    BASE_COLORS = dict(
        base0=spotColor(412),
        base1=spotColor(214),
        base2=spotColor(369),
        base3=spotColor(389),
        base4=spotColor(401), # Supporter1
        base5=spotColor(103),
    )
    BASE_TYPE = dict(
        familyName='Georgia',
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
