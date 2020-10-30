# type your Python code here and press cmd+Return to run.


try:
    Glyphs
except NameError:
    print('Make test class Glyphs')
    class TestGFont(object):
        def __init__(self):
            self.copyright = 'Copyright test notice.'
            self.familyName = 'MyFamileName'
            self.designer = 'Me'
            self.designerURL = 'www.me.com'
            self.manufacturer = 'The Foundry'
            self.manufacturerURL = 'www.thefoundry.com'
    class TestGlyphs(object):
        def __init__(self):
            self.font = TestGFont()
    Glyphs = TestGlyphs()

class G2RF_Glyph(object):
    def __init__(self, gg):
        self.gg = gg
    

class G2RF_Info(object):
    def __init__(self, gf):
        self.gf = gf
    
    def _get_copyright(self):
        return self.gf.copyright
    def _set_copyright(self, copyright):
        self.gf.copyright = copyright
    copyright = property(_get_copyright, _set_copyright)
    
    def _get_familyName(self):
        return self.gf.familyName
    def _set_familyName(self, familyName):
        self.gf.familyName = familyName
    familyName = property(_get_familyName, _set_familyName)
                    
    def _get_designer(self):
        return self.gf.designer
    def _set_designer(self, designer):
        self.gf.designer = designer
    designer = property(_get_designer, _set_designer)
    
    def _get_designerURL(self):
        return self.gf.designerURL
    def _set_designerURL(self, designerURL):
        self.gf.designerURL = designerURL
    designerURL = property(_get_designerURL, _set_designerURL)
                    
    def _get_manufacturer(self):
        return self.gf.manufacturer
    def _set_manufacturer(self, manufacturer):
        self.gf.manufacturer = manufacturer
    manufacturer = property(_get_manufacturer, _set_manufacturer)
    
    def _get_manufacturerURL(self):
        return self.gf.manufacturerURL
    def _set_manufacturerURL(self, manufacturerURL):
        self.gf.manufacturerURL = manufacturerURL
    manufacturerURL = property(_get_manufacturerURL, _set_manufacturerURL)
                    
class G2RF_Font(object):
    def __init__(self, gf):
        self.gf = gf
        self.info = G2RF_Info(gf)

    def __getitem__(self, name):
        return G2RF_Glyph(self.gf.glyphs[name])
        
def CurrentFont():
    return G2RF_Font(Glyphs.font)
  
f = CurrentFont()
print(f.info.copyright)
print(f.info.familyName)
print(f.info.designer, f.info.designerURL)
print(f.info.manufacturer, f.info.manufacturerURL)
f.info.copyright = 'Hello'
print(f.info.copyright)
#print(f['H'].gg.points) <-- ???

