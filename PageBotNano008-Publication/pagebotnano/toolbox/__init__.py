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
#   from this diretory/folder
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

if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]