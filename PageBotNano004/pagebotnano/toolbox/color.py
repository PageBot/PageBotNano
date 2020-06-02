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
#	color.py
#
#	This source contains the class with knowledge about elements that
#	can be placed on a page.
#
def asColor(r, g=None, b=None, a=None):
	"""Convert the attribute to a color tuple that is valid in DrawBot.
	"""
	if isinstance(r, (tuple, list)):
		if len(r) == 3:
			r, g, b = r
			return r, g, b, 1 # Return the color with undefined opacity.
		if len(r) == 4:
			return r # Answer the color tuple unchanged.
		print('asColor: Color "%s" for not have the right format')
		return (0, 0, 0) # Answer black in case of error
	if isinstance(r, float) and 0 <= r <= 1:
		# Fill the green and blue with the red value, if they are undefined.
		return r, g or r, b or r, a or 1 # Answer the (r, g ,b, a) 
	return None, None, None, None