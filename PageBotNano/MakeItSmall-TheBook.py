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
#	This script shows the relative simple process of creating a book.
#   All difficult stuff is hidden in classes like the context, the theme,
#   the templates and the typesetter. 
#   The content markdown file also directs the selection of template pages.
#
import sys
sys.path.insert(0, "../") # So we can import pagebotnano without installing.

from pagebotnano.toolbox.units import pt, mm
from pagebotnano.constants import PENGUIN_POCKET
from pagebotnano.publications.book import Book
from pagebotnano.contexts.drawbot.context import DrawBotContext
from pagebotnano.themes import SeasoningTheDish
from pagebotnano.toolbox.typesetter import Typesetter
from pagebotnano.templates.onecolumn import OneColumnTemplates

MARKDOWN_PATH = 'MakeItSmall-TheBook.md'
#MARKDOWN_PATH = 'Test.md'

W, H = PENGUIN_POCKET

context = DrawBotContext()

# Choose and create a theme. This includes all color and typographic styles.
# Details of the theme can be changed in a later stage.
theme = SeasoningTheDish()

# Use the template class to generate pages and context,
# based on a selection indicated by markers in the markdown file.
# Those have a format like ==cover== and ==page==
templates = OneColumnTemplates()

# Create a publication, that includes the document and pages
# to be filled.
book = Book(w=W, h=H, theme=theme, templates=templates, context=context)

# Typeset the markdown file into a “galley”, a rolled up stack of
# all elements in the file, divided by markers and XML tags.
# Part of the elements is to be placed on the pages as elements,
# (such as TextBox and Image) and part is just instructions for the composer
# as non-displaying Marker elements.
ts = Typesetter()
galley = ts.typesetFile(MARKDOWN_PATH)
"""
print('XML ' + '-'*50)
print(ts.xml)
print('XML ' + '-'*50)
print(galley.elements)
print('XML ' + '-'*50)
"""
# Now let the publication compose itself, using the galley as a
# list of content and composing instructions.
book.compose(galley)

book.export('_export/TheBook.pdf')

