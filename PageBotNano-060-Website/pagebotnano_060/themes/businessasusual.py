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
#   businesasusual.py
#
import sys
sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano_060.themes.theme import BaseTheme
from pagebotnano_060.toolbox.color import spotColor

class BusinessAsUsual(BaseTheme):
    """The BusinessAsUsual theme is a generic “woody cool gray” theme, with settings that
    can be used in environments when functionality is more important than “arty”
    appearance."""

    NAME = 'Business as Usual'
    THEME_COLORS = dict(
        #logo1
        #logo2
        #logo3
        main=spotColor('blacku'),
        accent=spotColor(404),
        alt1=spotColor(541),
        alt2=spotColor(542),
        support1=spotColor(139), 
        support2=spotColor(877),
    )

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
