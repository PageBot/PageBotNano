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
    """The HappyHolidays is ...

    >>> theme = HappyHolidays()
    >>> theme.getColor('main').hex
    'FF0033'
    """
    NAME = 'Happy Holidays'

    # Example logo colors, to be modified by an inheriting class.
    baseLogo1=color(1, 0, 0)
    #baseLogo2
    #baseLogo3
    baseMain=color(1, 0, 0.2)
    baseAccent=color(0.7, 0.1, 0.2)
    baseAlt1=color(0.9, 0, 0.3)
    baseAlt2=color(0.5, 0.96, 0.2)
    baseSupport1=color(0, 1, 0)
    baseSupport2=color(0.55, 0.5, 0.5)

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
