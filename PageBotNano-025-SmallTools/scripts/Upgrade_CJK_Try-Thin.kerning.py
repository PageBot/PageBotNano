#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import sys
if __name__ == "__main__":
   sys.path.insert(0, "../")
from pagebotnano_025 import openFont

font = openFont("../masters/Upgrade_CJK_Try-Thin.ufo") 

def k(f, pair, value):
   f.kerning[pair] = value


font.save()
font.close()
