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
#   builder.py
#
#   https://developer.sketch.com/reference/api/
#   https://developer.sketch.com/reference/api/#create-a-new-document
#
import os
import sys
import shutil
from random import random
sys.path.insert(0, "../../../") # So we can import pagebotnano without installing.
import codecs

from pagebotnano_040.toolbox import pt
from pagebotnano_040.toolbox.color import noColor, color
from pagebotnano_040.constants import A4

# The directory where SketchApp keeps the plugins. Note that it starts with a "~"
# so that must be inside the local user area.
# In general, it is better to save the .sketchplugin in a local folder, then 
# double click on the file to let SketchApp install the plugin (first remove
# it, if it already exists).
PLUGIN_PATH = """~/Library/Application Support/com.bohemiancoding.sketch3/Plugins"""
PLUGIN_EXTENSION = 'sketchplugin'

class SketchJSBuilder:
    PB_ID = 'SketchJS'

    def __init__(self, path=None, **kwargs):
        """
        >>> from pagebotnano_040.contexts.sketchjs.context import SketchJSContext
        >>> b = SketchJSBuilder()
        >>> b
        <SketchJSBuilder>
        >>> b.jsOut
        []
        >>> b.newDocument()
        >>> b.fill(color('red'))
        >>> b.rect(10, 20, 250, 200)
        >>> b.fill(color('darkblue'))
        >>> b.rect(110, 120, 250, 200)
        >>> b.save('_export/PageBotNano_init.sketchplugin')
        """
        super().__init__(**kwargs)
        # Initialising code, collect lines to place only once. Note that the order is arbitrary
        self.prepareOut = set((
            "var sketch = require('sketch/dom')",
            "var async = require('sketch/async')",
            "var DataSupplier = require('sketch/data-supplier')",
            "var UI = require('sketch/ui')",
            "var Settings = require('sketch/settings')",
            "var Document = require('sketch/dom').Document",
        )) 
        self.globalOut = [] # Output stream for predefined variables.
        self.jsOut = [] # Output stream for generated JavaScript
        self.path = path
        self._fill = None
        self._stroke = None
        self._strokeWidth = 0
        self.shapeId = 0 # Incremental shape id to make unique names.
        self.parent = 'thisArtboard' # Default to use the current Artboard as parent.

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

    def newStyle(self, name, style):
        """
        The Sketch Style is a dictionary attribute of Sketch Shape
        style.opacity (number) The opacity of a Layer, between 0 (transparent) and 1 (opaque).
        style.blendingMode (BlendingMode) The blend mode used to determine the composite color.
        style.blur (Blur) The blur applied to the Layer.
        style.fills (Fill[]) The fills of a Layer.
        style.borders (Border[]) The borders of a Layer.
        style.borderOptions (BorderOptions) The options that the borders share.
        style.shadows (Shadow[]) The shadows of a Layer.
        style.innerShadows (Shadow[]) The inner shadows of a Layer.
        style.alignment (Alignment) The horizontal alignment of the text of a Text Layer
        style.verticalAlignment (VerticalAlignment) The vertical alignment of the text of a Text Layer
        style.kerning (number / null) The kerning between letters of a Text Layer. null means that the kerning will be the one defined by the font.
        style.lineHeight (number / null) The height of a line of text in a Text Layer. null means “automatic”.
        style.paragraphSpacing (number) The space between 2 paragraphs of text in a Text Layer.
        style.textColor (string) A rgba hex-string (#000000ff is opaque black) of the color of the text in a Text Layer.
        style.fontSize (number) The size of the font in a Text Layer.
        style.textTransform (‘none’ / ‘uppercase’ / ‘lowercase’) The transform applied to the text of a Text Layer.
        style.fontFamily (string) The name of the font family of a Text Layer. 'system' means the font family of the OS ('.SF NS Text' on macOS 10.14).
        style.fontWeight (number) The weight of the font of a Text Layer. Goes from 0 to 12, 0 being the thinest and 12 being the boldest. Not every weight are available for every fonts. When setting a font weight that does not exist for the current font family, the closest weight that exists will be set instead.
        style.fontStyle (‘italic’ / undefined) The style of the font of a Text Layer.
        style.fontVariant (‘small-caps’ / undefined) The variant of the font of a Text Layer.
        style.fontStretch (‘compressed’ / ‘condensed’ / ‘narrow’ / ‘expanded’ / ‘poster’ / undefined) The size variant of the font of a Text Layer.
        style.textUnderline (string: <line-style> [<line-pattern>] ['by-word'] / undefined where <line-style> can be single / thick / double and <line-pattern> can be dot / dash / dash-dot / dash-dot-dot) The underline decoration of a Text Layer.
        style.textStrikethrough (string: <line-style> [<line-pattern>] ['by-word'] / undefined where <line-style> can be single / thick / double and <line-pattern> can be dot / dash / dash-dot / dash-dot-dot) The strikethrough decoration of a Text Layer.
        style.fontAxes (FontAxes) The axes of the Text Layer font (only available when the font is a variable font).

        """
        self.prepareOut.add("var Style = require('sketch/dom').Style")

    def newDocument(self, w=None, h=None):
        """
        In Sketch JS the following lines are valid for export.
        var Document = require('sketch/dom').Document
        var document = new Document()
        var document = Document.getSelectedDocument()
        var documents = Document.getDocuments()
        Avilable attributes:
        document.id (string) The unique ID of the document.
        document.pages (Page[]) The pages of the document.
        document.selectedPage (Page) The selected page of the Document.
        document.selectedLayers (Selection) The Selection of the layers that the user has selected in the currently selected page.
        document.path (string) The path to the document (or the appcast URL in case of a Document from a remote Library).
        document.sharedLayerStyles (SharedStyle[]) The list of all shared layer styles defined in the document.
        document.sharedTextStyles (SharedStyle[]) The list of all shared text styles defined in the document.
        document.colors (ColorAsset[]) A list of color assets defined in the document. Mutating the returned array will update the document colors.
        document.gradients (GradientAsset[]) A list of gradient assets defined in the document. Mutating the returned array will update the document gradients.
        document.colorSpace (ColorSpace) The color space of the document.

        """
        #self.prepareOut.add("let sketch = require('sketch')")
        
        self.globalOut.append("var pwWidth = %d" % (w or pt(A4[0])))
        self.globalOut.append("var pwHeight = %d" % (w or pt(A4[1])))

        self.jsOut.append("var document = new Document()")
        #self.jsOut.append("let document = sketch.getSelectedDocument()")
        self.jsOut.append("let page = document.selectedPage")
        self.jsOut.append("page.layers = []")
        self.jsOut.append("let Artboard = sketch.Artboard")
        self.jsOut.append("let thisArtboard = new Artboard({")
        self.jsOut.append("\tparent: page,") # Artboard is the PageBotNano Page equivalent
        self.jsOut.append("\tframe: { x: 0, y: 0, width: pbWidth, height: pbHeight }")
        self.jsOut.append("})")

    def frameDuration(self, frameDuration):
        pass

    def _getIdNumber(self, v):
        return int(round(int('0x' + 'F'*v, base=16)*random()))

    def makeSketchIdentifier(self):
        """Make Sketch identifier, similar to:
                'com.example.sketch.28e11d34-b511-42e4-8cfb-7f49dc7e2831

        >>> b = SketchJSBuilder()
        >>> b.makeSketchIdentifier().startswith('com.example.sketch.')
        True
        """
        return 'com.example.sketch.%08x-%04x-%04x-%04x-%012x' % (
           self._getIdNumber(8),
           self._getIdNumber(4),
           self._getIdNumber(4),
           self._getIdNumber(4),
           self._getIdNumber(12),
        )

    SCRIPT_JS = 'script.js'
    MANIFEST_JSON = """
{
  "author" : "",
  "commands" : [
    {
      "script" : "%(fileName)s",
      "name" : "%(name)s",
      "handlers" : {
        "run" : "onRun"
      },
      "identifier" : "com.bohemiancoding.sketch.runscriptidentifier"
    }
  ],
  "menu" : {
    "title" : "%(name)s",
    "items" : [
      "com.bohemiancoding.sketch.runscriptidentifier"
    ]
  },
  "identifier" : "%(identifier)s",
  "version" : "1.0",
  "description" : "%(description)s",
  "authorEmail" : "%(email)s",
  "name" : "%(name)s"
}
"""
    def save(self, path=None):
        # Make sure the path does not exist, otherwise delete it.
        if path is None:
            path = '_export/Untitled.sketchplugin'
        # Make sure we have an empty plugin folder
        if os.path.exists(path):
            shutil.rmtree(path)
        contentsPath = path + '/Contents'
        sketchPath = contentsPath + '/Sketch'
        # Make the new plugin folder and populate it.
        os.makedirs(sketchPath) 
        f = codecs.open(sketchPath + '/' + self.SCRIPT_JS, 'w', encoding='utf-8')
        f.write('var onRun = function(context) {\n\n')    
        f.write('/* Prepare */\n')      
        f.write('\n'.join(sorted(self.prepareOut)))
        f.write('/* Global variables */\n')      
        f.write('\n'.join(sorted(self.globalOut)))
        f.write('\n\n/* Script */\n')
        f.write('\n'.join(self.jsOut))
        f.write('\n\n}')
        f.close()

        manifestParams = dict(
            name=path.split('/')[-1].replace('.sketchplugin', ''),
            identifier=self.makeSketchIdentifier(),
            email='info@designdesign.space',
            description='Description of the plugin',
            fileName=self.SCRIPT_JS,
        )
        f = codecs.open(sketchPath + '/manifest.json', 'w', encoding='utf-8')
        f.write(self.MANIFEST_JSON % manifestParams)
        f.close()

    def fill(self, c):
        self._fill = c

    def rect(self, x, y, w=None, h=None, **kwargs):
        """Build the JavaScript code that generates a rectangle in SketchApp.

        >>> b = SketchJSBuilder()
        >>> b.fill(color('red'))
        >>> b.rect(10, 20, 100, 200)
        """
        if w is None:
            w = DEFAULT_WIDTH
        if h is None:
            h = DEFAULT_HEIGHT
        self.prepareOut.add("var ShapePath = require('sketch/dom').ShapePath")
        params = dict(
            shapeId=self.shapeId,
            parent=self.parent,
            x=x, y=y, w=w, h=h,
            fill=(self._fill or color(0, 0, 0)).hex,
        )      
        self.jsOut.append("""
let rect%(shapeId)s = new ShapePath({
    parent: %(parent)s,
    frame: { x:%(x)d, y:%(y)d, width:%(w)d, height:%(h)d },
    style: { fills: ['#%(fill)s'], borders: []}
})
""" % params)
        self.shapeId += 1

    def text(self, bs, (x, y)):
        """
        Create a text layer (in Sketch a layer is equivalent to PageBotNano element).

        e.id (string) The unique ID of the Text.
        e.name (string) The name of the Text
        e.parent (Group) The group the Text is in.
        e.locked (boolean) If the Text is locked.
        e.hidden (boolean) If the Text is hidden.
        e.frame (Rectangle) The frame of the Text. This is given in coordinates that are local to the parent of the layer.
        e.selected (boolean) If the Text is selected.
        e.flow (Flow) The prototyping action associated with the Text.
        e.exportFormats (ExportFormat[]) The export formats of the Symbol Master.
        e.transform (object) The transformation applied to the Text.
        e.transform.rotation (number) The rotation of the Text in degrees, clock-wise.
        e.transform.flippedHorizontally (boolean) If the Text is horizontally flipped.
        e.transform.flippedVertically (boolean) If the Text is vertically flipped.
        e.style (Style) The style of the Text.
        e.sharedStyle (SharedStyle / null) The associated shared style or null.
        e.sharedStyleId (string / null) The ID of the SharedStyle or null, identical to sharedStyle.id.
        e.text (string) The string value of the text layer.
        e.lineSpacing (LineSpacing) The line spacing of the layer.
        e.fixedWidth (boolean) Whether the layer should have a fixed width or a flexible width.
        
        """


    def _get_size(self):
        return upt(self.sketchApi.getSize())
    size = property(_get_size)

    def restore(self):
        pass


if __name__ == '__main__':
  import doctest
  import sys
  sys.exit(doctest.testmod()[0])
