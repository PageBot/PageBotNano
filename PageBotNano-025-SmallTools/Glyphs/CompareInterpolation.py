#
# Rough compare interpolations between glyph layers
#
# Example output:
# (u'A', 'Layer', u'Bold', 'contour', 0, 'has not same amount of points', 12, 'as layer', u'Regular', 40)
# (u'A', 'Layer', u'Bold', 'contour', 1, 'has not same amount of points', 40, 'as layer', u'Regular', 12)
# (u'A', 'Layer', u'Bold Italic', 'contour', 0, 'has not same amount of points', 12, 'as layer', u'Regular', 40)
# (u'A', 'Layer', u'Bold Italic', 'contour', 1, 'has not same amount of points', 40, 'as layer', u'Regular', 12)
# (u'A', 'Layer', None, 'contour', 0, 'has not same amount of points', 46, 'as layer', u'Regular', 40)
#
# Run this as Glyphs macro on the current selected font
#
# Get the current open font object
f = Glyphs.font
for g in f.glyphs: # For all glyph ovbjects in the current font
	# Try to find the Regular layer for each glyph and store here
	regularLayer = None
	for layer in g.layers: # = different styles of a glyph
		#print(g.name, layer.name)
		if layer.name == 'Regular': # 
			regularLayer = layer
			break # We found it

	assert regularLayer is not None # Make sure it exists
	# Run through the layers again to compare to Regular
	for layer in g.layers:
		if layer.name == regularLayer.name:
			continue # No need to compare to itself
	#weightLayer = g.layers['Bold']
	#print(g.name, weight.LSB, weight.width, weight.RSB)
	#weight.LSB -= 200
		# Test if the number of contours is the same
		if len(layer.paths) != len(regularLayer.paths):
			print(g.name, 'Layer', layer.name, 'has not same amount of contours as layer', regularLayer.name)
			continue # No need to check any further
		# For all contours 
		for cIndex, contour in enumerate(layer.paths):
			# Find the corresponding contour in the Regular layer
			regContour = regularLayer.paths[cIndex]
			# Test if the contours have the same amount of points
			if len(contour.nodes) != len(regContour.nodes):
				print(g.name, 'Layer', layer.name, 'contour', cIndex, 'has not same amount of points', len(contour.nodes), 'as layer', regularLayer.name, len(regContour.nodes))
			# This would be the way to extend the script, 
			# drilling deeper to test if all point types 
			# are the same and if the contour rotation direction 
			# is the same.					
			#for p in contour.nodes:
		    #   ...
