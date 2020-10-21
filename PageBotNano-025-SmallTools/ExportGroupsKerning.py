
import os, codecs
#from pagebotnano_025 import openFont

def openFont(nameOrPath, showUI=False):
    """
    Open a font defined by the name of path. If the font is already open
    in RoboFont, then answer.
    """
    from fontParts.fontshell.font import RFont
    #print('RFONT', nameOrPath) 
    return RFont(nameOrPath, showInterface=showUI)

# Kerning pair (group1, group2) 
# Kerning pair (group1, glyph2)
# Kerning pair (glyph1, group2)
# Kerning pair (glyph1, glyph2)
# 
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
    code.append('')
    code.append('def g(f, groupName, group):')
    code.append('   f.groups[groupName] = group')
    code.append('')
    
    for groupName, group in f.groups.items():
        code.append('g(font, "%s", %s)' % (groupName, group))
    code.append('')
    code.append('font.save()')
    code.append('font.close()')
    code.append('')
    return '\n'.join(code)

def getKerningSource(f):
    code = [INIT_OPEN % f.path]
    code.append('')
    code.append('def k(f, pair, value):')
    code.append('   f.kerning[pair] = value')
    code.append('')
    
    for pair, value in f.kerning.items():
        code.append('k(font, %s, %s)' % (pair, value))
    code.append('')
    code.append('font.save()')
    code.append('font.close()')
    code.append('')
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

