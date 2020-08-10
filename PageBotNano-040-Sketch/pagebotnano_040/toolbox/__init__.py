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
import sys
sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano_040.constants import PADDING

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

def pt(pt):
    """Convert to points, so do nothing.

    >>> pt(12)
    12
    """
    return pt
    
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

def makePadding(padding):
    """Check on the various ways that padding can be defined.

    >>> makePadding((10, 20, 30, 40))
    (10, 20, 30, 40)
    >>> makePadding((10, 20))
    (10, 20, 10, 20)
    >>> makePadding(50)
    (50, 50, 50, 50)
    """
    if isinstance(padding, (list, tuple)):  
        if len(padding) == 2:
            pt, pr = pb, pl = padding
        elif len(padding) == 4:
            pt, pr, pb, pl = padding
        else: # In case None or illegal value, then just use defailt
            raise ValueError('%s.padding: Not the right kind of padding "%s"' % (self.__class.__.__name__, padding))
    elif padding is None or isinstance(padding, (int, float)):
        pt = pr = pb = pl = padding or PADDING
    else: # In case None or illegal value, then just use defailt
        raise ValueError('%s.padding: Not the right kind of padding "%s"' % (self.__class.__.__name__, padding))
    if pt is None:
        pt = PADDING
    if pr is None:
        pr = PADDING
    if pb is None:
        pb = PADDING
    if pl is None:
        pl = PADDING
    return pt, pr, pb, pl

if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]