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
#	book.py
#
import os # Import standard Python library to create the _export directory
import sys
from random import random
sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano.constants import CENTER, LEFT
from pagebotnano.publications.publication import Publication
from pagebotnano.document import Document
from pagebotnano.elements import Rect, Text, TextBox, Image
from pagebotnano.babelstring import BabelString

class Book(Publication):
	"""A Book publication takes a volume of text/imges source
	as markdown document, composing book pages and export as
	PDF document.

	>>> from pagebotnano.elements import Rect, Text
	>>> from pagebotnano.constants import A5
	>>> from pagebotnano.toolbox.loremipsum import loremipsum, randomName, randomTitle
	>>> w, h = A5
	>>> title = randomTitle()
	>>> author = randomName()
	>>> content = (loremipsum() + ' ') * 50
	>>> imagePath = '../../../resources/images/cookbot1.jpg'
	>>> pub = Book(w=w, h=h, title=title, author=author, content=content, coverImagePath=imagePath)
	>>> pub.export('_export/Book.pdf')
	"""
	MAX_PAGES = 1000
	
	def __init__(self, w, h, title, author, content, coverImagePath=None,
		coverColor=None):
		Publication.__init__(self, w, h)
		self.title = title
		self.author = author
		self.content = content
		self.coverImagePath = coverImagePath
		if coverColor is None:
			coverColor = random()*0.3, random()*0.1, random()*0.4 # Random dark blue
		self.coverColor = coverColor

	def compose(self):
		"""This is the core of a publication, composing the specific
		content of the document. The compose method gets called
		before building and exporting the self.doc document.
		"""
		fontSize = 11
		headSize = fontSize*1.5
		titleSize = 36
		subTitleSize = titleSize * 0.5
		pad = 48

		titleStyle = dict(font='Georgia-Bold', 
			lineHeight=titleSize*1.1, 
			fontSize=titleSize,
			align=CENTER,
			fill=1, # White title on dark cover background
		)
		subTitleStyle = dict(font='Georgia-Italic',
			paragraphTopSpacing=subTitleSize/2,
			lineHeight=subTitleSize*1.2, 
			fontSize=subTitleSize,
			align=CENTER,
			fill=1, # White title on dark cover background
		)
		headStyle = dict(font='Georgia', 
			lineHeight=headSize*1.3, 
			fontSize=headSize,
			fill=0, # Black text
		)
		subHeadStyle = dict(font='Georgia-Italic', 
			lineHeight=headSize*0.8*1.4, 
			fontSize=headSize*0.8,
			fill=0, # Black text
		)
		bodyStyle = dict(font='Georgia', 
			lineHeight=fontSize*1.4, 
			fontSize=fontSize,
			fill=0, # Black text
		)
		pageNumberStyle = dict(
			font='Georgia', 
			fontSize=10,
			fill=0, # Black text
			align=CENTER, 
		)
		# Make the cover page.
		page = self.doc.newPage()

		# Fill the cover page with a random dark color
		e = Rect(0, 0, page.w, page.h, fill=self.coverColor) # Dark cover color
		page.addElement(e) 

		# Add title and author, centered on top-half of the cover.
		titleBs = BabelString(self.title+'\n', titleStyle)
		authorBs = BabelString(self.author, subTitleStyle)
		bs = titleBs + authorBs
		e = TextBox(bs, x=pad/2, y=page.h/2, w=page.w-pad, h=page.h/2-pad)
		page.addElement(e)

		if self.coverImagePath is not None: # Only if not defined.
			e = Image(self.coverImagePath, x=pad, y=pad, w=page.w-2*pad)
			page.addElement(e)

		# Make “French” “Voordehandse” page.
		page = self.doc.newPage()
		# CENTER text alignment overwrites the value in headStyle.
		# fontSize overwrites the value in headStyle
		bs = BabelString(self.title+'\n', headStyle, fontSize=fontSize, align=CENTER)
		e = Text(bs, x=page.w/2, y=page.h*4/5)
		page.addElement(e)

		# Make Title page.
		page = self.doc.newPage()
		bs = BabelString(self.title+'\n', headStyle, align=CENTER)
		bs.append(BabelString(self.author, subHeadStyle, align=CENTER))
		e = Text(bs, x=page.w/2, y=page.h*3/4)
		page.addElement(e)

		# Make content pages
		bs = BabelString(self.title+'\n\n', headStyle)
		bs.append(BabelString(self.content, bodyStyle, align=LEFT))
		for n in range(self.MAX_PAGES):
			page = self.doc.newPage()

			# Add text element with page number
			pn = BabelString(str(page.pn), pageNumberStyle)
			e = Text(pn, page.w/2, pad/2)
			page.addElement(e)

			# Add text element with the main text column of this page
			e = TextBox(bs, x=pad, y=pad, w=page.w-2*pad, h=page.h-2*pad)
			page.addElement(e)

			# If there is overflow on this page, continue looping creating
			# as many pages as needed to fill all the text in self.content.
			# Otherwise break the loop, as we are done placing content.
			bs = e.getOverflow(bs, doc=self.doc)
			# Test on this “incomplete” BabelString, as it only has a cached FS
			if not bs.fs:
				break
if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]