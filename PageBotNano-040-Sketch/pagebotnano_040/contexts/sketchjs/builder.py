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
sys.path.insert(0, "../../../") # So we can import pagebotnano without installing.
import codecs

class SketchJSBuilder:
    PB_ID = 'SketchJS'

    def __init__(self, path=None, **kwargs):
        """
        >>> b = SketchJSBuilder()
        >>> b
        <SketchJSBuilder>
        >>> b.jsOut
        []
        >>> b.rect(10, 20, 100, 200)
        >>> b.jsOut
        ['var rect = new Rectangle(10.00, 20.00, 100.00, 200.00);']
        >>> b.save('_export/SketchJSBuilder_init.sketchplugin')
        """
        super().__init__(**kwargs)
        self.prepare = set() # Initialising code, place only once.
        self.jsOut = [] # Output stream for generated JavaScript
        self.path = path

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

    def newDocument(self, w, h):
        self.jsOut.append('var document = new Document(); /* (w=%s, h=%s)' % (w, h))

    def frameDuration(self, frameDuration):
        pass

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
  "identifier" : "com.example.sketch.28e11d34-b511-42e4-8cfb-7f49dc7e2831",
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
        f.write('\n'.join(self.prepare))
        f.write('\n\n\n')
        f.write('\n'.join(self.jsOut))
        f.close()

        manifestParams = dict(
            name=path.split('/')[-1].replace('.sketchplugin', ''),
            email='info@designdesign.space',
            description='Description of the plugin',
            fileName=self.SCRIPT_JS,
        )
        f = codecs.open(sketchPath + '/manifest.json', 'w', encoding='utf-8')
        f.write(self.MANIFEST_JSON % manifestParams)
        f.close()

    def fill(self, e, g, b, alpha=None):
        pass

    def rect(self, x, y, w=None, h=None, **kwargs):
        """Build the JavaScript code that generates a rectangle in SketchApp.

        >>> b = SketchJSBuilder()
        >>> b.rect(10, 20, 100, 200)
        >>> b.jsOut
        ['var rect = new Rectangle(10.00, 20.00, 100.00, 200.00);']

        """
        if w is None:
            w = DEFAULT_WIDTH
        if h is None:
            h = DEFAULT_HEIGHT
        self.prepare.add("var Rectangle = require('sketch/dom').Rectangle;")
        self.jsOut.append("var rect = new Rectangle(%0.2f, %0.2f, %0.2f, %0.2f);" % (x, y, w, h))

    def _get_pages(self):
        """Answer the list of all SketchPage instances.

        >>> b = SketchJSBuilder()
        >>> b
        <SketchJSBuilder>
        """
        return self.sketchApi.getPages()
    pages = property(_get_pages)

    def _get_size(self):
        return upt(self.sketchApi.getSize())
    size = property(_get_size)

    def restore(self):
        pass


if __name__ == '__main__':
  import doctest
  import sys
  sys.exit(doctest.testmod()[0])
