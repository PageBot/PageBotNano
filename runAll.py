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
#   testAll.py
#
#   Run all versions to check for doc-test errors.
#
import os
import sys
import importlib

from random import random
import drawBot

def testPath(path, level=0):
    os.chdir(path)
    for fileName in sorted(os.listdir('.')):
        if fileName.startswith('.') or fileName.startswith('_'):
            continue

        if os.path.isdir(fileName):
            testPath(fileName, level+1)
        elif fileName.endswith('.py'):
            print('... %s %s/ %s' % ('\t'*level, path, fileName))
            # Not using exec(open(fileName).read())
            # to get a "clean" python sys path.
            os.system('python3 ' + fileName)
    os.chdir('..')

RUNNING_VERSIONS = [1, 2, 3, 4, 5, 6, 7, 8, 9]
#RUNNING_VERSIONS = [10]
DEVELOPMENT_VERSIONS = [10, 20, 30, 40, 50]

for fileName in sorted(os.listdir('.')):
    if fileName.startswith('PageBotNano'):
        version = int(fileName.split('-')[1])
        if version in RUNNING_VERSIONS:
            testPath(fileName)

print('Done running tests')