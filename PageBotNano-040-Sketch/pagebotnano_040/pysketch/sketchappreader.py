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
#   sketchappreader.py
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

class SketchAppReader(SketchAppBase):

  def read(self, path):
    """Read a sketch file and answer a SketchDocument that contains the interpreted data.

    >>> path = 'resources/TemplateSquare.sketch'
    >>> reader = SketchAppReader()
    >>> skf = reader.read(path)
    >>> skf.document.do_objectID is not None
    True
    >>> len(skf.pages)
    1
    >>> pageId, page = sorted(skf.pages.items())[0]
    >>> page.__class__.__name__
    'SketchPage'
    >>> page.name
    'Page 1'
    >>> page.frame
    <SketchRect x=0 y=0 w=0 h=0>
    >>> page.isLocked
    False
    >>> page.isVisible
    True
    >>> page.exportOptions
    <SketchExportOptions>
    >>> artboard = page.layers[0]
    >>> artboard
    <SketchArtboard name=Artboard1 w=576 h=783>
    >>> artboard.layers[0]
    <SketchRectangle name=RectangleTopLeft>
    >>> bitmap = artboard.layers[0]
    >>> bitmap.frame
    <SketchRect x=60 y=96 w=216 h=168>
    """

    assert path.endswith('.'+FILETYPE_SKETCH)
    fileName = path.split('/')[-1] # Use file name as document name and storage of images

    skf = SketchFile(path)

    # Construct the directory name to store images. Create the directory if it does not exist.
    # aPath/fileName.sketch --> aPath/fileName_images/
    # Answer the newly constructed image path.
    imagesPath = skf.imagesPath
    if not os.path.exists(imagesPath):
      os.makedirs(imagesPath)

    zf = zipfile.ZipFile(path, mode='r') # Open the file.sketch as Zip.
    zipInfo = zf.NameToInfo

    # Set general document info
    if DOCUMENT_JSON in zipInfo:
      fc = zf.read(DOCUMENT_JSON).decode("utf-8")
      d = json.loads(fc)
      skf.document = SketchDocument(parent=skf, **d)
    else:
      return None # Cannot readw this file.

    # Set general user info
    if USER_JSON in zipInfo:
      fc = zf.read(USER_JSON).decode("utf-8")
      d = json.loads(fc)
      skf.user = SketchUser(parent=skf, **d)

    # Read pages and build self.imagesId2Path dictionary, as we find sId-->name relations.
    for key in zipInfo:
      if key.startswith(PAGES_JSON): # This much be a page.
        fc = zf.read(key).decode("utf-8")
        sketchPageInfo = json.loads(fc)
        # Reading pages/layers will find all docment images, and store them in self.imagesId2Path
        sketchPage = SketchPage(parent=skf, **sketchPageInfo)
        skf.pages[sketchPage.do_objectID] = sketchPage

    # Set general meta info
    if META_JSON in zipInfo:
      fc = zf.read(META_JSON).decode("utf-8")
      d = json.loads(fc)
      skf.meta = SketchMeta(parent=skf, **d)

    # Find all images used in the file tree, so we can save them with their layer name.
    # Note that for now this is not a safe method, in case there are layers with
    # the same name in the document that refer to different bitmap files.
    # Also note that renaming the files in the _images/ folder, will disconnect them
    # from placements by bitmap layers.
    # TODO: Solve this later, creating unique file names.
    imageRefs = set()
    for image in skf.find(_class='bitmap'): # Recursively find all bitmap layers.
      imageBinary = zf.read(image.image._ref)
      # Save by internal name, that we already copied this image.
      imageRefs.add(image.image._ref)
      # If the image cannot be found by key, then use BitMap id as used in the file.
      # Export the image as separate file in _images directory.
      fbm = open(imagesPath + image.name + '.png', 'wb')
      fbm.write(imageBinary)
      fbm.close()

    # Now copy all remaining images (if not used in bitmap layer), under their own name.
    for key in zipInfo:
      if key.startswith(IMAGES_JSON) and key not in imageRefs:
        imageBinary = zf.read(key)
        fileName = key.split('/')[-1]
        fbm = open(imagesPath + fileName, 'wb')
        fbm.write(imageBinary)
        fbm.close()

    # Save any previews in the _images/ directory too.
    # Note that there may be an potential naming conflict here, in case a layer is called
    # "preview".
    # TODO: To be solved later.
    for key in zipInfo:
      if key.startswith(PREVIEWS_JSON): # This is a preview image
        previewBinary = zf.read(key)
        fp = open(imagesPath + key.split('/')[-1], 'wb') # Save in _images/ folder
        fp.write(previewBinary)
        fp.close()

    return skf

if __name__ == '__main__':
  import doctest
  import sys
  sys.exit(doctest.testmod()[0])
