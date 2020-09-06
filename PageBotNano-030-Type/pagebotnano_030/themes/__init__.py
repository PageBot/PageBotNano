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
import sys
sys.path.insert(0, "../..") # So we can import pagebotnano_030 without installing.

from pagebotnano_030.themes.backtothecity import BackToTheCity

AllThemes = (
    BackToTheCity,
)
DefaultTheme = BackToTheCity