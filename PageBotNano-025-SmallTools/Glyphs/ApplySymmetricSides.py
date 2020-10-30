

DO_CHANGE = False
symmetry = ('A','I','H','O','N','M','V','W','X','Y','Z','v','w','x','z')

for f in Glyphs.fonts: # RF: AllFonts():
    foundError = False
    #for gName in sorted(f.keys()):
    for gName in sorted(symmetry):
    	for g in f.glyphs[gName].layers: # RF: for g in f:
	        # RF: g.leftMargin --> GlyphsApp: g.LSB
	        # RF: g.rightMargin --> GlyphsApp: g.RSB
        	if g.LSB != g.RSB: # They should all be symmetric identical
        		print('Before: %s: %d %d %d' % (g.name, g.LSB, g.width, g.RSB))
        	if DO_CHANGE:
        		g.LSB = g.RSB = max(g.LSB, g.RSB)
        		print('After: %s: %d %d %d' % (g.name, g.LSB, g.width, g.RSB))
        	# RF: g.changed()
        	foundError = True
        	#if abs(g.LSB - g.RSB) > 1: # Difference of one is ok.
        	#    print('%s: %d %d %d' % (g.name, g.LSB, g.width, g.RSB))
    if not foundError:
        print('All ok')
print('Done')   