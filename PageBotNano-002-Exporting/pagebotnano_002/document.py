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
import sys # Import access to some deep Python functions
import os # Import standard Python library to create the _export directory
import drawBot # Import the drawBot functions, embedded in the DrawBot app.

if __name__ == "__main__":
    sys.path.insert(0, "..") # So we can import pagebotnano002 without installing.

# Import some constants that we need in this source.
from pagebotnano_002.constants import A4, EXPORT_DIR

class Document:
    # Class names start with a capital. See a class as a factory
    # of document objects (name spelled with an initial lower case.)
    
    def __init__(self, w=None, h=None):
        """This is the "constructor" of a Document instance (=object).
        It takes two optional attributes: `w` is the general width of 
        pages in points and `h` is the general height of pages.
        If omitted, a default A4 page size is taken from the constants.py file.

        >>> doc = Document()
        >>> doc
        I am a Document(w=595, h=842)
        >>> doc = Document(h=100)
        >>> doc.w, doc.h
        (595, 100)
        >>> doc = Document(w=100, h=150)
        >>> doc
        I am a Document(w=100, h=150)
        >>> h, w = A4 # Reverse the order, to make a landscape A4 document
        >>> doc = Document(w=w, h=h)
        >>> doc # Show that it is landscape
        I am a Document(w=842, h=595)
        """
        if w is None: # If not defined, then take the width of A4
            w, _ = A4
        if h is None: # If not defined, then take the height of A4
            _, h = A4
        # Store the values in the document instance.
        self.w = w
        self.h = h

    def __repr__(self):
        """This method is called when print(document) is executed.
        It shows the name of the class, which can be different, if the
        object inherits from Document.
        
        >>> doc = Document()
        >>> print(doc)
        I am a Document(w=595, h=842)
        """
        return 'I am a %s(w=%d, h=%d)' % (self.__class__.__name__, self.w, self.h)

    def export(self, path):
        """Draw a page and export the document into the _export folder.
        Note that in this version, we still generate the document page
        just before it is exported. Not Page instances are stored in the 
        Document yet.

        >>> doc = Document()
        >>> doc.export('_export/Document-export.jpg') # Exporting the JPG
        """
        # Make sure that the _export folder exists, as it does not standard
        # dowload from Github, nor it is committed to Github.
        if path.startswith(EXPORT_DIR) and not os.path.exists(EXPORT_DIR):
            os.mkdir(EXPORT_DIR)
        # Now let DrawBot do its work, creating the page canvas, filling it
        # black, add the title text and then saving it.
        drawBot.newPage(self.w, self.h)
        # For now to have something visible, draw a gray rectangle filling the page.
        drawBot.fill(0.2) # Set fill color at 20% dark gray.
        drawBot.rect(0, 0, self.w, self.h) # Draw the rectangle for the entire page.
        # Create a Formatted String for white text with the specified font/fontSize.
        fs = drawBot.FormattedString('My specimen', font='Georgia', fontSize=80, fill=1)
        # Draw the FormattedString on this fixed position: x from left and y from top.
        drawBot.text(fs, (50, self.h-100))
        # Save the drawn DrawBot page into the _export folder, using `path` as file name.
        # File in the _export folder are ignored by Git, so they don't upload.
        drawBot.saveImage(path)

if __name__ == "__main__":
    import doctest
    doctest.testmod()[0]
