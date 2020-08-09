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
#   page.py
#
#   This source contains the class with knowledge about elements that
#   can be placed on a page.
#
class Page:
    """Class names start with a capital letter.
    Think of classes as factories for making objects (in this case, page objects) 
    whose names start with a lowercase letter.
    
    Running this Python file tests consistency by executing the docstring below. 
    
    >>> e = Page()
    >>> e
    I am a Page
    """
    pass # For now the code does nothing, but that will change in later versions.

    def __repr__(self):
        # This method is called when print(page) is executed. It returns the name of 
        # its class, which can be different for classes that inherit from the Page class.
        return 'I am a ' + self.__class__.__name__

if __name__ == "__main__":
    import doctest
    doctest.testmod()[0]
