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

from pagebotnano.themes.backtothecity import BackToTheCity
from pagebotnano.themes.businessasusual import BusinessAsUsual
from pagebotnano.themes.fairytales import FairyTales
from pagebotnano.themes.freshandshiny import FreshAndShiny
from pagebotnano.themes.happyholidays import HappyHolidays
from pagebotnano.themes.intothewoods import IntoTheWoods
from pagebotnano.themes.seasoningthedish import SeasoningTheDish
from pagebotnano.themes.somethingintheair import SomethingInTheAir
from pagebotnano.themes.wordlywise import WordlyWise

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