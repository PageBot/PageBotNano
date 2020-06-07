#
#   PageBot Nano
#
#   This MyTypeSpecimen.py shows an example how to import
#   existing libaries, that contain knowledge about document,
#   pages and the elements on the pages.
#

# From the library we import the classes (=object factories)
# that we need for creating the type specimen.
from pagebotnano.document import Document
from pagebotnano.page import Page
from pagebotnano.elements import Element

class TypeSpecimen(Document):
    # Class names start with a capital. See a class as a factory
    # of type specimen objects (name spelled with an initial lower case.)
    # In this case we inherit from what is already defined in Document.
    # Similar how a Volkswagen factory would inherit the functions already
    # defined in a generic car factory. Inheriting is one of the most 
    # powerful aspects of Python programming, so an object can perform
    # complex tasks, without the need to add these functions again for
    # every new project.
    pass # For now it will do nothing, but that will change.


# Now we create a new type specimen, by executing the class.
# Compare that by letting a car factory produce a car. We only need
# one factory ("TypeSpecimen" name starting with capital), which
# then can product an inlimited number of typeSpecimen objects (name
# starting with a lower case.)

typeSpecimen = TypeSpecimen() # Execute the class/factory by adding "()"
print(typeSpecimen)

# It seems like nothing happened yet, because the class/factory is
# still empty, but that will change soon. That is worked is visible
# because there was no error when running this in DrawBot.
