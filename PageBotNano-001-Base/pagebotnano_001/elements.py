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
#   elements.py
#
#   This source contains the class with information about elements that
#   can be placed on a page.
#
class Element:
    """Class names start with a capital letter.
    Think of classes as factories for making objects (in this case, element objects) 
    whose names start with a lowercase letter.
    
    Running this Python file tests consistency by executing the docstring below. 
    
    >>> e = Element()
    >>> e
    I am an Element
    """
    pass # For now the code does nothing, but that will change in later versions.

    def __repr__(self):
        # This method is called when print(element) is executed. It returns the name of 
        # its class, which can be different for classes that inherit from the Element class.
        return 'I am an ' + self.__class__.__name__

if __name__ == "__main__":
    import doctest
    doctest.testmod()[0]
