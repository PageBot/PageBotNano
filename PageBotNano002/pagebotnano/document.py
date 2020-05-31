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
#	document.py
#
#	This source contains the class with knowledge about a generic document.
#
import os # Import standard Python library to create the _export directory
import sys
sys.path.insert(0, "..") # So we can import pagebotnano without installing.
import drawBot

from pagebotnano.constants import *

class Document:
	# Class names start with a capital. See a class as a factory
	# of document objects (name spelled with an initial lower case.)
	
	def __init__(self, w=None, h=None):
		"""This is the "constructor" of a Document instance (=object).
		It takes two attributes: `w` is the general width of pages and
		`h` is the general height of pages.
		If omitted, a default A4 page size is taken.

		>>> doc = Document()
		>>> doc
		I am a Document(w=595, h=842)
		"""
		if w is None: # If not defined, take the width of A4
			w, _ = A4
		if h is None: # If not defined, then take the height of A4
			_, h = A4
		# Store the values in the document instance.
		self.w = w
		self.h = h

	def __repr__(self):
		# This method is called when print(document) is executed.
		# It shows the name of the class, which can be different, if the
		# object inherits from Document.
		return 'I am a %s(w=%d, h=%d)' % (self.__class__.__name__, self.w, self.h)

	def export(self, path):
		"""Export the document into the _export folder.

		"""
		if path.startswith(EXPORT_DIR) and not os.path.exists(EXPORT_DIR):
			os.mkdir(EXPORT_DIR)
		# Now let DrawBot do its work, creating the page and saving it.
		drawBot.newPage(self.w, self.h)
		# FOr now to have something visible
		drawBot.fill(0.2)
		drawBot.rect(0, 0, self.w, self.h)
		fs = drawBot.FormattedString('My specimen', font='Georgia', fontSize=80, fill=1)
		drawBot.text(fs, (50, self.h-100))
		drawBot.saveImage(path)

if __name__ == "__main__":
    import doctest
    doctest.testmod()[0]
