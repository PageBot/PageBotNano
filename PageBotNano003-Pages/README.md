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

## Gallery

![](gallery/MyTypeSpecimen.png)