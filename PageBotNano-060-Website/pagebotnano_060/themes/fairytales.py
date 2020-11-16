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
#   fairytales.py
#
import sys
sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano_060.themes.theme import BaseTheme
from pagebotnano_060.toolbox.color import spotColor

class FairyTales(BaseTheme):
    """The FairyTales theme is ..."""

    NAME = 'Fairy Tales'
    THEME_COLORS = dict(
        #logo1
        #logo2
        #logo3
        main=spotColor(425),
        accent=spotColor(237),
        alt1=spotColor(278),
        alt2=spotColor(373),
        support1=spotColor(422),
        support2=spotColor(473),
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
