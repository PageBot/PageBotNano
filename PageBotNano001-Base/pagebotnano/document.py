#
#	PageBot Nano
#
#	document.py
#
#	This source contains the class with knowledge about a generic document.
#
class Document:
	# Class names start with a capital. See a class as a factory
	# of document objects (name spelled with an initial lower case.)
	# For now it will do nothing, but that will change.

	def __repr__(self):
		# This method is called when print(document) is executed.
		# It shows the name of the class, which can be different, if the
		# object inherits from Document.
		return 'I am a ' + self.__class__.__name__