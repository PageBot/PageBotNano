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
import sys

if __name__ == "__main__":
    sys.path.insert(0, "../..") # So we can import pagebotnano without installing.
  
from pagebotnano.publications.publication import Publication
from pagebotnano.publications.book import Book
