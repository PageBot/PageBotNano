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
sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano_060.themes.backtothecity import BackToTheCity
from pagebotnano_060.themes.businessasusual import BusinessAsUsual
from pagebotnano_060.themes.fairytales import FairyTales
from pagebotnano_060.themes.freshandshiny import FreshAndShiny
from pagebotnano_060.themes.happyholidays import HappyHolidays
from pagebotnano_060.themes.intothewoods import IntoTheWoods
from pagebotnano_060.themes.seasoningthedish import SeasoningTheDish
from pagebotnano_060.themes.somethingintheair import SomethingInTheAir
from pagebotnano_060.themes.wordlywise import WordlyWise

AllThemes = (
    BackToTheCity,
    BusinessAsUsual,
    FairyTales,
    FreshAndShiny,
    HappyHolidays,
    IntoTheWoods,
    SeasoningTheDish,
    SomethingInTheAir,
    WordlyWise,
)
DefaultTheme = HappyHolidays