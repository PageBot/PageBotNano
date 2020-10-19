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
#   This source makes it possible to import other sources
#   from this directory/folder
#
#   Try two types of import, so we don't need to install the pagebotnano 
#   package into the Python of your system.
import os, shutil

def isRoboFont():
    try:
        from mojo.roboFont import AllFonts, OpenFont
        return True
    except ModuleNotFoundError: # Not in RoboFont
        pass
    return False

def openFont(nameOrPath, showUI=False):
    """
    Open a font defined by the name of path. If the font is already open
    in RoboFont, then answer.
    """
    if isRoboFont():
        from mojo.roboFont import AllFonts, OpenFont
        for f in AllFonts():
            if nameOrPath == f.info.familyName or f.path.endswith(nameOrPath):
                return f
        assert os.path.exists(nameOrPath)
        return OpenFont(nameOrPath, showUI=showUI)
    # Else not in RoboFont, use plain fontParts instead
    from fontParts.fontshell.font import RFont
    #print('RFONT', nameOrPath) 
    return RFont(nameOrPath, showInterface=showUI)

def copyGlyph(srcFont, glyphName, dstFont, dstGlyphName=None):
    assert glyphName in srcFont, ('Glyph "%s" does not exist source font "%s"' % (glyphName, srcFont.path))
    if dstGlyphName is None:
        dstGlyphName = glyphName
    srcGlyph = srcFont[glyphName]
    if not dstGlyphName in dstFont:
        dstFont.newGlyph(dstGlyphName)
    dstGlyph = dstFont[dstGlyphName]
    dstGlyph.clear()
    for srcLayerGlyph in srcGlyph.layers:
        dstLayerGlyph = dstGlyph.getLayer(srcLayerGlyph.layerName)
        pen = dstLayerGlyph.getPen()
        srcLayerGlyph.draw(pen)
        dstLayerGlyph.width = srcLayerGlyph.width
    return dstGlyph

def copyLayer(glyph, srcLayer, dstLayer):
    srcLayerGlyph = glyph.getLayer(srcLayer)
    dstLayerGlyph = glyph.newLayer(dstLayer)
    dstLayerGlyph.clear()
    pen = dstLayerGlyph.getPen()
    srcLayerGlyph.draw(pen)
    dstLayerGlyph.width = srcLayerGlyph.width

def removeLayer(glyph, layer):
    if layer != 'public.default':
        glyph.removeLayer(layer)

def getComponentNames(g, nameSet=None, createMissing=True):
    """Answer all recursive component names that g refers to."""
    if nameSet is None:
        nameSet = set()
    f = g.getParent()
    nameSet.add(g.name)
    for component in g.components:
        if component.baseGlyph not in f:
            baseGlyph = f.newGlyph(component.baseGlyph)
        else:
            baseGlyph = f[component.baseGlyph]
        nameSet.add(baseGlyph.name)
        getComponentNames(baseGlyph, nameSet)
    return nameSet

def glyphSet2NameSet(f, glyphSet, skipExtensions=None):
    """Converts all unicode chars in glyphSet (string, set, list, tuple, dict) to
    their glyph name in the font and answer that as set. If the unicode char
    matches the glyph name, then add it too.
    If the skipExtensions list is test, then also skip glyphs that have those
    extensions.
    """
    if skipExtensions is None:
        skipExtensions = ('sc',)
    nameSet = set()
    for g in f:
        gName = g.name
        nameParts = gName.split('.')
        baseName = nameParts[0]
        if len(nameParts) > 1:
            extension = '.'.join(nameParts[1:])
        else:
            extension = None
        if extension and extension in skipExtensions:
            continue
        if baseName in f:
            baseGlyph = f[baseName]
            if (baseGlyph.unicode and chr(baseGlyph.unicode) in glyphSet) or baseName in glyphSet:
                nameSet.add(g.name)
                nameSet.add(baseName)
        elif (g.unicode and chr(g.unicode) in glyphSet) or gName in glyphSet:
            nameSet.add(g.name)
    return nameSet
  
               
def getComponentNameSet(f, nameSet):
    for glyphName in sorted(nameSet):
        if glyphName in f:
            g = f[glyphName]
            getComponentNames(g, nameSet)
        else:
            print('[getComponentNameSet] Missing glyph', glyphName, f)
    return nameSet

# U F O  F I L E S

def deleteUFOs(dirPath):
    """Delete all .ufo files (actually directories) in dirPath.
    Ufo files in deeper paths are ignored. Answer a list of files
    that were deleted.
    """
    deletedFiles = []
    if not dirPath.endswith('/'):
        dirPath += '/'
    for fileName in os.listdir(dirPath):
        if fileName.lower().endswith('.ufo'):
            shutil.rmtree(dirPath + fileName)
            deletedFiles.append(fileName)
    return deletedFiles

def deleteUFO(path):
    assert path.endswith('.ufo')
    if os.path.exists(path):
        shutil.rmtree(path)

def copyUFO(srcPath, dstPath):
    """Copy the UFO in srcPath to dstPath (directory or UFO name).
    Make sure they are not equal and that the srcPath indeed is 
    has a ufo extension.
    """
    assert os.path.exists(srcPath) and srcPath.endswith('.ufo'), ('Wrong source path %s' % srcPath)
    if os.path.exists(dstPath):
        assert os.path.isdir(dstPath) or dstPath.endswith('.ufo'), ('Wrong existing destination path %s' % dstPath)
    else:
        assert dstPath.endswith('.ufo'), ('Wrong destination path %s' % dstPath)
    shutil.copytree(srcPath, dstPath)

def copyUFOs(srcDirPath, dstDirPath):
    """Copy all UFO's in the srcDirPath to dstDirPath.
    """
    if not srcDirPath.endswith('/'):
        srcDirPath += '/'
    if not dstDirPath.endswith('/'):
        dstDirPath += '/'
    assert os.path.isdir(srcDirPath)
    copiedFiles = []
    for fileName in os.listdir(srcDirPath):
        if fileName.endswith('.ufo'):
            shutil.copytree(srcDirPath + fileName, dstDirPath + fileName)
            copiedFiles.append(fileName)
    return copiedFiles
   
 