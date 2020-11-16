from vanilla import Window
from canvas import Canvas
from AppKit import NSMakeRect, NSColor, NSBezierPath
from colors import yellowColor, rgba

M = 20
class ExampleWindow:

    def __init__(self):
        self.w = Window((400, 400), minSize=(200, 200))
        self.w.canvas = Canvas((M, M, -M, -M), delegate=self)
        self.w.open()

    def draw(self, rect):
        #NSColor.redColor().set()
        yellowColor.set()
        for n in range(50):
            rgba(random(), random(), random())
            rect = NSMakeRect(n*400+M, n*400+M, M, M)
            path = NSBezierPath.bezierPathWithRect_(rect)
            path.fill()

ExampleWindow()