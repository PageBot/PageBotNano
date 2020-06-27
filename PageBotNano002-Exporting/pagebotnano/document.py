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
#   document.py
#
#   This source contains the class with knowledge about a generic document.
#
import os # Import standard Python library to create the _export directory
import sys # Import access to some deep Python functions
sys.path.insert(0, "..") # So we can import pagebotnano without installing.
import drawBot # Import the drawBot functions, embedded in the DrawBot app.

from pagebotnano.constants import A4, EXPORT_DIR

class Document:
    # Class names start with a capital. See a class as a factory
    # of document objects (name spelled with an initial lower case.)
    
    def __init__(self, w=None, h=None):
        """This is the "constructor" of a Document instance (=object).
        It takes two optional attributes: `w` is the general width of 
        pages and `h` is the general height of pages.
        If omitted, a default A4 page size is taken from the content.py file.

        >>> doc = Document()
        >>> doc
        I am a Document(w=595, h=842)
        """
        if w is None: # If not defined, take take the width of A4
            w, _ = A4
        if h is None: # If not defined, then take the height of A4
            _, h = A4
        # Store the values in the document instance.
        self.w = w
        self.h = h

    def __repr__(self):
        # This method is called when print(document) is executed.
        # It shows the name of the class, which can be different, if the
        # object inherits from Document.
        return 'I am a %s(w=%d, h=%d)' % (self.__class__.__name__, self.w, self.h)

    def export(self, path):
        """Draw a page and export the document into the _export folder.
        Note that in this version, we still generate the document page at
        just before it is exported. Not Page instances are stored in the 
        Document yet.
        """
        # Make sure that the _export folder exists, as it does not standard
        # dowload from Github, nor it is committed to Github.
        if path.startswith(EXPORT_DIR) and not os.path.exists(EXPORT_DIR):
            os.mkdir(EXPORT_DIR)
        # Now let DrawBot do its work, creating the page and saving it.
        drawBot.newPage(self.w, self.h)
        # For now to have something visible, draw a gray rectangle filling the page.
        drawBot.fill(0.2) # Set fill color at 20% black.
        drawBot.rect(0, 0, self.w, self.h) # Draw the rectangle.
        # Create a Formatted String in white with specified font/fontSize.
        fs = drawBot.FormattedString('My specimen', font='Georgia', fontSize=80, fill=1)
        # Draw the FormattedString on this fixed position.
        drawBot.text(fs, (50, self.h-100))
        # Save the drawn DrawBot page into the _export folder, using `path` as file name.
        drawBot.saveImage(path)

if __name__ == "__main__":
    import doctest
    doctest.testmod()[0]
