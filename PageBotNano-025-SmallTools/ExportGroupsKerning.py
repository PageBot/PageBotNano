
import os, codecs
from pagebotnano_025 import openFont

TAB_WIDTH = 630

PATH = 'masters/'
EXPORT = 'scripts/'

INIT_OPEN = """#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import sys
if __name__ == "__main__":
   sys.path.insert(0, "../")
from pagebotnano_025 import openFont
font = openFont("../%s") """

def getGroupsSource(f):
    code = [INIT_OPEN % f.path]
    return '\n'.join(code)

def getKerningSource(f):
    code = [INIT_OPEN % f.path]
    return '\n'.join(code)

def writeFile(path, code):
    f = codecs.open(path, 'w', encoding='utf-8')
    f.write(code)
    f.close()

if not os.path.exists(EXPORT):
    print('Creating', EXPORT)
    os.makedirs(EXPORT)

for fileName in os.listdir(PATH):
    if fileName.startswith('.') or not fileName.endswith('.ufo'):
        continue
    font = openFont(PATH+fileName)
    print('Checking', font.path, 'Groups', len(font.groups), 'Kerning', len(font.kerning))

    groupsPath = EXPORT + fileName.replace('.ufo', '.groups.py')
    writeFile(groupsPath, getGroupsSource(font))

    kerningPath = EXPORT + fileName.replace('.ufo', '.kerning.py')
    writeFile(kerningPath, getKerningSource(font))

    font.save()
    font.close() # Does not do+anything in this script.

print('Done')

