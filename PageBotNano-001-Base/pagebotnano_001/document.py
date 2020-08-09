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
#   This source contains the class that stores information about a generic document.
#
class Document:
    """Class names start with a capital letter.
    Think of classes as factories for making objects (in this case, document objects) 
    whose names start with a lowercase letter.
    In this version of the code, the class doesn`t make anything, but that will change.

    Running this Python file tests the consistency of the class by executing the docstring below.

    >>> doc = Document()
    >>> doc # Prints the `doc` object showing the line answered by `__repr__`
    I am a Document
    """
    def __repr__(self):
        """This method is called when print(document) is executed. It returns the name of 
        its class, which can be different for classes that inherit from the Document class.
        """
        return 'I am a ' + self.__class__.__name__ # Returns the name of the class.

if __name__ == "__main__":
    import doctest
    doctest.testmod()[0]
