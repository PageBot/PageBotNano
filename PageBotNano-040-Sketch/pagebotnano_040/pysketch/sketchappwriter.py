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
#   Supporting Sketch, https://github.com/Zahlii/python_sketch_api
# -----------------------------------------------------------------------------
#
#   sketchappwriter.py
#
#   Write the Sketch classes into a valid Sketch file.
#
#   Inspect sketch file:
#   https://xaviervia.github.io/sketch2json/
#
#   https://gist.github.com/xaviervia/edbea95d321feacaf0b5d8acd40614b2
#   This description is not complete.
#   Additions made where found in the Reading specification of this context.
#
#   Webviewer
#   https://github.com/AnimaApp/sketch-web-viewer
#
import sys
sys.path.insert(0, "../../") # So we can import pagebotnano without installing.

from pagebotnano_040.pysketch.sketchclasses import *

class SketchAppWriter(SketchAppBase):
  """
  >>> from pagebotnano_040.pysketch.sketchappreader import SketchAppReader
  >>> testFileNames = (
  ...     'TestImage.sketch',
  ...     'TestRectangles.sketch',
  ...     'TestStar.sketch',
  ...     'TestPolygon.sketch',
  ...     'TestOval.sketch',
  ...     'TestABC.sketch',
  ... )
  >>> for fileName in testFileNames:
  ...     reader = SketchAppReader()
  ...     readPath = 'resources/test/' + fileName
  ...     skf = reader.read(readPath)
  ...     writePath = readPath.replace('.sketch', 'Write.sketch')
  ...     writer = SketchAppWriter()
  ...     writer.write(writePath, skf)
  """

  def write(self, path, sketchFile):
    assert path.endswith('.sketch')
    zf = zipfile.ZipFile(path, mode='w') # Open the file.sketch as Zip.

    tmpPath = '/tmp/'+DOCUMENT_JSON
    f = open(tmpPath, 'w')
    d = sketchFile.document.asJson()
    ds = json.dumps(d)
    f.write(ds)
    f.close()
    zf.write(tmpPath, arcname=DOCUMENT_JSON)
    os.remove(tmpPath)

    tmpPath = '/tmp/'+USER_JSON
    f = open(tmpPath, 'w')
    d = sketchFile.user.asJson()
    ds = json.dumps(d)
    f.write(ds)
    f.close()
    zf.write(tmpPath, arcname=USER_JSON)
    #os.remove(tmpPath)

    tmpPath = '/tmp/'+META_JSON
    f = open(tmpPath, 'w')
    d = sketchFile.meta.asJson()
    ds = json.dumps(d)
    f.write(ds)
    f.close()
    zf.write(tmpPath, arcname=META_JSON)
    os.remove(tmpPath)

    for pageId, page in sorted(sketchFile.pages.items()):
      tmpPath = '/tmp/pages_'+pageId+'.json'
      f = open(tmpPath, 'w')
      d = page.asJson()
      ds = json.dumps(d)
      f.write(ds)
      f.close()

      zf.write(tmpPath, arcname='pages/'+pageId+'.json')
      os.remove(tmpPath)

    # Recursively find all images in the node tree, so we can reconstruct
    # the internal file name from external file name (in _images/)
    imageRefs = set(['images/preview.png']) # Keep track of images that we did or don't want to
    imagesPath = sketchFile.imagesPath
    for image in sketchFile.find('bitmap'): # Recursively find all bitmap layers
      zf.write(imagesPath + image.name + '.png', arcname=image.image._ref)
      imageRefs.add(image.image._ref)

    # Now copy all the remaining images in the directory into the zip
    # keeping their own name. Filter out the preview.png
    for fileName in os.listdir(imagesPath):
      if fileName.startswith('.') or ('images/'+fileName) in imageRefs:
        continue # Skip OS-related based files or file we already did
      zf.write(imagesPath+fileName, arcname=IMAGES_JSON+fileName)

    # Copy the preview to the right zip directory
    previewFileName = 'preview.png' # TODO: Make more generic?
    if os.path.exists(imagesPath + previewFileName):
      zf.write(imagesPath + previewFileName, arcname=PREVIEWS_JSON + previewFileName)

    zf.close()


if __name__ == '__main__':
  import doctest
  import sys
  sys.exit(doctest.testmod()[0])
