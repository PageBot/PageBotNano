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
#   constants.py
#
A4 = 595, 842 # Rounded equivalent in points of 210mm x 297mm
A5 = 421, 595

DEFAULT_WIDTH = 100 # Default width for some of the element types.

# Types of text alignment
LEFT = 'left'
CENTER = 'center'
RIGHT = 'right'
JUSTIFIED = 'justified'

EXPORT_DIR = '_export/' # Name of the directory that does not commit in Github

# Set of names that are allowed as attribute in DrawBot.FormattedString,
# so we can filter from a more generic style description.
# See: https://www.drawbot.com/content/text/formattedString.html
FS_ATTRIBUTES = {
    'txt', 'font', 'fontSize', 'fallbackFont', 'fill', 'cmykFill', 'stroke',
    'cmykStroke', 'strokeWidth', 'align', 'lineHeight', 'tracking', 'baselineShift',
    'openTypeFeatures', 'tabs', 'language', 'indent', 'tailIndent', 
    'firstLineIndent', 'paragraphTopSpacing', 'paragraphBottomSpacing',
}
# This dictionary translate PageBotNano style names into their CSS equivalents.
CSS_ATTRIBUTES = dict(
    font='font-family',
    fontSize='font-size',
    fill='background-color',
)

HTML_TEXT_TAGS = {'h1', 'h2', 'h3', 'h4', 'h5', 'p', 'span', 'b', 'i'}

# Language codes for OSX
EN = 'en' # English
