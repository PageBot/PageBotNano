**(Use MacDown to view this document)**

# PageBotNano-025-SmallTools

This part of the library introduces the functionality of small tools. These are scripts of only a couple of lines, that offer a enormous help in automaticing repeating tasks in the design process.

Slightly outside the sequence of increasing Document-Page classes, the art of making small tools is an important skill for designers. It is a design process in itself, to find the relevant balance between writing one-time-only scripts with the least amount of code, and generic tools that can be used again in future projects, automatically requiring more code and an intuitive interface.

## DesignDesign.Space workshop “Coding simple scripted tools”

The sources in this chapter were developed for and during the DesignDesign.Space workshop [“Coding simple scripted tools”](https://designdesign.space/#coding-simple-scripted-tools) and [Coding tools with a user interface](https://designdesign.space/#coding-in-python2)

The first workshop is focused on very short scripts, only a couple of lines long, that automate repeating tasks in the design process. The result is a set of example scripts that can later be modified to be used in real life projects.

You can make a selection from the following exercises. And it is also possible to bring your own ideas.

## Type related tools

* Make a script that generates TTF and OTF fonts, after doing some automated operations on the outlines.
* QA stuff
* Automatic export of feature source
* OT-features and glyph replacement (exporting to Python source)
* Check on exact vertical/horizontal lines (within margin)
* Check on off-curves in extremes that are not vertical/horizontal
* ...

## To be fixed by Petr

* Check component base glyphs to exist in the font
* Check margins (using kerning groups as source)

## To be done in workshop UI

* Make sample tool that uses all vanilla control
* Make a tool that include the scripts of previous workshop
* Make new vanilla class by inheriting existing classes 
* Make a canvas/drawing board 
* Possibly look into a spreadsheet
* Connect to Glyphs (to RoboFont)
* Implementation of dimensioneer: finding stems, bars, diagonals + UI to control + drawing in GlyphsApp

## Design knowledge
* Check interpolation errors between masters (easy at start, complex with fixing)
* Add anchors and position accents on anchors, check vertical position of anchors
* write glyph.angledLeftMargin and glyph.angleRightMargin for fontParts.Font

## Done

* Look at vanilla sources

* Check unicode (no doubles, relevant glyphs have unicode)
* accentnamecmb --> width = 0
* Check on negative width
* Read a UFO, do something to it, save it.
* **check width of .tab for a whole family**
* **Groups and kerning, exporting to Python source**
* **Make a script that checks a font for mistakes in spacing and kerning**
* **Export Python source for groups and kerning**

## Other example exercises

* Make a script that runs through folders with images and applies Photoshop-like filters on each of them;
* Make a script that draws graphs based on information from a spreadsheet. Save the pages in PDF documents, using your own layout;
* Make a script that generates a simple website, based on content in a Markdown file.


