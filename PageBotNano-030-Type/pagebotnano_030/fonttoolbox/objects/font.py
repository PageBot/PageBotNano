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
#   font.py
#
#   Implements a PageBotNano font style to get info from a TTFont. Using the
#   Font / Glyph classes, allows page layout in PageBotNano to access
#   all information in a font with the purpose of typography and layout.
#
#   We will call this class "Font" instead of "Style" , to avoid confusion
#   with the PageBotNano style dictionary, which hold style parameters.
#
import sys
from random import random
sys.path.insert(0, "../../../") # So we can import pagebotnano without installing.

import os

# We assume that fontTools is installed (as it is inside the DrawBotApp)
from fontTools.ttLib import TTFont, TTLibError
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates

from pagebotnano_030.constants import *
from pagebotnano_030.fonttoolbox.objects.glyph import Glyph
from pagebotnano_030.fonttoolbox.objects.fontinfo import FontInfo
from pagebotnano_030.fonttoolbox.analyzers.fontanalyzer import FontAnalyzer
from pagebotnano_030.toolbox.transformer import path2Extension, path2FontName
from pagebotnano_030.contributions.adobe.kerndump.getKerningPairsFromOTF import OTFKernReader

def findFont(name):
    """

    >>> findFont('Georgia').endswith('/Fonts/Georgia')
    True
    """
    fontPaths = ('~/Library/Fonts/', '/Library/Fonts/')
    for fontPath in fontPaths:
        fontPath = os.path.expanduser(fontPath)
        print(fontPath)
        for fileName in os.listdir(fontPath):
            if fileName.startswith('.'):
                continue
            print(fontPath, fileName)
            if name in fileName:
                return fontPath + fileName
    return None

class Font:
    """Storage of font information while composing the pages.

    >>> fontPath = '../../../../resources/fonts/typetr/PageBot-Bold.ttf'
    >>> f = Font(fontPath)
    >>> f.info.familyName
    'PageBot'
    >>> len(f)
    93
    >>> f.features
    {}
    >>> f.groups

    >>> f.designSpace
    {}
    """
    GLYPH_CLASS = Glyph
    FONTANALYZER_CLASS = FontAnalyzer

    def __init__(self, path=None, ttFont=None, name=None, opticalSize=None,
            location=None, styleName=None, lazy=True):
        """Initialize the TTFont, for which Font is a wrapper. self.name is
        supported, in case the caller wants to use a different

        >>> path = '../../../../resources/fonts/typetr/PageBot-Bold.ttf'
        >>> Font(path)
        <Font PageBot-Bold>
        >>> Font()
        <Font Untitled Untitled>
        """

        if path is None and ttFont is None:
            self.ttFont = TTFont()
            self.path = '%d' % id(ttFont) # In case no path, use unique id instead.
        elif ttFont is None and path is not None:
            self.ttFont = TTFont(path, lazy=lazy)
            self.path = path # File path of the existing font file.
        elif path is None:
            self.ttFont = ttFont
            self.path = '%d' % id(ttFont) # In case no path, use unique id instead.
        else: # ttFont is not None: There is ttFont data
            self.ttFont = ttFont
            self.path = path

        # Store location, in case this was a created VF instance
        self.location = location
        # TTFont is available as lazy style.info.font
        self.info = FontInfo(self.ttFont)
        self.info.opticalSize = opticalSize # Optional optical size, to indicate where this Variable Font is rendered for.
        self.info.location = location # Store origina location of this instance of the font is derived from a Variable Font.
        # Stores optional custom name, otherwise use original DrawBot name.
        # Otherwise use from FontInfo.fullName
        self.name = name or self.info.fullName
        if styleName is not None:
            self.info.styleName = styleName # Overwrite default style name in the ttFont or Variable Font location
        self._kerning = None # Lazy reading.
        self._groups = None # Lazy reading.
        self._glyphs = {} # Lazy creation of self[glyphName]
        self._analyzer = None # Lazy creation.
        self._variables = None # Lazy creations of delta's dictionary per glyph per axis

    def __repr__(self):
        """
        >>> path = '../../../../resources/fonts/typetr/PageBot-Bold.ttf'
        >>> f = Font(path)
        >>> str(f)
        '<Font PageBot-Bold>'
        """
        return '<Font %s>' % (path2FontName(self.path) or self.name or 'Untitled').strip()

    def __getitem__(self, glyphName):
        """Answers the glyph with glyphName, making the font behave as dictionary of glyphs.

        >>> path = '../../../../resources/fonts/typetr/PageBot-Bold.ttf'
        >>> f = Font(path)
        >>> g = f['A']
        >>> g.name, g.width
        ('A', 722)
        """
        if not glyphName in self._glyphs:
            self._glyphs[glyphName] = self.GLYPH_CLASS(self, glyphName)
        return self._glyphs[glyphName]

    def __len__(self):
        """Answers the number of glyphs in the font.

        >>> path = '../../../../resources/fonts/typetr/PageBot-Bold.ttf'
        >>> f = Font(path)
        >>> len(f) # Number of glyphs
        93
        """
        if 'glyf' in self.ttFont:
            return len(self.ttFont['glyf'])
        return 0

    def __eq__(self, font):
        """Answer the boolean flag if `self` and `font` match family name and style name or path

        >>> path = '../../../../resources/fonts/typetr/PageBot-Bold.ttf'
        >>> f1 = Font(path)
        >>> f2 = Font(path)
        >>> f1 == f2
        True
        >>> path = '../../../../resources/fonts/typetr/PageBot-Regular.ttf'
        >>> f3 = Font(path)
        >>> f1 == f3
        False
        """
        if isinstance(font, self.__class__):
            return self.info.familyName == font.info.familyName and self.info.styleName == font.info.styleName
        return False

    def __ne__(self, font):
        """Answer the boolean flag if `self` and `font` match family name and style name or path

        >>> path = '../../../../resources/fonts/typetr/PageBot-Bold.ttf'
        >>> f1 = Font(path)
        >>> f2 = Font(path)
        >>> f1 != f2
        False
        >>> path = '../../../../resources/fonts/typetr/PageBot-Regular.ttf'
        >>> f3 = Font(path)
        >>> f1 != f3
        True
        """
        if not isinstance(font, self.__class__):
            return True
        if self.path == font.path:
            return False
        return self.info.familyName != font.info.familyName or self.info.styleName != font.info.styleName

    def nameMatch(self, pattern):
        """Answers level of matching between pattern and the font file name or
        font.info.fullName. Pattern can be a single string or a list of
        string.

        >>> path = '../../../../resources/fonts/typetr/PageBot-Bold.ttf'
        >>> f = Font(path)
        >>> f.nameMatch('Bold')
        1.0
        >>> f.nameMatch('Blackish')
        0
        >>> f.nameMatch(('PageBot', 'Bold'))
        1.0
        """
        fontName = path2FontName(self.path)
        if not isinstance(pattern, (list, tuple)):
            pattern = [pattern]
        for part in pattern:
            if not part in fontName:# or part in self.info.fullName):
                return 0
        return 1.0

    def isItalic(self):
        """Answers if this font should be considered italic. Currently
        there is only no-match (0) and full-match (1). 

        >>> path = '../../../../resources/fonts/typetr/PageBot-Bold_Italic.ttf'
        >>> f = Font(path)
        >>> f.isItalic()
        1
        >>> path = '../../../../resources/fonts/typetr/PageBot-Bold.ttf'
        >>> f = Font(path)
        >>> f.isItalic()
        0
        """
        if self.info.italicAngle: # And angle != 0
            return 1
        return 0

    def getItalicAngle(self):
        return self.info.italicAngle
    italicAngle = property(getItalicAngle)

    def keys(self):
        """Answers the glyph names of the font.

        >>> path = '../../../../resources/fonts/typetr/PageBot-Bold.ttf'
        >>> f = Font(path, lazy=False)
        >>> 'A' in f.keys()
        True
        """
        if 'glyf' in self.ttFont:
            return self.ttFont['glyf'].keys()
        return []

    def _get_cmap(self):
        """Answers the dictionary of sorted {unicode: glyphName, ...} in the
        font.

        >>> from pagebot.fonttoolbox.objects.font import Font
        >>> path = '../../../../resources/fonts/typetr/PageBot-Bold.ttf'
        >>> f = Font(path)
        >>> f.cmap[65]
        'A'
        >>> f.cmap.keys()[70:90]

        """
        if 'cmap' in self.ttFont:
            return self.ttFont['cmap'].getBestCmap()
        return {}
    cmap = property(_get_cmap)

    def __contains__(self, glyphName):
        """Allow direct testing.

        >>> path = '../../../../resources/fonts/typetr/PageBot-Bold.ttf'
        >>> f = Font(path)
        >>> 'A' in f
        True
        """
        return glyphName in self.keys()

    def _get_analyzer(self):
        """Answers the style / font analyzer if it exists. Otherwise create
        one.

        >>> path = '../../../../resources/fonts/typetr/PageBot-Bold.ttf'
        >>> f = Font(path)
        >>> f.analyzer
        <Analyzer of PageBot Bold>
        """
        if self._analyzer is None:
            self._analyzer = self.FONTANALYZER_CLASS(self)
        return self._analyzer
    analyzer = property(_get_analyzer)

    def _get_axes(self):
        """Answers dictionary of axes if self.ttFont is a Variable Font.
        Otherwise answer an empty dictioary.

        >>> path = '../../../../resources/fonts/typetr/PageBot-Bold.ttf'
        >>> f = Font(path)
        >>> f.axes.get('opsz') is None
        True
        """
        try:
            # TODO: Change value to Axis dictionary instead of list
            axes = {a.axisTag: (a.minValue, a.defaultValue, a.maxValue) for a in self.ttFont['fvar'].axes}
        except KeyError:
            axes = {} # This is not a variable font.
        return axes
    axes = property(_get_axes)

    def getDefaultVarLocation(self):
        """Answers the location dictionary with the default axes values.

        >>> path = '../../../../resources/fonts/typetr/PageBot-Bold.ttf'
        >>> f = Font(path)
        >>> len(f.getDefaultVarLocation().keys())
        0
        """
        defaultVarLocation = {}
        for axisName, axis in self.axes.items():
            defaultVarLocation[axisName] = axis[1]
        return defaultVarLocation

    def _get_rawDeltas(self):
        """Answers the list of axis dictionaries with deltas for all glyphs and
        axes. Answer an empty dictionary if the [gvar] table does not exist.

        >>> path = '../../../../resources/fonts/typetr/PageBot-Bold.ttf'
        >>> f = Font(path)
        >>> f.rawDeltas
        {}
        """
        try:
            return self.ttFont['gvar'].variations
        except:
            return {}
    rawDeltas = property(_get_rawDeltas)

    def _get_designSpace(self):
        """Answers the design space in case this is a variable font.

        >>> path = '../../../../resources/fonts/typetr/PageBot-Bold.ttf'
        >>> f = Font(path)
        >>> f.designSpace # Basically the "cvar" table.
        {}
        """
        try:
            designSpace = self.ttFont['cvar']
        except KeyError:
            designSpace = {}
        return designSpace
    designSpace = property(_get_designSpace)

    def _get_variables(self):
        """Answers the gvar-table (if it exists) translated into plain Python
        dictionaries of deltas per glyph and per axis if this is a Var-fonts.
        Otherwise answer an empty dictionary

        >>> path = '../../../../resources/fonts/typetr/PageBot-Bold.ttf'
        >>> f = Font(path)

        """
        """
        TODO We need a "stable" var-font to test on.

        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> font = findFont('Amstelvar-Roman-VF')
        >>> len(font.variables)
        592
        >>> variables = font.variables['H']
        >>> sorted(variables.keys())
        []
        >>> #['GRAD', 'XOPQ', 'XTRA', 'YOPQ', 'YTRA', 'YTSE', 'YTUC', 'opsz', 'wdth', 'wght']
        >>> axis, deltas = variables['GRAD']
        >>> axis
        {'GRAD': (0.0, 1.0, 1.0)}
        >>> deltas[:6]
        [(0, 0), None, (52, 0), None, None, (89, 0)]
        >>> font.variables.get('wrongglyphName') is None
        True
        """
        if self._variables is None:
            try:
                # Get the raw fonttools gvar table if it exists.
                gvar = self.ttFont['gvar']
                self._variables = {}
                for glyphName, tupleVariations in gvar.variations.items():
                    self._variables[glyphName] = axisDeltas = {}
                    for tupleVariation in tupleVariations:
                        #{'GRAD': (0.0, 1.0, 1.0)} Make unique key, in case multiple
                        axisKey = '_'.join(tupleVariation.axes.keys())
                        # ({'GRAD': (0.0, 1.0, 1.0)}, [(0, 0), None, (52, 0), None, None, (89, 0), ...])
                        axisDeltas[axisKey] = tupleVariation.axes, tupleVariation.coordinates
            except KeyError:
                pass # No gvar table, just answer the current self._variables as None.
        return self._variables
    variables = property(_get_variables)

    def getInstance(self, location=None, dstPath=None, opticalSize=None,
            styleName=None, cached=True, lazy=True, kerning=None):
        """Answers the instance of self at location. If the cache file already
        exists, then just answer a Font instance to that font file.

        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> f = findFont('RobotoDelta-VF')
        >>> sorted(f.axes.keys())
        ['GRAD', 'POPS', 'PWDT', 'PWGT', 'UDLN', 'XOPQ', 'XTRA', 'YOPQ', 'YTAD', 'YTAS', 'YTDD', 'YTDE', 'YTLC', 'YTRA', 'YTUC', 'opsz', 'wdth', 'wght']
        >>> f.name
        'RobotoDelta VF'
        >>> len(f)
        188
        >>> f.axes['wght']
        (100.0, 400.0, 900.0)
        >>> g = f['H']
        >>> g
        <Glyph 'H' (Pts:12, Cnt:1, Cmp:0)>
        >>> g.points[6], g.width
        (APoint(1288,1456,On), 1458)
        >>> instance = f.getInstance(location=dict(wght=500))
        >>> instance
        <Font RobotoDelta-VF-wght500>
        >>> ig = instance['H']
        >>> ig
        <Glyph 'H' (Pts:12, Cnt:1, Cmp:0)>
        >>> ig.points[6], ig.width
        (APoint(1307,1456,On), 1477)
        """
        if location is None:
            location = self.getDefaultVarLocation()
        return getInstance(self.path, location=location, dstPath=dstPath, opticalSize=opticalSize,
            styleName=styleName, cached=cached, lazy=lazy, kerning=kerning)

    def _get_cmap(self):
        """Answer the best cmap for this font

        >>> path = '../../../../resources/fonts/typetr/PageBot-Bold.ttf'
        >>> f = Font(path)
        >>> cmap = f.cmap
        >>> sorted(cmap.items())[0]
        (32, 'space')
        >>> len(cmap)
        94
        """
        if self.ttFont is not None:
            return self.ttFont.getBestCmap()
        return None
    cmap = property(_get_cmap)

    def _get_features(self):
        # TODO: Use TTFont for this instead.
        #return context.listOpenTypeFeatures(self.path)
        return {}
    features = property(_get_features)

    def _get_kerning(self):
        """Answers the (expanded) kerning table of the font.

        >>> path = '../../../../resources/fonts/typetr/PageBot-Bold.ttf'
        >>> f = Font(path)
        >>> len(f.kerning)
        1602
        >>> f.kerning[('V','a')]
        -69
        """
        if self._kerning is None: # Lazy read.
            self._kerning = OTFKernReader(self.path).kerningPairs
        return self._kerning
    kerning = property(_get_kerning)

    def _get_groups(self):
        """Answers the groups dictionary of the font. TODO: How to initialize?

        >>> path = '../../../../resources/fonts/typetr/PageBot-Bold.ttf'
        >>> f = Font(path)
        >>> f.groups is None
        True
        """
        return self._groups
    groups = property(_get_groups)

    def save(self, path=None):
        """Save the font to optional path or to self.path."""
        self.ttFont.save(path or self.path)

    def getAscender(self): # DrawBot compatible
        """Answer the ascender value in em-units from [hhea] table, as used by browsers.

        >>> path = '../../../../resources/fonts/typetr/PageBot-Bold.ttf'
        >>> f = Font(path)
        >>> f.getAscender()
        898
        >>> f.ascender # Also available as property
        898
        """
        return self.info.ascender # From self.ttFont['hhea'] table
    ascender = property(getAscender)

    def getDescender(self): # DrawBot compatible
        """Answer the descender value in em-units from [hhea] table, as used by browsers.

        >>> path = '../../../../resources/fonts/typetr/PageBot-Bold.ttf'
        >>> f = Font(path)
        >>> f.getDescender()
        -302
        >>> f.descender # Also available as property
        -302
        """
        return self.info.descender # From self.ttFont['hhea'] table
    descender = property(getDescender)

    def getUpem(self): # DrawBot compatible
        """Answer the self.info.unitsPerEm value in em-units from [hhea] table, as used by browsers.

        >>> path = '../../../../resources/fonts/typetr/PageBot-Bold.ttf'
        >>> f = Font(path)
        >>> f.getUpem()
        1000
        >>> f.unitsPerEm
        1000
        >>> f.upem
        1000
        """
        return self.info.unitsPerEm
    upem = unitsPerEm = property(getUpem)

    def getXHeight(self):
        """Answer the self.info.xHeight value in em-units from [OS/2] table, as used by browsers.

        >>> path = '../../../../resources/fonts/typetr/PageBot-Bold.ttf'
        >>> f = Font(path)
        >>> f.getXHeight()
        474
        >>> f.xHeight # Also available as property
        474
        """
        table = self.ttFont['OS/2']
        return getattr(table, 'sxHeight', None)
    xHeight = property(getXHeight)

    def getCapHeight(self):
        """Answer the self.info.capHeight value in em-units from [OS/2] table, as used by browsers.

        >>> path = '../../../../resources/fonts/typetr/PageBot-Bold.ttf'
        >>> f = Font(path)
        >>> f.getCapHeight()
        658
        >>> f.capHeight # Also available as property
        658
        """
        table = self.ttFont['OS/2']
        return getattr(table, 'sCapHeight', None)

    capHeight = property(getCapHeight)


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
