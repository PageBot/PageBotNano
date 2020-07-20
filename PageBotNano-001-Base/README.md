**(Use MacDown to view this document)**


# PageBotNano-001-Base
PageBotNano is a top-down evolving light-weight training version of PageBot. It is not compatible, but shares the same structure. 

## In this version

This version of PageBotNano doesn’t do anything yet, except describing the base structure of the Document-Page-Element relation: A Document contains multiple **Page** instances (= objects) and a **Page** contains multiple **Element** instances (e.g. images, text and graphical elements).

### document.py

Contains the class definition of **Document** instances (= objects). A **Document** instance contains a list of **Page** instances.

## element.py 

Contains the start of the **Element** class, of which all elements on a **Page** will inherit their behaviour.

## page.py

Contains the start of the **Page** class, a rectangular area that is the top level container of all elements.