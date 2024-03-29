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
#   MyBook.py
#
#   This MyBook.py shows an example how to import
#   existing libaries, that contain knowledge about document,
#   pages and the elements on the pages.
#
from random import random
#
# From the library we import the classes (=object factories)
# that we need for creating the type specimen.
# Classes can be recognised by their initial capital name.
from pagebotnano_005.document import Document
from pagebotnano_005.elements import Rect, Text, TextBox
from pagebotnano_005.toolbox.loremipsum import loremipsum

class TypeSpecimen(Document):
    # Class names start with a capital. See a class as a factory
    # of type specimen objects (name spelled with an initial lower case.)
    # In this case we inherit from what is already defined in Document.
    # Similar how a Volkswagen factory would inherit the functions already
    # defined in a generic car factory. Inheriting is one of the most 
    # powerful aspects of Python programming, so an object can perform
    # complex tasks, without the need to add these functions again for
    # every new project.
    pass # For now it will do nothing, but that will change.


# Now we create a new type specimen, by executing the class.
# Compare that by letting a car factory produce a car. We only need
# one factory ("TypeSpecimen" name starting with capital), which
# then can product an inlimited number of typeSpecimen objects (name
# starting with a lower case.)

typeSpecimen = TypeSpecimen() # Execute the class/factory by adding "()"

fontName = 'Georgia'
titleSize = 64
headSize = 24
bodyFontSize = 16
leading = 1.4 # Multiplier for the fontSize;lineHe
padding = 80 # Padding of the page. Outside CSS called "margin" of the page.

def makeCoverPage(doc, title):
    global Rect, Text, TextBox
    global fontName, titleSize, headSize, bodyFontSize, leading, padding

    page = doc.newPage()

    # Fill the page with a random dark color (< 50% for (r, g, b))
    fillColor = random()*0.5, random()*0.5, random()*0.5
    rectangleElement = Rect(0, 0, page.w, page.h, fill=fillColor)
    page.addElement(rectangleElement) # Add the rectangle element to the page.

    # Make a FormattedString for the text box
    fs = Text.FS(title,
        font=fontName, fontSize=titleSize, lineHeight=titleSize*1.1, fill=1)
    # Make a Text element with an (x, y) position and add it to the page.
    textElement = Text(fs, x=padding, y=page.h-1.5*padding)
    page.addElement(textElement) # Add the text element to the page.

    # Add square with light color (> 50% for (r, g, b)) and lighter frame.
    rx = ry = padding # Position from bottom-left
    rw = rh = page.w - 2*padding # Make a square, so w = h
    fillColor = 0.5+random()*0.5, 0.5+random()*0.5, 0.5+random()*0.5
    strokeColor = 0.75+random()*0.25, 0.75+random()*0.25, 0.75+random()*0.25
    rectangleElement = Rect(rx, ry, rw, rh, fill=fillColor,
        stroke=strokeColor, strokeWidth=5)
    page.addElement(rectangleElement) # Add the rectangle element to the page.

def makeBodyPages(doc, bodyText):
    """Create a number of new pages in the document, as long as there is overflow. 
    If no new page size is given, it will take over the size of the document.
    """
    fs = Text.FS(bodyText, font=fontName, fontSize=bodyFontSize, lineHeight=bodyFontSize*leading)
    while True:
        page = doc.newPage()
        # Add text element with page number
        pn = TextBox.FS(str(page.pn), align='center', font=fontName, fontSize=bodyFontSize)
        page.addElement(Text(pn, page.w/2, padding/2))
        e = TextBox(fs, x=padding, y=padding, w=page.w-2*padding, h=page.h-2*padding, fill=1)
        page.addElement(e)
        fs = e.getOverflow(fs)
        if not fs:
            break

txt = loremipsum(doShuffle=True)

makeCoverPage(typeSpecimen, 'Book about\n'+fontName)
makeBodyPages(typeSpecimen, txt)

# There could be future composing functions here.

# Build the document, all pages and their contained elements.
typeSpecimen.build() 

# Create the "_export" folder if it does not exist yet.
# This Github repository is filtering file to not upload _export.
# Export the specimen as empty page as PDF and PNG.
typeSpecimen.export('_export/MyBook.pdf')
typeSpecimen.export('_export/MyBook.png')

print('Done 005')
