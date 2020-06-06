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
#	This source makes it possible to import other sources
#	from this diretory/folder
#
#	Try two types of import, so we don't need to install the pagebotnano 
#	package into the Python of your system.
try:
	from constants import *
	from document import Document
	from page import Page
	from elements import Element
except (ImportError, ModuleNotFoundError):
	from pagebotnano.constants import *
	from pagebotnano.document import Document
	from pagebotnano.page import Page
	from pagebotnano.elements import Element
