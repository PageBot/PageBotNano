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
from copy import copy
import drawBot

from pagebotnano.constants import FS_ATTRIBUTES, CSS_ATTRIBUTES, HTML_TEXT_TAGS

class BabelRun:
	"""Holds a plain string with a style.
	"""
	def __init__(self, s, style):
		self.s = s # Property that clear the native cache components of a string.
		self.style = style

	def copy(self):
		"""Answer a copy of self, where also the style is copied.

		>>> br = BabelRun('Hello world', dict(font='Georgia'))
		>>> br2 = br.copy()
		>>> br.s == br2.s and br.style == br2.style # Copy is equal
		True
		>>> br.style is not br2.style
		True
		"""
		return self.__class__(self.s, copy(self.style))

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

	def getMergedStyles(self):
		merged = {} # First merge equal styles for defined tags
		for style in self.styles:
			tag = style.get('tag', 'span')
			class_ = style.get('name')
			if tag in HTML_TEXT_TAGS:
				cssStyle = dict(class_=class_)
				if tag not in merged:
					merged[tag] = cssStyle
				for cssName, value in style.items():
					merged[tag][cssName] = value
		return merged

	def asString(self, compact=False):
		if compact:
			r = t = s = ''
		else:
			r = '\n'
			t = '\t'
			s = ' '
		css = ''
		for tag, style in sorted(self.getMergedStyles().items()):
			class_ = style.get('class_')
			css += tag
			if class_ is not None:
				css += '.'+class_
			css += ' {'
			for cssName, value in style.items():
				if cssName in CSS_ATTRIBUTES:
					# TODO: make better representations of the CSS value
					css += '%s%s:%s%s;%s' % (t, cssName, s, value, r)
			css += '};\n'
		return css

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
	def __init__(self, s=None, style=None, **kwargs):
		if s is None:
			s = ''
		if style is None:
			style = {}
		else:
			# Make a copy, as we are altering it with **kwargs attributes
			style = copy(style) 
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

	def append(self, bs, style=None):
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
		>>> bs2 = BabelString('(ok)')
		>>> bs.append(bs2) # Adding another BabelString
		>>> bs 
		<BabelString runs=3>
		"""
		if isinstance(bs, self.__class__):
			for run in bs.runs:
				self.runs.append(run.copy())
		else:
			if style is None:
				self.runs[-1].s += str(bs) # Undefined style, just add to last run
			else:
				self.runs.append(BabelRun(str(bs), style))
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
	def _set_fs(self, fs):
		"""In case of DrawBot.textBox a DrawBot.FormattedString is answered.
		An “incomplete” BabelString is constructed by the DrawBotContext,
		because we cannot reconstruct the source of the string. But the 
		DrawBot.FormattedString can still be used for placement in Text
		and TextBox when doc.context is a DrawBotContext.
		"""
		self._fs = fs
	fs = property(_get_fs, _set_fs)

	def _get_html(self):
		"""Property that creates a new HTML string representation of self,
		from the current set of runs, if the cached value self._html
		does not already exist. Otherwise just answer the cached HTML string.

		>>> bs = BabelString('Hello world', dict(tag='h1', name='top'))
		>>> bs.html
		'<h1 class="top">Hello world</h1>'
		>>> bs = BabelString('Hello world', dict(name='top'))
		>>> bs.html # Default tag name is <span>
		'<span class="top">Hello world</span>'
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

		>>> bs = BabelString('Hello world', dict(font='Georgia', fontSize=24, tag='h1', name='top'))
		>>> bs.css
		<Css style=1>
		>>> bs.css.asString(compact=True)
		'h1.top {font:Georgia;fontSize:24;};\\n'
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