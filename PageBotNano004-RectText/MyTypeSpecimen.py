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
#   MyTypeSpecimen.py
#
#   This MyTypeSpecimen.py shows an example how to import
#   existing libaries, that contain knowledge about document,
#   pages and the elements on the pages.
#
from random import random

# From the library we import the classes (=object factories)
# that we need for creating the type specimen.
# Classes can be recognised by their initial capital name.
from pagebotnano.document import Document
from pagebotnano.elements import Rect, Text

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

padding = 50 # Padding of the page. Outside CSS called "margin" of the page.

# Create a number of new pages in the document. If no new page size is given, 
# it will take over the size of the document.
for n in range(10):
    page = typeSpecimen.newPage()

    # Fill the page with a random dark color (< 50% for (r, g, b))
    fillColor = random()*0.5, random()*0.5, random()*0.5
    rectangleElement = Rect(0, 0, page.w, page.h, fill=fillColor)
    page.addElement(rectangleElement) # Add the rectangle element to the page.

    # Make a FormattedString for the text box
    fs = Text.FormattedString('My specimen\nPage %d' % page.pn, 
        font='Georgia', fontSize=80, lineHeight=90, fill=1)
    # Make a Text element with an (x, y) position and add it to the page.
    textElement = Text(fs, x=padding, y=page.h-2*padding)
    page.addElement(textElement) # Add the text element to the page.

    # Add square with light color (> 50% for (r, g, b)) and lighter frame.
    rx = ry = padding # Position from bottom-left
    rw = rh = page.w - 2*padding # Make a square, so w = h
    fillColor = 0.5+random()*0.5, 0.5+random()*0.5, 0.5+random()*0.5
    strokeColor = 0.75+random()*0.25, 0.75+random()*0.25, 0.75+random()*0.25
    rectangleElement = Rect(rx, ry, rw, rh, fill=fillColor,
        stroke=strokeColor, strokeWidth=5)
    page.addElement(rectangleElement) # Add the rectangle element to the page.


# Build the document, all pages and their contained elements.
typeSpecimen.build() 

# Shows: I am a TypeSpecimen(w=595, h=842, pages=10) with default size
# and the amount of created images.
print(typeSpecimen) 
# Show the pages
for page in typeSpecimen.pages:
    print(page)

# Create the "_export" folder if it does not exist yet.
# This Github repository is filtering file to not upload _export.
# Export the specimen as empty page as PDF and PNG.
typeSpecimen.export('_export/MyTypeSpecimen.pdf')
typeSpecimen.export('_export/MyTypeSpecimen.png')

