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

if __name__ == "__main__":
    sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano_010.themes.backtothecity import BackToTheCity
from pagebotnano_010.themes.businessasusual import BusinessAsUsual
from pagebotnano_010.themes.fairytales import FairyTales
from pagebotnano_010.themes.freshandshiny import FreshAndShiny
from pagebotnano_010.themes.happyholidays import HappyHolidays
from pagebotnano_010.themes.intothewoods import IntoTheWoods
from pagebotnano_010.themes.seasoningthedish import SeasoningTheDish
from pagebotnano_010.themes.somethingintheair import SomethingInTheAir
from pagebotnano_010.themes.wordlywise import WordlyWise

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