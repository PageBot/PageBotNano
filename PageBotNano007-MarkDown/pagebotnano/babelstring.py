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
#	babelstring.py
#
import sys
sys.path.insert(0, "..") # So we can import pagebotnano without installing.
import drawBot

from pagebotnano.constants import FS_ATTRIBUTES

class BabelRun:
	"""Holds a plain string with a style.
	"""
	def __init__(self, s, style):
		self.s = s # Property that clear the native cache components of a string.
		self.style = style

class Css:
	"""Holds a set of styles for the BabelString. Capable of exporting 
	into standard css syntax.
	"""
	def __init__(self):
		self.styles = []

	def append(self, style):
		self.styles.append(style)

	def __repr__(self):
		return '<%s style=%s>' % (self.__class__.__name__, len(self.styles))

class BabelString:
	"""The BabelString is a wrapper around native string formats, such as
	DrawBot.FormattedString. While supporting the full API (=interface)
	of a FormattedString, it can also support other formats, such as HTML/CSS
	when text comes from a markdown file or should generate HTML/CSS.

	>>> bs = BabelString('Hello world', dict(font='Georgia', fontSize=24, name='h1'))
	>>> bs
	<BabelString runs=1>
	>>> bs.fs # Generates a DrawBot.FormattedString
	Hello world
	>>> bs += 's' # Add to the last run, no style change. Reset DrawBot cache.
	>>> bs.fs # Generates a new DrawBot.FormattedString
	Hello worlds
	>>> bs.append(' and other planets', dict(font='Georgia-Bold', fontSize=18))
	>>> bs # This added a new run
	<BabelString runs=2>
	>>> bs.fs, bs.fs.__class__.__name__ # New DrawBot.FormattedString created.
	(Hello worlds and other planets, 'FormattedString')
	"""
	def __init__(self, s, style=None, **kwargs):
		if style is None:
			style = {}
		for name, value in kwargs.items():
			style[name] = value
		self.runs = [] # List of BabelRun instances.
		self.append(s, style)
		self.reset() # Initialize storage of native cached formatted strings 

	def __repr__(self):
		return '<%s runs=%d>' % (self.__class__.__name__, len(self.runs))

	def __add__(self, s):
		"""Add `s` to self. If `s` is another BabelString, then copy all of
		its runs to self.runs. If `s` is a string then append it to the last
		run (inheriting the current style). Otherwise convert `s` to a string
		and the add it to the last run.

		>>> bs = BabelString('Hello world')
		>>> bs += 's and other planets' # Adding calls the self.__add__ method.
		>>> bs.fs
		Hello worlds and other planets
		"""
		if isinstance(s, self.__class__):
			for run in s.runs:
				self.append(run.s, run.style)
		elif isinstance(s, str):
			self.append(s)
		else:
			self.append(str(s))
		return self

	def append(self, s, style=None):
		"""Append the string s to self. If not style is defined, then just add
		the `s` to the last run (inheriting the current style).
		Otherwise create a new BabelRun to store that `s` string with the style.

		>>> bs = BabelString('Hello world')
		>>> bs
		<BabelString runs=1>
		>>> bs.append('s') # No style defined, does not create a new run
		>>> bs
		<BabelString runs=1>
		>>> bs.append(' and other worlds', dict(font='Georgia'))
		>>> bs # Created a new run
		<BabelString runs=2>
		"""
		assert isinstance(s, str)
		if style is None:
			self.runs[-1].s += s # Undefined style, just add to last run
		else:
			self.runs.append(BabelRun(s, style))
		self.reset()

	def reset(self):
		self._fs = None # Storage of DrawBot.FormattedString
		self._html = None # Storage of html string representation.
		self._css = None # Storage Css instance.

	def _getFSStyle(self, style):
		"""Answer a style dict that only contains names that are allowed 
		in the DrawBot.FormattedString attributes.
		"""
		fsStyle = {}
		for name, value in style.items(): # Only copy what is allowed in FS
			if name in FS_ATTRIBUTES:
				fsStyle[name] = value
		return fsStyle

	def _get_fs(self):
		"""Property that creates a new DrawBot.FormattedString from the
		current set of runs, if the cached value self._fs does not already
		exist. Otherwise just answer the cached value.

		>>> bs = BabelString('Hello world', dict(font='Georgia'))
		>>> bs.fs, isinstance(bs.fs, drawBot.FormattedString().__class__)
		(Hello world, True)
		"""
		if self._fs is None:
			self._fs = fs = drawBot.FormattedString()
			for run in self.runs:
				fs.append(drawBot.FormattedString(run.s, **self._getFSStyle(run.style)))
		return self._fs
	fs = property(_get_fs)

	def _get_html(self):
		"""Property that creates a new HTML string representation of self,
		from the current set of runs, if the cached value self._html
		does not already exist. Otherwise just answer the cached HTML string.

		>>> bs = BabelString('Hello world', dict(tag='h1', name='top'))
		>>> bs.html
		'<h1 class="top">Hello world</h1>'
		"""
		if self._html is None:
			tags = []
			self._html = ''
			for run in self.runs:
				tag = None
				if 'tag' in run.style:
					tag = run.style['tag']
				else:
					tag = 'span'
				self._html += '<' + tag
				if 'name' in run.style:
					self._html += ' class="%s"' % run.style['name']
				self._html += '>%s</%s>' % (run.s, tag)

		return self._html
	html = property(_get_html)

	def _get_css(self):
		"""Property that creates a new Css instance of self,
		from the current set of runs, if the cached value self._html
		does not already exist. Otherwise just answer the cached Css instance.

		>>> bs = BabelString('Hello world', dict(tag='h1', name='top'))
		>>> bs.css, isinstance(bs.css, Css)
		(<Css style=1>, True)
		"""
		if self._css is None:
			self._css = Css()
			for run in self.runs:
				self._css.append(run.style)
		return self._css
	css = property(_get_css)

if __name__ == "__main__":
	# Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]