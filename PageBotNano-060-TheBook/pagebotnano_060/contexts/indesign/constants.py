
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
#   constants.py
#
import sys
sys.path.insert(0, "../../..") # So we can import pagebotnano without installing.

DEFAULT_WIDTH = DEFAULT_HEIGHT = 100

JSX_LIB = """
function pbGetColor(doc, c){
    if (c.length == 4){
        colorName = "C=" + Math.round(c[0]) + " M=" + Math.round(c[1]) +" Y=" + Math.round(c[2]) + " K=" + Math.round(c[3]);  
        colorSpace = ColorSpace.cmyk;
        colorModel = ColorModel.process;
    } else {
        colorName = "R=" + Math.round(c[0]) + " G=" + Math.round(c[1]) +" B=" + Math.round(c[2]);  
        colorSpace = ColorSpace.rgb;
        colorModel = ColorModel.process;
    }
    try {
        pbColor = doc.colors.add({
            name: colorName, 
            model: colorModel,
            space: colorSpace, 
            colorValue: c});
    } 
    catch (e) {
        pbColor = doc.swatches.item(colorName);
    }
    //alert(colorName);
    return(pbColor);
}
function myScriptPath(){
    return(File(app.activeScript).parent + '/');
}
"""

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
