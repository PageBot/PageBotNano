# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     apoint.py
#
import weakref

class APoint:
    """Analyzer Point, used if addition information (like its type) needs to be
    stored. Otherwise just use the point2D() and point3D() which are simple
    tuples.
    Note that the values are plain numbers in font.info.unitsPerEm, not PabeBot units.

    >>> p = APoint((101, 303), True)
    >>> p.onCurve is False
    False
    >>> print(p)
    <APoint x=101 y=303 On>
    """

    def __init__(self, xy, onCurve=True, glyph=None, index=None):
        self.glyph = glyph # Set the weakref by property
        self.index = index # Index of this point in glyph.points
        assert isinstance(xy, (list, tuple)) and len(xy) == 2
        self.p = xy # (x, y)
        self.onCurve = bool(onCurve)

    def __getitem__(self, i):
        """Allow APoint to x and y attributes to be indexed like a point2D tuple.

        >>> ap = APoint((100, 200))
        >>> ap
        <APoint x=100 y=200 On>
        >>> ap[0], ap[1]
        (100, 200)
        """
        return self.p[i]

    def __setitem__(self, i, value):
        """Allow APoint to x and y attributes to be indexed like a point2D or point3D tuple.

        >>> ap = APoint((100, 200))
        >>> ap[1] = 222
        >>> ap
        <APoint x=100 y=222 On>
        >>> ap[0], ap[1]
        (100, 222)
        """
        self.p = list(self.p)
        self.p[i] = value

        # Update the changed point value in the glyph.
        glyph = self.glyph
        if glyph is not None and self.index is not None: # Glyph still alive? Then update x or y
            x, y = glyph.coordinates[self.index]
            if i == 0:
                glyph.coordinates[self.index] = value, y
            elif i == 1:
                glyph.coordinates[self.index] = x, value
            # Ignore setting of z
            glyph.dirty = True

    def _get_onCurve(self):
        return self._onCurve
    def _set_onCurve(self, onCurve):
        self._onCurve = onCurve
        # Update the changed point value in the glyph.
        glyph = self.glyph
        if glyph is not None and self.index is not None: # Still alive, then update glyph points too.
            glyph.flags[self.index] = bool(onCurve)
            glyph.dirty = True
    onCurve = property(_get_onCurve, _set_onCurve)

    def _get_offCurve(self):
        return not self.onCurve
    def _set_offCurve(self, offCurve):
        self.onCurve = not offCurve
    offCurve = property(_get_offCurve, _set_offCurve)

    def __lt__(self, p):
        """Compare the points.

        >>> APoint((100, 200)) < APoint((200, 300))
        True
        >>> APoint((100, 200)) < APoint((100, 300))
        True
        >>> APoint((100, 200)) < APoint((100, 200))
        False
        """
        return self.p < p.p

    def __le__(self, p):
        """Compare the points.

        >>> APoint((100, 200)) <= APoint((200, 300))
        True
        >>> APoint((100, 200)) <= APoint((100, 300))
        True
        >>> APoint((100, 200)) <= APoint((100, 200))
        True
        >>> APoint((100, 200)) <= APoint((100, 199))
        False
        """
        return self.p <= p.p

    def __gt__(self, p):
        """Compare the points.

        >>> APoint((200, 100)) > APoint((100, 300))
        True
        >>> APoint((200, 200)) > APoint((200, 100))
        True
        >>> APoint((200, 100)) > APoint((200, 99))
        True
        >>> APoint((200, 100)) > APoint((200, 100))
        False
        """
        return self.p > p.p

    def __ge__(self, p):
        """Compare the points.

        >>> APoint((200, 100)) >= APoint((100, 300))
        True
        >>> APoint((200, 200)) >= APoint((200, 100))
        True
        >>> APoint((200, 100)) >= APoint((200, 100))
        True
        >>> APoint((200, 100)) >= APoint((200, 101))
        False
        """
        return self.p >= p.p

    def __sub__(self, p):
        """Subtract the points. Result is a point3D tuple.

        >>> APoint((200, 500)) - APoint((100, 300))
        (100, 200)
        >>> APoint((200, 500)) - APoint((100, 300))
        (100, 200)
        >>> APoint((200, 500)) - APoint((-100, -300))
        (300, 800)
        """
        return self.p[0] - p[0], self.p[1] - p[1]

    def __add__(self, p):
        """Add the points. Result is a point3D tuple.

        >>> APoint((200, 500)) + APoint((100, 300))
        (300, 800)
        >>> APoint((200, 500)) + APoint((100, 300))
        (300, 800)
        >>> APoint((200, 500)) + APoint((-100, -300))
        (100, 200)
        """
        return self.p[0] + p[0], self.p[1] + p[1]

    def __mul__(self, v):
        """Multiply the point by a scalar. Result is a point3D tuple.

        >>> APoint((200, 500)) * 2
        (400, 1000)
        >>> APoint((200, 500)) * 2
        (400, 1000)
        """
        assert isinstance(v, (int, float))
        return self.p[0] * v, self.p[1] * v

    def __div__(self, v):
        """Divide the point by a scalar. Result is a point3D tuple.

        >>> APoint((200, 500)) / 2
        (100, 250)
        >>> APoint((200, 500)) / 2
        (100, 250)
        """
        assert isinstance(v, (int, float))
        return int(round(self.p[0] / v)), int(round(self.p[1] / v))

    __truediv__ = __div__

    def _get_x(self):
        """APoint.x property. Using indexed addressing of self.p to trigger
        Glyph point update.

        >>> ap = APoint((200, 500))
        >>> ap.x = 100
        >>> ap
        <APoint x=100 y=500 On>
        >>> ap.x
        100
        """
        return self.p[0]
    def _set_x(self, x):
        self[0] = x # Indirect by index, triggers the update of the glyph point data.
    x = property(_get_x, _set_x)

    def _get_y(self):
        """APoint.y property. Using indexed addressing of self.p to trigger
        Glyph point update.

        >>> ap = APoint((200, 500))
        >>> ap.y = 100
        >>> ap
        <APoint x=200 y=100 On>
        >>> ap.y
        100
        """
        return self.p[1]
    def _set_y(self, y):
        self[1] = y # Indirect by index, triggers the update of the glyph data.
    y = property(_get_y, _set_y)

    def _get_glyph(self):
        """Answers the parent glyph, if the weakref is still allive."""
        if self._glyph is not None:
            return self._glyph()
        return None
    def _set_glyph(self, glyph):
        if glyph is not None:
            self._glyph = weakref.ref(glyph)
        else:
            self._glyph = None
    glyph = property(_get_glyph, _set_glyph)

    def __repr__(self):
        return '<%s x=%s y=%s %s>' % (self.__class__.__name__, self.x, self.y,
            {True:'On', False:'Off'}[self.onCurve])

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
