
# Generate tab figures from figures
import os
from pagebotnano_025 import openFont, copyGlyph

FIGURES = ('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'zero')
PATH = 'masters/'

for fileName in os.listdir(PATH):
	if fileName.startswith('.'):
		continue
	font = openFont(PATH+fileName)
	print('Checking', font.path)
	for gName in FIGURES:
		if gName in font:
			tabName = gName + '.tab'
			if tabName in font:
				font.removeGlyph(tabName)
				print('Deleting tab figure', tabName)
	font.save()
	font.close() # Does not do anything in this script.

print('Done')


