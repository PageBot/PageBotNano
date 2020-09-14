

class Glyph:
    def __init__(self, name, width):
        self.name = name
        self.points = ((100, 0), (100, 700), (180, 700), (180, 0))
        self.width = width

    def getLeftMargin(self):
        lm = 100000000
        for x, _ in self.points:
            #if x < lm:
            #    lm = x
            lm = min(x, lm)
        return lm

    def getRightMargin(self):
        maxX = -100000000
        for x, _ in self.points:
            #if x > maxX:
            #    maxX= x
            maxX = max(x, maxX)
        return self.width - maxX

    def _get_leftMargin(self):
        return(self.getLeftMargin())
    leftMargin = property(_get_leftMargin)
    
    def _get_rightMargin(self):
        return(self.getRightMargin())
    rightMargin = property(_get_rightMargin)
    
g = Glyph('A', 400)
print(g.name, g.width)
print(g.leftMargin, g.rightMargin)
print(g.getLeftMargin(), g.getRightMargin())

