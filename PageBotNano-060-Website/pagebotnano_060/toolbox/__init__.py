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

def path2Extension(path):
    """Answer the extension of path. Answer None of there is no extension.

    >>> path2Extension('../../images/myImage.jpg')
    'jpg'
    >>> path2Extension('aFile.PDF') # Answer a lowercase
    'pdf'
    >>> path2Extension('aFile') is None # No extension
    True
    >>> path2Extension('../../aFile') is None # No extension on file name
    True
    """
    parts = path.split('/')[-1].split('.')
    if len(parts) > 1:
        return parts[-1].lower()
    return None

def path2FileName(path):
    """Answer the file name part of the path.

    >>> path2FileName('../../aFile.pdf')
    'aFile.pdf'
    >>> path2FileName('../../') is None # No file name
    True
    """
    return path.split('/')[-1] or None

def path2DirectoryName(path):
    """Answer the directory name part of the path.

    >>> path2DirectoryName('../../aFile.pdf')
    '../../'
    """
    return '/'.join(path.split('/')[:-1]) + '/'

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

def pt(pt):
    """Convert to points from points: return the same value.

    >>> pt(72)
    72
    """
    return pt
 
if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]