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
#   typesetter.py
#
#   This source contains the Typesetter class, that converts structured
#   context (such as a markdown file) into a Galley, which it self is an
#   element, basically an unlimited vertical sequence of elements of various 
#   kinds, each with their specific content, width and height. 
#   Compare this best with the role of typeset columns that came
#   from the typesetter office, to be composed on pages.
#
from xml.etree import ElementTree as ET
import sys
sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano.babelstring import BabelString
from pagebotnano.toolbox.markdown import parseMarkdownFile, parseMarkdown
from pagebotnano.elements import Element, TextBox, Image
from pagebotnano.toolbox import extensionOf, fileNameOf
from pagebotnano.constants import DEFAULT_WIDTH

class Galley(Element):
    
    def getTextBox(self):
    	"""Answer the last TextBox element if it exists. 
    	Otherwise create it first.

		>>> g = Galley()
		>>> e = g.getTextBox()
		>>> e
		<TextBox w=100 h=None>
		>>> e1 = g.getTextBox() # Gets the existing last TextBox
		>>> e is e1
		True
		>>> e2 = TextBox('', x=0, y=0, w=DEFAULT_WIDTH)
		>>> g.addElement(e2)
		>>> e2 is g.getTextBox() # Now finding the new one as last
		True
    	"""
    	if not self.elements or not isinstance(self.elements[-1], TextBox):
    		self.addElement(TextBox('', x=0, y=0, w=self.w or DEFAULT_WIDTH))
    	return self.elements[-1]

class Typesetter:
    """Typesetter takes one or a series of inputs, converts them to
    BabelString and elements, and adds thoses to the supplied galley.

    >>> ts = Typesetter()
    >>> ts.galley # By default a galley has no with or height.
    <Galley w=None h=None>
     
    """
    def __init__(self, galley=None):
        self.reset(galley)

    def reset(self, galley):
        """Reset the storage buffers of the typesetter."""
        if galley is None:
            galley = Galley()
        self.galley = galley

        self.verbose = [] # Storage for errors/warnings during processing.

    def typesetFile(self, path, styles=None):
        """Typeset the content of the file: .md, .txt or any kind of 
        image). Depending on the kind of file, different actions are taken.
        """
        assert path is not None or xml is not None
        extension = extensionOf(path)
        if extension in ('jpg', 'png', 'gif'):
            # This is an image, create the html tag link code for it.
            xml = '<xml><img src="%s"/></xml>'
        elif extension == 'pdf':
            # This is a PDF file, in html we can only link to it.
            xml = '<xml><a href="%s">%s</a></xml>' % (path, fileNameOf(path))
        elif extension in ('svg', 'html', 'xml'):
            # This is an XML-tagged document. We can directly parse it
            root = ET.fromFile(path)
            self.typesetNode(root, self.galley, styles)
        elif extension in ('md', 'txt'):
            xml = parseMarkdownFile(path)
        self.typeset(xml, styles)

    def typeset(self, xml, styles=None):
        """Parse the xml into TextBox/Image elements,using the matching styles.

        >>> from pagebotnano.toolbox.markdown import parseMarkdownFile
        >>> ts = Typesetter()
        >>> ts.typesetFile('../../../resources/test.md')
        >>> ts.typesetFile('../../../resources/images/cookbot1.jpg')
        >>> xml = '<xml><h1>Headline</h1><h2>Subhead</h2><p>This is a tagged text</p></xml>'
        >>> styles = dict()
        >>> styles['h1'] = dict(font='Georgia-Bold', fontSize=24) # Intentionally not for <h2>
		>>> styles['p'] = dict(font='Georgia', fontSize=10)
        >>> ts.typeset(xml, styles)
        >>> xml = '<unknownTag/>'
		>>> ts.typeset(xml)
		>>> ts.verbose
		['Node "unknownTag" not supported']

        """
        root = ET.fromstring(xml)
        self.typesetNode(root, self.galley, styles)

    def typesetNode(self, node, e, styles=None):
        """Recursively typeset the etree `node`, using a reference to element `e`.
        """
        nodeSupport = 'node_'+node.tag
        if hasattr(self, nodeSupport): # Is this tag supported?
            getattr(self, nodeSupport)(node, e, styles)
        else:
            self.verbose.append('Node "%s" not supported' % node.tag)

        # Type set all childs node in the current node, by recursive call.
        for child in node:
            self.typesetNode(child, e, styles)

        if hasattr(self, '_'+nodeSupport): # Is this tag supported?
            getattr(self, '_'+nodeSupport)(node, e, styles)

    def node_xml(self, node, e, styles):
        """Root of the xml tree. Ignore."""
        pass

    def _node_xml(self, node, e, styles):
        """Root of the xml tree. Ignore."""
        pass

    def node_img(self, node, e, styles):
        pass

    def _node_img(self, node, e, styles):
        pass

    def node_p(self, node, e, styles):
        pass

    def _node_p(self, node, e, styles):
        pass

    def node_h1(self, node, e, styles):
        pass

    def _node_h1(self, node, e, styles):
        pass

    def node_h2(self, node, e, styles):
        pass

    def _node_h2(self, node, e, styles):
        pass

    def node_h3(self, node, e, styles):
        pass

    def _node_h3(self, node, e, styles):
        pass

    def node_h4(self, node, e, styles):
        pass

    def _node_h4(self, node, e, styles):
        pass

    def node_h5(self, node, e, styles):
        pass

    def _node_h5(self, node, e, styles):
        pass

    def node_h6(self, node, e, styles):
        pass

    def _node_h6(self, node, e, styles):
        pass

    def node_em(self, node, e, styles):
        pass

    def _node_em(self, node, e, styles):
        pass

    def node_a(self, node, e, styles):
        pass

    def _node_a(self, node, e, styles):
        pass

    def node_b(self, node, e, styles):
        pass

    def _node_b(self, node, e, styles):
        pass

    def node_ul(self, node, e, styles):
        pass

    def _node_ul(self, node, e, styles):
        pass

    def node_ol(self, node, e, styles):
        pass

    def _node_ol(self, node, e, styles):
        pass

    def node_li(self, node, e, styles):
        pass

    def _node_li(self, node, e, styles):
        pass

    def node_strong(self, node, e, styles):
        pass

    def _node_strong(self, node, e, styles):
        pass

    def node_i(self, node, e, styles):
        pass

    def _node_i(self, node, e, styles):
        pass

    def node_hr(self, node, e, styles):
        pass

    def _node_hr(self, node, e, styles):
        pass

    def node_code(self, node, e, styles):
        pass

    def _node_code(self, node, e, styles):
        pass

    def node_python(self, node, e, styles):
        pass

    def _node_python(self, node, e, styles):
        pass

    def node_br(self, node, e, styles):
        pass

    def _node_br(self, node, e, styles):
        pass

    def node_blockquote(self, node, e, styles):
        pass

    def _node_blockquote(self, node, e, styles):
        pass


if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]