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
#   MyBooklet.py
#
#   This MyBooklet.py shows an example how to import
#   existing libaries, that contain knowledge about a publication,
#   document, pages and the elements on the pages.
#
from pagebotnano.publications.booklet import Booklet
from pagebotnano.toolbox.typesetter import Typesetter
from pagebotnano.toolbox import mm
from pagebotnano.templates.onecolumn import OneColumnTemplates 
from pagebotnano.themes import *
from pagebotnano.constants import DARK, LIGHT

w, h = mm(130), mm(210) # Nice little booklet

# Select a theme for colors and typographic styles.
#theme = HappyHolidays(LIGHT)
theme = BusinessAsUsual(LIGHT)

contentPath = '../resources/PublishingVariables.md'

# Create the typesetter that will do content parsing into a “Galley”
ts = Typesetter()
# Do the typesetting. Galley is now another type of element
# that contains text and image elements in the sequence of the markdown.
galley = ts.typesetFile(contentPath, theme.styles)

# Create the Booklet publication and feed it with the processed galley content.
booklet = Booklet(w=w, h=h, theme=theme, galley=galley, 
    templates=OneColumnTemplates())

booklet.export('_export/MyBooklet.pdf')

print('Done')