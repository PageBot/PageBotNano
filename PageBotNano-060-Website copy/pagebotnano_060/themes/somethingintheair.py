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
    """The SomethingInTheAir theme is ..."""

    NAME = 'Something in the Air'
    BASE_COLORS = dict(
        base0=spotColor('reflexblueu'),
        base1=spotColor(540),
        base2=spotColor(542),
        base3=spotColor(306),
        base4=spotColor(245), # Supporter1
        base5=spotColor(190),
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
