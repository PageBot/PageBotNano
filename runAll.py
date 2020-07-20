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

VERBOSE = False # If True, show all file name as they are tested.

def testPath(path, level=0):
    os.chdir(path)
    for fileName in sorted(os.listdir('.')):
        if fileName.startswith('.') or fileName.startswith('_'):
            continue

        if os.path.isdir(fileName):
            testPath(fileName, level+1)
        elif fileName.endswith('.py'):
            if VERBOSE:
                print('... %s %s/%s' % ('\t'*level, path, fileName))
            # Not using exec(open(fileName).read())
            # to get a "clean" python sys path.
            os.system('python3 ' + fileName)
    os.chdir('..')

# Versions that pass the doc tests
MAIN_VERSION = [0]
RUNNING_VERSIONS = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# Version under development
DEVELOPMENT_VERSIONS = [10, 20, 30, 40, 50]
# Versions to test
TEST_VERSIONS = RUNNING_VERSIONS
TEST_VERSIONS = [5]

for fileName in sorted(os.listdir('.')):
    if not os.path.isdir(fileName) or fileName.startswith('.'):
        continue
    if fileName == 'PageBotNano':
        version = 0
    elif fileName.startswith('PageBotNano'):
        version = int(fileName.split('-')[1])
    if version in TEST_VERSIONS:
        testPath(fileName)

print('Done running %s test(s)' % len(TEST_VERSIONS))
