#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#	P A G E B O T  N A N O
#
#	Copyright (c) 2020+ Buro Petr van Blokland + Claudia Mens
#	www.pagebot.io
#	Licensed under MIT conditions
#
#	Supporting DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#	htmlcontext.py
#
import os
import codecs
import sys
sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

class HtmlContext:

	PAGE = """
<html>
	<head>
		%(head)s
	</head>
	<body>
		%(body)s
	</body>
</html>
	"""	
	def __init__(self):
		"""

		>>> from pagebotnano.document import Document
		>>> from pagebotnano.elements import Rect, Text
		>>> from pagebotnano.babelstring import BabelString
		>>> context = HtmlContext()
		>>> doc = Document(context=context)
		>>> page = doc.newPage()
		>>> padding = 40
		>>> e = Rect(padding, padding, page.w-2*padding, page.h-2*padding, fill=(1, 0.2, 1))
		>>> page.addElement(e)
		>>> style = dict(font='Georgia', fontSize=100)
		>>> bs = BabelString('Hello world', style)
		>>> e = Text(bs, padding, page.h/2, fill=(1, 0, 0))
		>>> page.addElement(e)
		>>> doc.export('_export/HtmlContext-website')
		"""
		self.newDrawing()

	def newDrawing(self):
		self.pages = []
		self.css = []
		self.style = {}
		self.newPage() # Set a current page to draw in.

	def newPage(self):
		self.page = page = dict(head='', body='')
		self.pages.append(page)

	def stroke(self, stroke, strokeWidth=None):
		if strokeWidth is not None:
			self.style['strokeWidth'] = strokeWidth
		self.style['stroke'] = stroke

	def fill(self, fill):
		self.style['fill'] = fill

	def rect(self, x, y, w, h):
		self.page['body'] += '<div width="%d"></div>' % w

	def text(self, bs, p):
		self.page['body'] += '<p>%s</p>' % bs.html

	def saveImage(self, path, multipage=True):
		"""Create folder names `path` if it does not already exist.
		"""
		if not os.path.exists(path):
			os.mkdir(path)
		else:
			assert os.path.isdir(path)
		if not path.endswith('/'):
			path += '/'
		for pIndex, page in enumerate(self.pages):
			if pIndex == 0:
				fileName = 'index.html'
			else:
				fileName = 'page%03d' % pIndex
			f = codecs.open(path+fileName, mode="w", encoding="utf-8") # Save the XML as unicode.
			f.write(self.PAGE % page)
			f.close()


if __name__ == "__main__":
	# Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]