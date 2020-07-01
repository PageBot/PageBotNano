**(Use MacDown to view this document)**

# PageBotNano-010-Template

## New to this version

* Create elements/__init__.py as directory with element.py inside
* Make Page inherit from Element
* Start of templates/onecolumn.py to hold standard layouts that can be included in publications.
* All elements now can have a name, so they can be searched for (e.g. with next-element) or for templates with predefined child elements.
* All elements call the initialize() method, to allow building a layout on creation.
* Add Element attributes padding top (pt), padding right (pr), padding bottom (pb) and padding left (pl)
* Add Element.padding property to get/set the padding as a tuple (pl, pr, pb, pl)

