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
#   This MyTypeSpecimen.py is an example of how to import existing `libraries`—
#	in this case, files that contain knowledge about documents, pages, and 
#	elements on pages.
#
# From the pagebotnano library we import the classes (= `object factories`) that 
# we need to create a type specimen for the local library.
# If this file and the pagebotnano library are in the same directory level, there 
# is no need to install the library in Python.
#
from pagebotnano_001.document import Document
from pagebotnano_001.page import Page
from pagebotnano_001.elements import Element

class TypeSpecimen(Document):
    """Class names start with a capital letter.
    Think of classes as factories for making objects (in this case, document objects) 
    whose names start with a lowercase letter.
    In this case, the class inherits from the function definitions in the Document 
    class, similar to how a Volkswagen factory would inherit the functions already
    defined in a generic car factory.
    Inheriting is one of the most powerful features of Python programming. It allows 
    objects to perform complex tasks without needing to add these functions again for
    every new project.
    """

# Now we create a new type specimen by executing the class. Compare it to telling 
# a car factory to produce a car. One `factory` (`TypeSpecimen`; note again 
# its name starts with a capital letter) can produce an inlimited number 
# of typeSpecimen objects (again, their names start with a lowercase letter.)

typeSpecimen = TypeSpecimen() # The "()" executes the class/`factory`
print(typeSpecimen)

# It seems like nothing has happened, because the class/`factory` is still empty—
# without any functions. That will change in later versions.
# We know the code worked, though, because running it in DrawBot raised no error.

print('Done 001')
