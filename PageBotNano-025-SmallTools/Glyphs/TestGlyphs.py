#
# Run this as Glyphs macro
#
# Get the current open font object
f = Glyphs.font
# Print the "represenation" (__repr__) of the font object
print(f)
# This produces this output:
# <GSFont "Upgrade" v1.0 with 1 masters and 1 instances>
# Now get the "A" glyph object from the f.glyphs dictionary
g = f.glyphs['A']
# Print the "representation" (__repr__) of the glyph object
print(g)
# This produces this output:
# <GSGlyph "A" with 1 layers>
