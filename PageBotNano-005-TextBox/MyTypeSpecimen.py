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

typeSpecimen = TypeSpecimen() # Execute the class/factory by adding "()"
page = typeSpecimen.newPage()

# Build the document, all pages and their contained elements.
typeSpecimen.build() 

# Create the "_export" folder if it does not exist yet.
# This Github repository is filtering file to not upload _export.
# Export the specimen as empty page as PDF and PNG.
typeSpecimen.export('_export/MyTypeSpecimen.pdf')
typeSpecimen.export('_export/MyTypeSpecimen.png')

print('Done 005')
