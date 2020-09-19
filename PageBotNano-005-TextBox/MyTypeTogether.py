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
#   MyTypeTogether.py
#
#   This MyTypeTogether.py shows an example how to import
#   existing libaries, that contain knowledge about document,
#   pages and the elements on the pages.
#   Several templates are defined as methods of the TypeSpecimen class,
#   using standard Text and TextBox elements.
#
from random import random, shuffle
import drawBot # Used to get the size of a FormattedString.
# From the PageBotNano library we import the classes (=object factories)
# that we need for creating the type specimen.
# Classes can be recognised by their initial capital name.
from pagebotnano_005.document import Document
from pagebotnano_005.elements import Rect, Text, TextBox
from pagebotnano_005.toolbox.loremipsum import loremipsum
from pagebotnano_005.constants import LAYOUT_GRID, LAYOUT_WRAPPED

PAD = 48 # Padding of the page on all sides
G = 8 # Gutter between columes, also used as unit for small measures.

fonts = ( # Assuming these exist and are available by DrawBot.
    'ACaslonPro-Regular',
    'ACaslonPro-Italic',
    'ACaslonPro-Semibold',
    'ACaslonPro-SemiboldItalic',
    'ACaslonPro-Bold',
    'ACaslonPro-BoldItalic',
)
fontsXXX = ( # Otherwise define the name of other styles that exist in the OSX.
    'Georgia', 
    'Georgia-Bold', 
    'Georgia-Italic', 
    'Georgia-BoldItalic', 
)
labelFont = 'ACaslonPro-Regular' # Label font can be different from selected font.

# Define the styles as used by all pages.
# In the font is None, it needs to be redefined by the method that uses it.
titleStyle = dict(font=None, fontSize=14)
pageNumberStyle = dict(font=labelFont, fontSize=14, align='right')
lineStyle = dict(font=None, fontSize=None, lineHeight=None)
# Specific styles by some elements.
labelTabStyle = dict(font=labelFont, fontSize=9, lineHeight=9, tabs=((24, 'right'), (24+G, 'left')))
labelStyle = dict(font=labelFont, fontSize=9, lineHeight=9)
glyphStyle = dict(font=None, fontSize=36, lineHeight=38, tracking=0)
typeTogetherStyle = dict(font=None, fontSize=80, align='center')

def setFontStyle(font):
    """Set the font for all styles that need one."""
    titleStyle['font'] = font
    lineStyle['font'] = font
    glyphStyle['font'] = font

class TypeSpecimen(Document):
    """Inheriting from Document, the TypeSpecimen behaves like one, but then
    with additional methods to fill pages as a type speciment.
    Some pages feature just one font (in which case the font name is on top
    of the top hgorizontal ruler. 
    Other pages show a free/random set of glyphs in various fonts. In that 
    case the font name is omitted.
    """
    def __init__(self, fonts, **kwargs):
        """Pass all keyword arguments on to the parent class. 
        """
        Document.__init__(self, **kwargs)
        self.fonts = fonts # List of font DrawBot names for this specimen.
        
    def initializePage(self, page, font=None):
        """Initialize the basic elements on @page.
        Add the name of the font (if defined), horizontal ruler on top and bottom.
        Add a pagenumber.
        """
        pw = page.w-2*PAD # Usable page width
        if font is not None: # If the font is defined, then add the name on top.
            fs = Text.FS(font, **titleStyle)
            e = Text(fs, x=PAD, y=page.h-PAD*4/5) # Create the text element.
            page.addElement(e) # Add the element to the page.
        # Add line as thin rectangle to avoid making Line class here
        e = Rect(x=PAD, y=page.h-PAD, w=pw, h=1, fill=0)
        page.addElement(e)
        e = Rect(x=PAD, y=PAD, w=pw, h=1, fill=0)
        page.addElement(e)
        # Add page number
        fs = Text.FS(str(page.pn), **pageNumberStyle)
        e = Text(fs, x=page.w-PAD, y=PAD*2/3)
        page.addElement(e)

    def makeWaterfall(self, page, font, s, fontSizes=None):
        """Draw a waterfall on the page for a single font in a defined
        range of sizes.
        """
        pw = page.w-2*PAD # Usable page width (without the padding)
        ph = page.h-2*PAD # Usable page height
        if fontSizes is None: # If no font sizes defined, then use this range.
            fontSizes = (
                8,9,10,11,12,13,14,15,16,18,20,22,24,26,28,32,36,40, 44,48,52,56
            )
        fs = Text.FS('') # Start with an empty FormattedString.
        for fontSize in fontSizes:
            lineStyle['fontSize'] = fontSize # Set the current font size of the line
            lineStyle['lineHeight'] = fontSize 
            labelTabStyle['lineHeight'] = fontSize * 1.2 # Label defines lineHeight
            # Composes the one line of the waterfall
            fs += Text.FS('\t%dpt\t' % fontSize, **labelTabStyle)
            fs += Text.FS(s+'\n', **lineStyle) # Add a newline in the line style
        # Make a TextBox element with all lines combines, fitting the usable
        # space of the page, which white background.
        e = TextBox(fs, x=PAD, y=PAD+8, w=pw, h=ph-24, fill=1)
        page.addElement(e)
        
    def makeIncrementalTextSamples(self, page, font, s, fontSizes=None):
        """Make a page with text samples that increase in side, all with the
        full width of the page. Make just one page, so it will only fit the
        (smallest) sizes. The rest of the size range is then ignored.
        """
        pw = page.w-2*PAD # Usable page width
        ph = page.h-2*PAD # Usable page height
        if fontSizes is None: # If no font sizes defined, then use this range.
            fontSizes = (
                8,9,10,11,12,13,14,15,16,18,20,22,24,26,28,32,36,40,44,48,52,56
            )
        y = ph-PAD/2
        for fontSize in fontSizes:
            lineHeight = fontSize * 1.2
            lineStyle['fontSize'] = fontSize # Set the style to this size
            lineStyle['lineHeight'] = lineHeight # To be sure, in case label is behind
            labelStyle['lineHeight'] = lineHeight # Label defines lineHeight
            # Make a FormattedString with an initial label, showing the size.
            fs = Text.FS('%dpt\n' % fontSize, **labelStyle)
            # Then add a wrapping text and make a TextBox element. This layout
            # is done in separate elements, so we can ignote the overfill, 
            # showing the same amount of lines for each size sample.
            fs += Text.FS(s+'\n', **lineStyle)
            e = TextBox(fs, x=PAD, y=y, w=pw, h=lineHeight*7, fill=1)
            page.addElement(e)
            # Calculate the vertical position of the next text box, depending
            # no a number of line heights of this sample size
            y -= lineHeight*8+G
            # If the vertical position drop from the page padding at the bottom,
            # then break the loop. We only show one page here.
            if y < PAD:
                break
                
    def makeSingleTextBoxGlyphSet(self, page, font): 
        """Old version with a single TextBox
        TODO: Overflow does not seem to work right: only first glyph is cut.
        """
        pw = page.w-2*PAD # Usable page width
        ph = page.h-2*PAD # Usable page height
        fs = Text.FS('', **glyphStyle)
        drawBot.font(self.font[0]) # Just take the first one of the list
        #glyphNames = []
        #for glyphName in drawBot.listFontGlyphNames():
        #    glyphNames.append(glyphName)
        #    glyphNames.append('space')
        glyphNames = drawBot.listFontGlyphNames()
        fs.appendGlyph(*glyphNames)
        pc = 0
        while pc < 4 and fs:
            if pc > 0:
                page = typeSpecimen.newPage()
                self.initializePage(page)
            e = TextBox(fs, x=PAD, y=PAD+8, w=pw, h=ph-24, fill=1)
            page.addElement(e)
            fs = e.getOverflow(fs, w=PAD, h=ph-24, doc=self)
            pc += 1
    
    def makeGlyphSet(self, page, font):
        """Fill the (self.w, self.h) with a number of children TextBoxes,
        positioned in lines and spaced by fixed distance, using the glyph
        width, ignore kerning.
        Some visual options: 
        - For every font in self.fonts, show the glyph set.
        - Glyphset by cmap of the font, or by string or random selection.
        - Glyph can be black or random selection of a set of colors.
        - Layout in a fixed width/height grid, or as wrapping lines.
        - Size of the glyph boxes is fixed (number in width/height that
        fit on the page) or fixed amount that scales to fit.
        """     
        pw = page.w-2*PAD # Usable page width
        ph = page.h-2*PAD # Usable page height

        drawBot.font(font) # Set the font to DrawBot current
        glyphNames = drawBot.listFontGlyphNames() # so we can get the set of glyph names.

        tracking = glyphStyle['fontSize']/4 # Extra fixed space between the glyphs.
        leading = 1.3 # Leading between the lines
        x = y = 0 # Start at top left of the page (our y goes down).
        for glyphName in glyphNames: # All glyph names in the current font
            fs = Text.FS('', **glyphStyle) # Make a new FormattedStringin this style
            fs.appendGlyph(glyphName) # And add the current glyph name to it.
            tw, th = drawBot.textSize(fs) # Measure the size of the FormattedString
            e = Text(fs, x=x+PAD, y=ph-y) # Text element with single glyph
            page.addElement(e) # And add it to the page
            x += tw + tracking # Calculate the horizontal position of the next box
            if x > pw - PAD: # If it runs over the right padding of the page
                x = 0 # Start on the left of the next line
                y += glyphStyle['fontSize'] * leading # New vertical position of the line
            if y > ph - glyphStyle['fontSize'] * leading: # If vertical is running over bottom
                page = typeSpecimen.newPage() # Then create a new page 
                self.initializePage(page, font) # and initialize it.
                x = y = 0 # Reset the position, starting on top-left of the new page.

    def makeTypeTogether(self, page, fonts):
        """This template makes an automated version of a TypeTogether sample page.
        """
        paperColor = 80/100, 80/100, 73/100 # Measure from the original image
        # Add a rectangle element in the paper color, spanning the full page.
        e = Rect(x=0, y=0, w=page.w, h=page.h, fill=paperColor)
        page.addElement(e)

        pw = page.w-2*PAD # Usable page width
        ph = page.h-3*PAD # Usable page height
        glyphNameByFont = None # Collect a set of glyphs that exist in all fonts.
        for font in fonts:
            drawBot.font(font) # Just take the first one of the list
            glyphNames = drawBot.listFontGlyphNames() # Glyph names for this font
            if glyphNameByFont is None: # If it is the first, take the list as start
                glyphNameByFont = set(glyphNames)
            else: # Otherwise, do an intersection, so we only keep was is in all fonts.
                glyphNameByFont = glyphNameByFont.intersection(glyphNames)
        glyphNameByFont = list(glyphNameByFont) # Convert the set into an unsorted list
        glyphNameByFont2 = [] # Storage of the filtered glyph names.
        # Filter the glyphset to what you want.
        for glyphName in glyphNameByFont:
            # Only select glyphs that have an initial capital.
            if glyphName[0] == glyphName[0].upper(): 
                glyphNameByFont2.append(glyphName)
        shuffle(glyphNameByFont2) # Force random order of the glyph name list
        fIndex = 0 # Index in font list
        gIndex = 0 # Index in the glyphNameByFont
        cIndex = 0 # Index in the color range
        # Hard coded number of columns and rows that distribute evenly on the page size.
        # This could be made more generic, calculating the optimal number from the
        # font size and the page size. For now this is a hand picked value.
        cols = 6 # Number of columns in the grid
        rows = 6 # Number of rows
        colors = ( # Original colors of the example, converted to 0..1
            (96/100, 24/100, 10/100),
            (23/100, 41/100, 56/100),
            (13/100, 11/100, 9/100),
            (41/100, 23/100, 56/100),
        )
        for iy in range(rows): # For all the rows on the page
            for ix in range(cols): # For all the columns on the page
                typeTogetherStyle['fill'] = colors[cIndex] # Cycle through the colors
                typeTogetherStyle['font'] = fonts[fIndex] # Cycle through the fonts
                fIndex += 1 # Calculate the index of the next font
                if fIndex == len(fonts): # If running over the amount, then reset to 0
                    fIndex = 0
                cIndex += 1 # Calculate the index of the next color
                if cIndex == len(colors): # If running over the amount, then reset to 0
                    cIndex = 0
                fs = Text.FS('', **typeTogetherStyle) # New FormattedString, using the style
                fs.appendGlyph(glyphNameByFont2[gIndex]) # Append the next glyph in the list
                # Tweaked calculation of the (x, y) position of this letter.
                # Since the style makes the letter position centered, we add
                # 1/2 of the index to calculate the position of cols and rows.
                x = (ix + 0.5) * pw / cols + PAD
                y = ph - (iy + 0.5) * ph / rows + PAD
                e = Text(fs, x=x, y=y) # Make a TextBox element with this single glyph
                page.addElement(e) # Add it to the page
                gIndex += 1 # Calculate the index of the next glyph

# Create a document with default A4-portrait size.
typeSpecimen = TypeSpecimen(fonts) # Execute the class/factory by adding "()"

# Single page template that uses all fonts in the list
page = typeSpecimen.newPage()
typeSpecimen.initializePage(page)
typeSpecimen.makeTypeTogether(page, fonts)

if 1: # Simple switch to turn this type of page on/off 
    for font in fonts:
        setFontStyle(font)
        page = typeSpecimen.newPage()
        typeSpecimen.initializePage(page, font)
        typeSpecimen.makeWaterfall(page, font, 'Hamburgefonstiv')

if 1: # Simple switch to turn this type of page on/off 
    for font in fonts:
        setFontStyle(font)
        page = typeSpecimen.newPage()
        typeSpecimen.initializePage(page, font)
        lorem = loremipsum().replace('\n', ' ')
        typeSpecimen.makeIncrementalTextSamples(page, font, lorem)

if 1: # Simple switch to turn this type of page on/off 
    for font in fonts:
        setFontStyle(font)
        page = typeSpecimen.newPage()
        typeSpecimen.initializePage(page, font)
        typeSpecimen.makeGlyphSet(page, font)

# Build the document, all pages and their contained elements.
typeSpecimen.build() 

# Save the document as PDF
typeSpecimen.export('_export/MyTypeTogether.pdf')

print('Done 005')
