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
#   context.py
#
#   The SketchJS Context generates the Sketch-API compatible Javascript
#   that generate one single document, as template for later use.
#   The code is not intended to be maintained as application, it is more
#   like a PostScript file, transferring PageBot generated output to create
#   documents in SketchApp on Javascript-API level.
#   The script is wrapped and saved as SketchApp plugin.
#
#   https://developer.sketch.com/reference/api/#create-a-new-document
#
import os
import sys
sys.path.insert(0, "../../..") # So we can import pagebotnano without installing.

from pagebotnano_040.contexts.sketchjs.builder import SketchJSBuilder
from pagebotnano_040.constants import A4, LEFT, RIGHT, CENTER, JUSTIFIED
from pagebotnano_040.toolbox.color import color, noColor
from pagebotnano_040.toolbox import pt
from pagebotnano_040.babelstring import BabelString

class SketchJSContext:

    '''
    Lib/pagebot/contexts/sketchcontext/sketchcontext.py:254:15: W0631: Using possibly undefined loop variable 'pIndex' (undefined-loop-variable)
    '''

    W, H = A4 # Default size of a document, as SketchApp has infinite canvas.

    # The directory where SketchApp keeps the plugins. Note that it starts with a "~"
    # so that must be inside the local user area.
    PLUGIN_PATH = """~/Library/Application Support/com.bohemiancoding.sketch3/Plugins"""

    def __init__(self, path=None):
        """Constructor of Sketch context.

        >>> from pagebotnano_040.document import Document
        >>> context = SketchJSContext() 
        >>> # Create a PageBot Document instance, reading the Sketch file data as source.
        >>> doc = Document(context=context)
        >>> page = doc.newPage()
        >>> page
        <Page pn=1 w=595 h=842 elements=0>
        >>> doc.context.b.path.endswith('/Plugins')
        True
        """
        super().__init__()
        self.name = self.__class__.__name__
        if path is None:
            path = self.getPluginPath()
        self.b = SketchJSBuilder(path)
        self.setSize()

    def installedFonts(self, patterns=None):
        # TODO: share with Flat context.
        pass

    def setStyles(self, styles):
        pass

    def newPath(self):
        pass

    def rect(self, x, y, w, h):
        self.b.rect(x, y, w, h)

    def text(self, bs, p):
        pass

    def getTextLines(self, bs, w=None, h=None):
        pass

    def textSize(self, bs, w=None, h=None):
        pass

    def textOverflow(self, bsOrFs, box, align=None):
        pass

    def textBox(self, fs, r=None, clipPath=None, align=None):
        pass

    def getDrawing(self):
        pass

    def installFont(self, fontOrName):
        """Should install the font in the context. fontOrName can be a Font
        instance (in which case the path is used) or a full font path."""

    def uninstallFont(self, fontOrName):
        pass

    def fontContainsCharacters(self, characters):
        pass

    def fontContainsGlyph(self, glyphName):
        pass

    def fontFilePath(self):
        pass

    def listFontGlyphNames(self):
        pass

    def endDrawing(self, doc=None):
        pass

    def fontAscender(self):
        pass

    def fontDescender(self):
        pass

    def fontXHeight(self):
        pass

    def fontCapHeight(self):
        pass

    def fontLeading(self):
        pass

    def fontLineHeight(self):
        pass

    def setSize(self, w=None, h=None):
        """Optional default document size. If not None, overwriting the size of the
        open Sketch document.

        >>> context = SketchJSContext()
        >>> context.w, context.h

        >>> context.setSize(w=300)
        >>> context.w
        300pt
        """
        self.w = w or A4[0]
        self.h = h or A4[1]

    def setPath(self, path):
        """Set the self.b builder to SketchBuilder(path), answering self.b.sketchApi.

        >>> context = SketchJSContext()
        >>> context.setPath('_export/Demo.sketchplugin')
        >>> context.b.path
        """
        self.b.path = path

    def getPluginPath(self):
        """Answer the path where the plugin can be saved. Answer None if the
        the directory cannot be found, e.g. because SketchApp is not installend.

        >>> context = SketchJSContext()
        >>> context.getPluginPath().endswith('/Plugins')
        True
        """
        return os.path.expanduser(self.PLUGIN_PATH)

    def save(self, path=None):
        """Save the current builder data into Sketch plugin, indicated by path.

        >>> context = SketchJSContext()
        >>> context.newDocument()
        >>> context.newPage()
        >>> context.rect(10, 20, 100, 200)
        >>> context.save('_export/SaveExample.sketchplugin')
        """
        self.b.save(path)

    def newDocument(self, w=None, h=None):
        """ Create a new document in the builder, that will create the Sketch JS
        code to create a new document when running the plugin.

        >>> context = SketchJSContext()
        >>> context.newDocument()
        >>> 
        """
        self.setSize(w, h)
        self.b.newDocument(self.w, self.h)

    def newDrawing(self, w, h):
        pass

    def newPage(self, w=None, h=None):
        pass

    def saveDrawing(self, path, multiPage=True):
        pass

    def stroke(self, c, strokeWidth=None):
        pass

    def line(self, p1, p2):
        pass

    def getFlattenedPath(self, path=None):
        pass

    def getFlattenedContours(self, path=None):
        pass

    def getGlyphPath(self, glyph, p=None, path=None):
        pass


if __name__ == '__main__':
  import doctest
  doctest.testmod()[0]