**(Use MacDown to view this document)**

# PageBotNano #009
## New to this version

* Reverse the order of this document

# PageBotNano #008
## New to this version

* Add MyBook.py, to generate a Book publication, with cover, “french” page, title page and content pages for as many as needed. Using Lorem ipsum text. Better styles. Automatics left/right page number positioning.
* Add default Book publication behavior.
* Add random generator for book titles and author names.
* Add new cookbot2.jpg square example image.
* Add PageBot Type-3 article as markdown file.
* Markdown parser that works entirely with regular expressions. TODO: Add [table] and adding 
* Typesetter now reads markdown files.
* Add Galley (=Element) class, as result of Typesetter typesetting.
* Add Typesetter.typesetMarkdown(), Typesetter.typesetString() and Typesetter.typeset(xml)
* Typesetter.verbose collects all errors and warnings during typesetting from content.
* Typesetter TODO: Add more functionality to the empty tag methods.
* Add MyManual.py example of small booklet reading from markdown file, trying to do real page composition. TODO: captions, better image positioning and more intelligent breaking of columns to next page (taking care about headings).
* Add BabelRun.__repr__
* Add hyphenation. Note that due to limitations of OSX, hyphenation turns on/off in a TextBox, not in a paragraph. The first style of the BabelString in a TextBox is taken as value for the setting.
* Add EN as language code to 
* Add mm() and cm() converter functions to toolbox/



# PageBotNano #007
PageBotNano is a top-down evolving light-weight training version of PageBot. It is not compatible, but shares the same structure. 

## New to this version

* Add context, replacing the fixed DrawBot reference. This leaves room to add Html export in the future. A small sample is already working, but it needs more HTML/CSS knowledge how to make proper pages of a website.

### Missing

* Still needs reading of a Markdown text document, with conversion into BabelString, so we can use it as content for both PDF and HTML/CSS



# PageBotNano #006
PageBotNano is a top-down evolving light-weight training version of PageBot. It is not compatible, but shares the same structure. 

## New to this version

* Add Image element for scaleable images.
* Add image on cover of the type specimen example.
* Add resource fodler with some example images.


# PageBotNano #005
PageBotNano is a top-down evolving light-weight training version of PageBot. It is not compatible, but shares the same structure. 

## New to this version

* Add TextBox element to make columns with overflow handling
* Add toolbox/loremipsum generator for test text, static and random
* Add body text pages to MyTypeSpecimen.py with loremipsum text
* Add functions makeCoverPage and makeBodyPages functions to MyTypeSpecimen.py
* Add boolean flag to Document for testing if build() already as been done before export().
* Add clearDrawing() to Document.
* Add force attribute to Document.export, to force a new build before export
* Add multipage attribute to Document.export, in case exporting multiple PNG pages.
* Add example doc strint to toolbox/color


# PageBotNano #004
PageBotNano is a top-down evolving light-weight training version of PageBot. It is not compatible, but shares the same structure. 

## Relation between classes

![](gallery/DocumentPagesElements.pdf)

## New to this version

* Add folder for tools
* Add Rect class, inheriting from Element
* Add Text class, inheriting from Element
* Add position and size to Element __init__ constructor
* Add toolbox.color.asColor function to test valid values and make a tuple color
* Add Element.drawBackground and Element.drawForeground methods
* Add a color stroked square on the page.

# PageBotNano #003
PageBotNano is a top-down evolving light-weight training version of PageBot. It is not compatible, but shares the same structure. 

## New to this version

* The document now adds 10 pages.
* Document and Page “broadcast” a build instruction, recursively down into the elements on the page. We separate the building process from the export, so it does not have to be done again when saving multiple formats of the same document.
* Pages store their page size internal from the document. But it is possible to adjust the size per page, e.g. to make spreads.
* Pages store their page number, as given by the document upon creation.
* print(document) now show the number of pages in the document.
* Since Pages don't have elements yet, their build method fills the background with a random color, a white title and their pagenummer to show the difference between the pages.



# PageBotNano #002
PageBotNano is a top-down evolving light-weight training version of PageBot. It is not compatible, but shares the same structure. 

## New to this version

* Adding document size
* A constants file with standard paper sizes
* Exporting to a _export folder that does not commit to Github.
* Creates the _export folder if it does not exist.
* Fill the document page with gray background and a white title for now.
* Export to document to show the result in this README.md file


