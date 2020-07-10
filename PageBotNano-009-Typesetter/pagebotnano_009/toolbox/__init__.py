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
#   This source makes it possible to import other sources
#   from this directory/folder
#
def extensionOf(path):
    """Answer the extension of path. Answer None of there is no extension.

    >>> extensionOf('../../images/myImage.jpg')
    'jpg'
    >>> extensionOf('aFile.PDF') # Answer a lowercase
    'pdf'
    >>> extensionOf('aFile') is None # No extension
    True
    >>> extensionOf('../../aFile') is None # No extension on file name
    True
    """
    parts = path.split('/')[-1].split('.')
    if len(parts) > 1:
        return parts[-1].lower()
    return None

def fileNameOf(path):
    """Answer the file name part of the path.

    >>> fileNameOf('../../aFile.pdf')
    'aFile.pdf'
    >>> fileNameOf('../../') is None # No file name
    True
    """
    return path.split('/')[-1] or None

#   M E A S U R E S

def mm(mm):
    """Convert from millimeter values to rounded points
    
    >>> mm(210)
    595
    >>> mm(297)
    842
    """
    return int(round(mm * 72 * 0.039370)) # Approximated 1" = 25.400051mm

def cm(cm):
    """Convert from millimeter values to rounded points
    
    >>> cm(21)
    595
    >>> cm(29.7)
    842
    """
    return int(round(cm * 72 * 0.039370 * 10)) # Approximated 1" = 25.400051mm

if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]