
f = Glyphs.font

leftMargins = {}
rightMargins = {}
for gName in f.glyphs.keys():
	g = f.glyphs[gName].layers[0]
	lm = g.LSB
	if not lm in leftMargins:
		leftMargins[lm] = []
	leftMargins[lm].append(gName)
	
	rm = g.RSB
	if not rm in rightMargins:
		rightMargins[rm] = []
	rightMargins[rm].append(gName)
    
print("LeftMargins: %d %s" % (len(leftMargins), sorted(leftMargins.keys())))
print("RightMargins: %d %s" % (len(rightMargins), sorted(rightMargins.keys())))