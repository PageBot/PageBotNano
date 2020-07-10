#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#   P A G E B O T  N A N O
#
#   Copyright (c) 2020+ Buro Petr van Blokland + Claudia Mens
#   www.pagebot.io
#   Licensed under MIT conditions
#
#   Supporting DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#   This source makes it possible to import other sources
#   from this directory/folder
#
#   Try two types of import, so we don't need to install the pagebotnano 
#   package into the Python of your system.
#
import sys # Import access to some deep Python functions
sys.path.insert(0, "..") # So we can import pagebotnano003 without installing.

from pagebotnano_003.constants import *
from pagebotnano_003.document import Document
from pagebotnano_003.page import Page
from pagebotnano_003.elements import Element
