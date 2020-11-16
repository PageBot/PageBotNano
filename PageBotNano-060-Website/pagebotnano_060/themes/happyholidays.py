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
#   happyholidays.py
#
import sys
sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano_060.themes.theme import BaseTheme
from pagebotnano_060.toolbox.color import color

class HappyHolidays(BaseTheme):
    NAME = 'Happy Holidays'
    THEME_COLORS = dict(
        # Example logo colors, to be modified by an inheriting class.
        logo1=color(1, 0, 0),
        #logo2
        #logo3
        main=color(1, 0, 0.2),
        accent=color(0.7, 0.1, 0.2),
        alt1=color(0.9, 0, 0.3),
        alt2=color(0.5, 0.96, 0.2),
        support1=color(0, 1, 0),
        support2=color(0.55, 0.5, 0.5),
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
