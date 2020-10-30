#
# Run this as Glyphs macro

#f = Glyphs.font
#print(f)
#f.copyright += 'HELLO'
#print(f.copyright)

try:
    Glyphs
except NameError:
    
    class G2RF_FontInfo(object):
    	def __init__(self, gf):
    		self.gf = gf
		
    	def _get_copyright(self):
    		return self.gf.copyright
    	def _set_copyright(self, copyright):
    		self.gf.copyright = copyright
    	copyright = property(_get_copyright, _set_copyright)
		
    	def _get_designer(self):
    		return self.gf.designer
    	def _set_designer(self, designer):
    		self.gf.designer = designer
    	designer = property(_get_designer, _set_designer)
		
    class G2RF_Font(object):
    	def __init__(self, gf):
    		self.gf = gf
    		self.info = G2RF_FontInfo(gf)
		
    	def __repr__(self):
    		return "<%s '%s'>" % (self.__class__.__name__, self.gf.familyName)
		
def CurrentFont():
	return G2RF_Font(Glyphs.font)

# -------------------------------------------------
# Runs both in RoboFont and Glyphs

f = CurrentFont()
print(f)

print(f.info.copyright)
print(f.info.designer)

