#MenuTitle: CallBack Test
# -*- coding: utf-8 -*-
__doc__="""
Do several adjustments to the font and current glypg.
"""
import vanilla
from vanilla import EditText, TextBox, Button, CheckBox, TextEditor

class DemoGlyphsEvents:
	def __init__( self ):
		# Window 'self.w':
		w  = 300
		h = 300
		windowWidthResize  = 200 # user can resize width by this value
		windowHeightResize = 500   # user can resize height by this value
		self.w = vanilla.FloatingWindow(
			(w, h ), # default window size
			"CallBack Test", # window title
			minSize = ( w, h-100 ), # minimum size (for resizing)
			maxSize = ( w + windowWidthResize, h + windowHeightResize ), # maximum size (for resizing)
			autosaveName = "com.typetr.DemoGlyphsEvents.mainwindow" # stores last window position and size
		)
		M = 10
		y = 30
		# UI elements:
		self.w.tabWidth = EditText( (M, y, w/4-M-M, 20), "650", sizeStyle='small' )
		self.w.tabWidthLabel = TextBox( (w/4, y+4, w/2, 20), "Tab width", sizeStyle='small' )
		
		y += 30
		# Run Button:
		self.w.runButton = Button((w/2, y, -M, 24), "Check/fix tab widths", sizeStyle='regular', callback=self.runButtonCallback)
		self.w.doFix = CheckBox((M, y, -M, 24), "Fix errors", value=False, sizeStyle='regular' )
		
		y += 40
		self.w.reporter = TextEditor((M, y, -M, -M), readOnly=True)
		
	
		self.w.setDefaultButton( self.w.runButton )
				
		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()
		
		# establish callbacks:
		
		Glyphs.addCallback( self.drawforeground, DRAWFOREGROUND )
		Glyphs.addCallback( self.drawbackground, DRAWBACKGROUND )
		Glyphs.addCallback( self.drawinactive, DRAWINACTIVE )
		Glyphs.addCallback( self.documentopened, DOCUMENTOPENED )
		Glyphs.addCallback( self.documentactivated, DOCUMENTACTIVATED )
		Glyphs.addCallback( self.documentwassaved, DOCUMENTWASSAVED )
		Glyphs.addCallback( self.documentexported, DOCUMENTEXPORTED )
		Glyphs.addCallback( self.documentclosed, DOCUMENTCLOSED )
		Glyphs.addCallback( self.tabdidopen, TABDIDOPEN )
		Glyphs.addCallback( self.tabwillclose, TABWILLCLOSE )
		Glyphs.addCallback( self.updateinterface, UPDATEINTERFACE )
		Glyphs.addCallback( self.mousemoved, MOUSEMOVED )
		
		print "Callbacks done."
	
	def runButtonCallback(self, sender):
		s = 'Testing all widths'
		if self.w.doFix.get():
			s += ' and fix where needed\n'
		
		try:
			tabWidth = int(self.w.tabWidth.get()) # Should be tested more
		except ValueError:
			self.w.reporter.set('Illegal width value: %s' % self.w.tabWidth.get())
			return
			
		f = Glyphs.font # Returns the current that is open in GlyphsApp
		for g in f.glyphs:
			for gStyle in g.layers:
				if '.tab' in g.name and gStyle.width != tabWidth:
					if self.w.doFix.get():
						s += 'Fixed: %s-%s: %d\n' % (gStyle.name, g.name, gStyle.width)
						gStyle.width = tabWidth
					else:
						s += 'Not tab width: %s-%s: %d\n' % (gStyle.name, g.name, gStyle.width)
						
					
		self.w.reporter.set(s)

	def drawforeground(self, layer, info):
		print "drawforeground"
		print "   layer: %s" % layer
		for dictKey in info.keys():
			print "   info > %s: %s" % ( dictKey, info[dictKey] )
			
	def drawbackground(self, layer, info):
		print "drawbackground"
		print "   layer: %s" % layer
		for dictKey in info.keys():
			print "   info > %s: %s" % ( dictKey, info[dictKey] )
			
	def drawinactive(self, layer, info):
		print "drawinactive"
		print "   layer: %s" % layer
		for dictKey in info.keys():
			print "   info > %s: %s" % ( dictKey, info[dictKey] )
			
	def documentopened(self, passedobject):
		print "documentopened"
		print "   passed object: %s" % repr(passedobject)
			
	def documentactivated(self, passedobject):
		print "documentactivated"
		print "   passed object: %s" % repr(passedobject)
			
	def documentwassaved(self, passedobject):
		print "documentwassaved"
		print "   passed object: %s" % repr(passedobject)
			
	def documentexported(self, passedobject):
		print "documentexported"
		print "   passed object: %s" % repr(passedobject)
			
	def documentclosed(self, passedobject):
		print "documentclosed"
		print "   passed object: %s" % repr(passedobject)
			
	def tabdidopen(self, tab):
		print "tabdidopen"
		print "   tab: %s" % repr(tab)
			
	def tabwillclose(self, tab):
		print "tabwillclose"
		print "   tab: %s" % repr(tab)
			
	def updateinterface(self, passedobject):
		# brings macro window to front and clears its log:
		Glyphs.clearLog()
		Glyphs.showMacroWindow()
		
		
		print "updateinterface"
		print "   passed object: %s" % repr(passedobject)
		
			
	def mousemoved(self, passedobject):
		print "mousemoved"
		print "   passed object: %s" % repr(passedobject)
	
	def cleanUp(self, sender):
		Glyphs.removeCallback( self.mousemoved, MOUSEMOVED )
		Glyphs.removeCallback( self.drawforeground, DRAWFOREGROUND )
		Glyphs.removeCallback( self.drawbackground, DRAWBACKGROUND )
		Glyphs.removeCallback( self.drawinactive, DRAWINACTIVE )
		Glyphs.removeCallback( self.documentopened, DOCUMENTOPENED )
		Glyphs.removeCallback( self.documentactivated, DOCUMENTACTIVATED )
		Glyphs.removeCallback( self.documentwassaved, DOCUMENTWASSAVED )
		Glyphs.removeCallback( self.documentexported, DOCUMENTEXPORTED )
		Glyphs.removeCallback( self.documentclosed, DOCUMENTCLOSED )
		Glyphs.removeCallback( self.tabdidopen, TABDIDOPEN )
		Glyphs.removeCallback( self.tabwillclose, TABWILLCLOSE )
		Glyphs.removeCallback( self.updateinterface, UPDATEINTERFACE )
		Glyphs.removeCallback( self.mousemoved, MOUSEMOVED )
		print sender
	
	def showWindow(self, sender):
		# brings macro window to front and clears its log:
		Glyphs.clearLog()
		Glyphs.showMacroWindow()
		print sender
		
DemoGlyphsEvents()