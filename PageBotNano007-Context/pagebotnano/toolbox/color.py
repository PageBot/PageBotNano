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
#   color.py
#
#   This source contains supporting functions for PageBotNano classes.
#
def asRgbaColor(c):
    """Convert the attribute to a color tuple that is valid in DrawBot.

    >>> asRgbaColor(1) # Answer white color tuple
    (1, 1, 1, 1)
    >>> asRgbaColor((0, 0, 1)) # Answer blue color
    (0, 0, 1, 1)
    >>> asRgbaColor((0.5)) # 50% gray
    (0.5, 0.5, 0.5, 1)
    >>> asRgbaColor((0.5, 0.4, 0.3, 0.2))
    (0.5, 0.4, 0.3, 0.2)
    """
    if isinstance(c, (tuple, list)):
        if len(c) == 3:
            r, g, b = c
            return r, g, b, 1 # Return the color with undefined opacity.
        if len(c) == 4:
            return c # Answer the color tuple unchanged.
        return (0, 0, 0) # Answer black in case of error
    elif isinstance(c, (float, int)) and 0 <= c <= 1:
        # Fill the green and blue with the red value, if they are undefined.
        return c, c, c, 1 # Answer the gray scale (r, g ,b, a) 
    print('asRgbaColor: Color "%s" does not have the right format' % str(c))

if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]