# GlyphsApp script

# Get a list of all open fonts
fonts = Glyphs.fonts

# Make a set of all glyphs names together, holding unique names. 
# Use it as a set() instead of an ordered list, so there 
# won't be double names when adding them.
allGlyphNames = set()

for font in fonts: # For all open fonts in the editor.
	for gName in font.glyphs.keys(): # For all glyph names in this font
		# Add this name to the set. Not need to check for doubles
		# as the set() will ignore that. It will only hold
		# unique names.
		allGlyphNames.add(gName) 
		
# Now we have a combined set of all names in all fonts.
# Loop through all fonts again and test the existing glyphs
# in each font against the total set of names
for font in fonts: 
	# Get the list of glyph names in this font
	fontGlyphNames = font.glyphs.keys() 
	# Test the total list against the font 
	for gName in sorted(allGlyphNames): 
		# If it does not exist in the font, 
		# then print it is missing
		if not gName in fontGlyphNames: 
			print('Missing "%s" in font "%s"' % (gName, font.familyName))
