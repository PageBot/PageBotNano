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
class Document:
    """Class names start with a capital. See a class as a factory
    of document objects (name spelled with an initial lower case.)
    For now it will do nothing, but that will change.

    Running this Python file, is testing the consistency by executing
    the docstring below. 

    >>> doc = Document()
    >>> doc # Print the `doc` object, shows the line answered by `__repr__`
    I am a Document
    """
    def __repr__(self):
        # This method is called when print(document) is executed.
        # It shows the name of the class, which can be different for
        # classes that inherit from this Document class.
        return 'I am a ' + self.__class__.__name__ # Answer the name of this class.

if __name__ == "__main__":
    import doctest
    doctest.testmod()[0]
