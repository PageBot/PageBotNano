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
#   https://developer.sketch.com/reference/api/#create-a-new-document
#
import os
import sys
import shutil
from random import random
sys.path.insert(0, "../../../") # So we can import pagebotnano without installing.
import codecs
from pagebotnano_040.toolbox.color import noColor, color

class SketchJSBuilder:
    PB_ID = 'SketchJS'

    def __init__(self, path=None, **kwargs):
        """
        >>> from pagebotnano_040.contexts.sketchjs.context import SketchJSContext
        >>> pluginPath = SketchJSContext.getPluginPath()
        >>> b = SketchJSBuilder()
        >>> b
        <SketchJSBuilder>
        >>> b.jsOut
        []
        >>> b.newDocument()
        >>> b.fill(color('red'))
        >>> b.rect(10, 20, 250, 200)
        >>> b.fill(color('darkblue'))
        >>> b.rect(300, 20, 250, 200)
        >>> b.save('_export/PageBotNano_init.sketchplugin')
        """
        super().__init__(**kwargs)
        self.prepare = set() # Initialising code, place only once.
        self.jsOut = [] # Output stream for generated JavaScript
        self.path = path
        self._fill = None
        self._stroke = None
        self._strokeWidth = 0
        self.shapeId = 0 # Incremental shape id to make unique names.
        self.parent = 'thisArtboard' # Default to use the current Artboard as parent.

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

    def newDocument(self, w=None, h=None):
        self.prepare.add("let sketch = require('sketch')")

        self.jsOut.append("let document = sketch.getSelectedDocument()")
        self.jsOut.append("let page = document.selectedPage")
        self.jsOut.append("page.layers = []")
        self.jsOut.append("let Artboard = sketch.Artboard")
        self.jsOut.append("let thisArtboard = new Artboard({")
        self.jsOut.append("\tparent: page,")
        self.jsOut.append("\tframe: { x: 0, y: 0, width: 400, height: 400 }")
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
        f.write('\n'.join(sorted(self.prepare)))
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
        self.prepare.add("var ShapePath = require('sketch/dom').ShapePath")
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
    style: { fills: ['#%(fill)s']}
})
""" % params)
        self.shapeId += 1


    def _get_size(self):
        return upt(self.sketchApi.getSize())
    size = property(_get_size)

    def restore(self):
        pass


if __name__ == '__main__':
  import doctest
  import sys
  sys.exit(doctest.testmod()[0])
