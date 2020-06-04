**(Use MacDown to view this document)**

# PageBotNano #002
PageBotNano is a top-down evolving light-weight training version of PageBot. It is not compatible, but shares the same structure. 

## New to this version

* Adding document size
* A constants file with standard paper sizes
* Exporting to a _export folder that does not commit to Github.
* Creates the _export folder if it does not exist.
* Fill the document page with gray background and a white title for now.
* Export to document to show the result in this README.md file

# PageBotNano #003
PageBotNano is a top-down evolving light-weight training version of PageBot. It is not compatible, but shares the same structure. 

## New to this version

* The document now adds 10 pages.
* Document and Page “broadcast” a build instruction, recursively down into the elements on the page. We separate the building process from the export, so it does not have to be done again when saving multiple formats of the same document.
* Pages store their page size internal from the document. But it is possible to adjust the size per page, e.g. to make spreads.
* Pages store their page number, as given by the document upon creation.
* print(document) now show the number of pages in the document.
* Since Pages don't have elements yet, their build method fills the background with a random color, a white title and their pagenummer to show the difference between the pages.

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

## Gallery

![](gallery/MyTypeSpecimen.png)

