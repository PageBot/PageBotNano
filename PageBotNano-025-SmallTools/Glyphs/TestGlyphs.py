#
# Run this as Glyphs macro
#
# Get the current open font object
#
# f = CurrentFont()
f = Glyphs.font # Returns the current that is open in GlyphsApp
# Print the "representation" (__repr__) of the font object
print(f)
# Shows that class name of the internal Glyphs structure: NSKVONotifying_GSFont
#print(f.__class__.__name__)
# This produces this output:
# <GSFont "Upgrade" v1.0 with 1 masters and 1 instances>
# RoboFont fonts behave like Python objects
# Now get the "A" glyph object from the f.glyphs dictionary
g = f.glyphs['A']
# Print the "representation" (__repr__) of the glyph object
print(g)
# This produces this output:
# <GSGlyph "A" with 1 layers>
print(g.__class__.__name__) # Aswers the name of the Python wrapper class NSKVONotifying_GSGlyph
# Run through all glyphs
for g in f.glyphs: # f.glyphs.keys() would answer a list of glyphnames
	# Get the first style in this glyph
	gStyle = g.layers[0]
	# Equivalent to fontParts g.leftMargin and g.rightMargin
	print(g.name, gStyle.LSB, gStyle.width, gStyle.RSB) 
