
# Generate tab figures from figures
import os
from pagebotnano_025 import openFont, copyGlyph

TAB_WIDTH = 630
FIGURES = ('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'zero')
PATH = 'masters/'

for fileName in os.listdir(PATH):
    if fileName.startswith('.'):
        continue
    font = openFont(PATH+fileName)
    print('Checking', font.path)
    for gName in FIGURES:
        if gName in font:
            g = font[gName]
            tabName = gName + '.tab'
            if not tabName in font:
                copyGlyph(font, gName, font, tabName)
                diff = TAB_WIDTH - g.width
                tabGlyph = font[tabName]
                tabGlyph.leftMargin += diff/2 # First set the margin
                tabGlyph.width = TAB_WIDTH # Then set the width
                print('Creating tab figure', tabName, 'on width', TAB_WIDTH)
    font.save()
    font.close() # Does not do anything in this script.

print('Done')


