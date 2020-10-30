# Scripting for GlyphsApp

## General Python courses

https://developers.google.com/edu/python/set-up
https://www.codecademy.com/learn/learn-python
https://www.udemy.com/the-python-bible/

## GlyphsApp script examples

https://github.com/mekkablue/Glyphs-Scripts

## GlyphsApp documentation

https://docu.glyphsapp.com/

## UFO documentation

http://unifiedfontobject.org
https://glyphsapp.com/tutorials/working-with-ufo

## GlyphsApp code snippets

Print the designer and designerURL of the current font

~~~ Python
f = Glyphs.font
print(f.designer)
print(f.designerURL)
~~~

Print the sidebearings and width of a glyph (front layer)

~~~ Python
f = Glyphs.font
g = f.glyphs['A'].layers[0]
print(g.LSB) # Left side bearing
print(g.width)
print(g.RSB) # Right side bearing
~~~
