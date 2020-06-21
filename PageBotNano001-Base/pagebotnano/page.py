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
    """Class names start with a capital. See a class as a factory
    of page objects (name spelled with an initial lower case.)
    
	Running this Python file, is testing the consistency by executing
	the docstring below. 
	
	>>> e = Page()
	>>> e
	I am a Page
    """
    pass # For now it will do nothing, but that will change in later version.

    def __repr__(self):
        # This method is called when print(document) is executed.
        # It shows the name of the class, which can be different, if the
        # object inherits from Document.
        return 'I am a ' + self.__class__.__name__

if __name__ == "__main__":
    import doctest
    doctest.testmod()[0]
