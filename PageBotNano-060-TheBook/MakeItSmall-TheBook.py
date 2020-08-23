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
#   MakeItSmall-TheBook.py
#
import sys
sys.path.insert(0, "../") # So we can import pagebotnano without installing.

from pagebotnano_060.toolbox.units import pt, mm
from pagebotnano_060.constants import PENGUIN_POCKET
from pagebotnano_060.publications.book import Book
from pagebotnano_060.contexts.drawbot.context import DrawBotContext

context = DrawBotContext()

W, H = PENGUIN_POCKET
book = Book(w=W, h=H, context=context)
#page = doc.newPage()

#doc.export('_export/060_TheBook.pdf')