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
#   Templates by TEMPLATED
#   templated.co @templatedco
#   Released for free under the Creative Commons Attribution 3.0 license (templated.co/license)
#   Modified to be used with PageBotNano
# -----------------------------------------------------------------------------
#
#   Templates are functions with a normalizes attribute interface, that contain
#   patterns to replace {{anchors}} in template sources.
#
import sys
sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano_060.templates.basetemplates import BaseTemplates
from pagebotnano_060.toolbox import path2DirectoryName, path2CoreFileName
from pagebotnano_060.toolbox.markdown import parseMarkdown

class TemplatedBase(BaseTemplates):
    """    
    The TemplatedBase is the abstract class, supporting the specific templates
    classes for each of the supported https://templated.co template structure, 
    Modified to be used with PageBotNano.
    """

