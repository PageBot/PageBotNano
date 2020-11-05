#MenuTitle: CallBack Test
# -*- coding: utf-8 -*-
__doc__="""
Test Script for Callbacks
"""

import vanilla

class CallBackTest( object ):
	def __init__( self ):
		# Window 'self.w':
		windowWidth  = 250
		windowHeight = 90
		windowWidthResize  = 200 # user can resize width by this value
		windowHeightResize = 0   # user can resize height by this value
		self.w = vanilla.FloatingWindow(
			( windowWidth, windowHeight ), # default window size
			"CallBack Test", # window title
			minSize = ( windowWidth, windowHeight ), # minimum size (for resizing)
			maxSize = ( windowWidth + windowWidthResize, windowHeight + windowHeightResize ), # maximum size (for resizing)
			autosaveName = "com.mekkablue.CallBackTest.mainwindow" # stores last window position and size
		)
		
		# UI elements:
		self.w.text = vanilla.TextBox( (14, 14, -15, 14), "Watch output in Macro Window", sizeStyle='small' )
		
		# Run Button:
		self.w.runButton = vanilla.Button((-200, -20-15, -15, -15), "Open Macro Window", sizeStyle='regular', callback=self.showWindow )
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
		
CallBackTest()