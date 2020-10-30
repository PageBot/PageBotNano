
# Get the current font
f = Glyphs.font

# Make a dictionaty of all glyphs names that have components, 
# showing the amount of components
glyphsWithComponents = {}

for gName in f.glyphs.keys():
	g = f.glyphs[gName].layers[0]
	if g.components:
		glyphsWithComponents[gName] = len(g.components)
        
print(glyphsWithComponents)