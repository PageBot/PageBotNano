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
import os
from xml.etree import ElementTree as ET
import sys

if __name__ == "__main__":
    sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano.babelstring import BabelString
from pagebotnano.toolbox.markdown import parseMarkdownFile, parseMarkdown
from pagebotnano.elements import Element, TextBox, Image, Marker
from pagebotnano.toolbox.transformer import path2Extension, path2FileName
from pagebotnano.constants import DEFAULT_WIDTH

class Galley(Element):
    pass

class Typesetter:
    """Typesetter takes one or a series of inputs, converts them to
    BabelString and elements, and adds thoses to the supplied galley.

    >>> ts = Typesetter()
    >>> ts.galley # By default a galley has no with or height.
    <Galley name=Galley w=None h=None>
    """
    def __init__(self, galley=None):
        self.reset(galley)

    def reset(self, galley=None):
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
        extension = path2Extension(path)
        if extension in ('jpg', 'png', 'gif'):
            # This is an image, create the html tag link code for it.
            xml = '<xml><img src="%s"/></xml>' % path
        elif extension == 'pdf':
            # This is a PDF file, in html we can only link to it.
            xml = '<xml><a href="%s">%s</a></xml>' % (path, path2FileName(path))
        elif extension in ('svg', 'html', 'xml'):
            # This is an XML-tagged document. We can directly parse it
            root = ET.fromFile(path)
            self.typesetNode(root, self.galley, styles)
        elif extension in ('md', 'txt'):
            xml = parseMarkdownFile(path)
        # Answer the galley for convenience of the caller
        return self.typeset(xml, styles) 

    def typesetMarkdown(self, md, style):
        xml = parseMarkdown(md)
        # Answer the galley for convenience of the caller
        return self.typeset(xml, styles) 

    def typesetString(self, s, styles):
        s = str(s).replace('<', '%lt;').replace('>', '%gt;')
        xml = '<xml>%s</xml>' % s # Convert to valid plain XML string.
        # Answer the galley for convenience of the caller
        return self.typeset(xml, styles) 

    def typeset(self, xml, styles=None):
        """Parse the xml into TextBox/Image elements,using the matching styles.

        >>> from pagebotnano.toolbox.markdown import parseMarkdownFile
        >>> ts = Typesetter()
        >>> g = ts.typesetFile('../../../resources/test.md')
        >>> ts.verbose[-1]
        'Node "h1" has no supporting style'
        >>> ts.reset()
        >>> g = ts.typesetFile('../../../resources/images/cookbot1.jpg')
        >>> ts.verbose
        ['Node "xml" has no supporting style', 'Node "img" has no supporting style']
        >>> ts.reset() # Reset the verbose warnings
        >>> xml = '<xml><h1>Headline</h1><h2>Subhead</h2><p>This is a tagged text</p></xml>'
        >>> styles = dict()
        >>> styles['h1'] = dict(font='Georgia-Bold', fontSize=24) # Intentionally not for <h2>
        >>> styles['p'] = dict(font='Georgia', fontSize=10)
        >>> g = ts.typeset(xml, styles)
        >>> xml = '<unknownTag/>'
        >>> g = ts.typeset(xml)
        >>> ts.verbose[-1]
        'Node "unknownTag" not supported'
        """
        self.xml = xml # Store the latest xml for debugging
        root = ET.fromstring(xml)
        self.typesetNode(root, self.galley, styles)
        return self.galley # Answer the galley for convenience of the caller

    def typesetNode(self, node, e, styles=None):
        """Recursively typeset the etree `node`, using a reference to element `e`.
        """
        # If not dictionary of node-tag styles supplied, then create an empty one.
        if styles is None:
            styles = {}
        style = styles.get(node.tag) # Search the style for this node. Can be None.
        if style is not None and 'tag' not in style:
            style['tag'] = node.tag

        nodeSupport = 'node_'+node.tag
        # Is this tag supported by the typesetter? If it does, then e.g. for a 
        # tag name of "img", the typesetter needs to implement self.node_img for
        # the opening and self._node_img for the closing of the tag processing.
        if hasattr(self, nodeSupport): 
            if style is None: # No style available for this tag, mark as warning.
                self.verbose.append('Node "%s" has no supporting style' % node.tag)
            # Get the self.node_<node.tag> method and call it with the node,
            # the `e` (likely to be the galley) and the tag style if it existed.
            getattr(self, nodeSupport)(node, e, style)
        else: # The typesetter does not support this kind of tag.
            self.verbose.append('Node "%s" not supported' % node.tag)

        # Typeset all childs node in the current node, by recursive call.
        for child in node:
            self.typesetNode(child, e, styles)

        if hasattr(self, '_'+nodeSupport): # Is this tag supported?
            # Get the typesetter method that knows how to handle the closing
            # of this tag and call it with the node, the `e` (likely to be the galley)
            # and the style if it existed.
            getattr(self, '_'+nodeSupport)(node, e, style)

    def getTextBox(self, e=None):
        """Answer the last TextBox element if it exists. 
        Otherwise create it first.

        >>> ts = Typesetter()
        >>> e = ts.getTextBox()
        >>> e
        <TextBox name=TextBox w=100pt h=None>
        >>> e1 = ts.getTextBox() # Gets the existing last TextBox
        >>> e is e1
        True
        >>> e2 = TextBox('', x=0, y=0, w=DEFAULT_WIDTH)
        >>> ts.galley.addElement(e2)
        <TextBox name=TextBox w=100pt h=None>
        >>> e2 is ts.getTextBox() # Now finding the new one as last
        True
        """
        if e is None:
            e = self.galley
        if not e.elements or not isinstance(e.elements[-1], TextBox):
            e.addElement(TextBox('', x=0, y=0, w=e.w or DEFAULT_WIDTH))
        return e.elements[-1]

    def node_xml(self, node, e, style):
        """Root of the xml tree. Ignore."""
        pass

    def _node_xml(self, node, e, style):
        """Root of the xml tree. Ignore."""
        pass

    def node_img(self, node, e, style):
        """Add a new image to the galley
        """
        path = node.attrib.get('src')
        if os.path.exists(path):
            e.addElement(Image(path))
        else:
            self.verbose.append('Image "%s" does not exist.' % path)

    def _node_img(self, node, e, style):
        pass

    def node_literature(self, node, e, style):
        e.addElement(Marker('literature', index=node.attrib.get('index')))

    def _node_literature(self, node, e, style):
        if node.tail:
            tb = self.getTextBox(e)
            tb.bs.append(node.tail, style) # Must be style of the parent.

    def node_footnote(self, node, e, style):
        e.addElement(Marker('footnote', index=node.attrib.get('index')))

    def _node_footnote(self, node, e, style):
        if node.tail:
            tb = self.getTextBox(e)
            tb.bs.append(node.tail, style) # Must be style of the parent.

    def node_author(self, node, e, style):
        e.addElement(Marker('author', index=node.attrib.get('index')))

    def _node_author(self, node, e, style):
        if node.tail:
            tb = self.getTextBox(e)
            tb.bs.append(node.tail, style) # Must be style of the parent.

    def node_page(self, node, e, style):
        e.addElement(Marker('page', index=node.attrib.get('index')))

    def _node_page(self, node, e, style):
        pass

    def node_chapter(self, node, e, style):
        e.addElement(Marker('chapter', index=node.attrib.get('ref')))

    def _node_chapter(self, node, e, style):
        pass

    def node_p(self, node, e, style):
        """Add a new paragraph to the last TextBox in the galley.
        
        >>> xml = '<xml><p>This is a tagged text</p></xml>'
        >>> styles = dict()
        >>> styles['p'] = dict(font='Georgia', fontSize=10)
        >>> ts = Typesetter()
        >>> g = ts.typeset(xml, styles)
        >>> ts.galley.elements[0].bs.runs[1].s
        'This is a tagged text'
        >>> ts.galley.elements[0].bs.runs[1].style
        {'font': 'Georgia', 'fontSize': 10, 'tag': 'p'}
        >>> ts.galley.elements[-1].bs.html # Reconstruct the html from the runs.
        '<p>This is a tagged text</p>'
        """
        tb = self.getTextBox(e)
        tb.bs.append(node.text, style)

    def _node_p(self, node, e, style):
        """Close the <p> with any text that is still in the node.tail.
        Always add a return (which will be removed on reconstruction of the bs.html)
        """
        if node.tail:
            tb = self.getTextBox(e)
            tb.bs.append(node.tail, style) # Must be style of the parent.

    def node_h1(self, node, e, style):
        """Add a new "h1" head to the last TextBox in the galley.
        
        >>> xml = '<xml><h1>Head</h1><p>This is a tagged text</p></xml>'
        >>> styles = dict()
        >>> styles['h1'] = dict(font='Georgia-Bold', fontSize=24)
        >>> styles['p'] = dict(font='Georgia', fontSize=10)
        >>> ts = Typesetter()
        >>> g = ts.typeset(xml, styles)
        >>> ts.galley.elements[0].bs.runs[1].s
        'Head'
        >>> ts.galley.elements[0].bs.runs[1].style
        {'font': 'Georgia-Bold', 'fontSize': 24, 'tag': 'h1'}
        >>> ts.galley.elements[-1].bs.html # Reconstruct the html from the runs.
        '<h1>Head</h1><p>This is a tagged text</p>'
        """
        tb = self.getTextBox(e)
        tb.bs.append(node.text, style)

    def _node_h1(self, node, e, style):
        """Close the <h1> with any text that is still in the node.tail.
        Always add a return (which will be removed on reconstruction of the bs.html)
        """
        if node.tail:
            tb = self.getTextBox(e)
            tb.bs.append(node.tail, style) # Must be style of the parent.

    def node_h2(self, node, e, style):
        tb = self.getTextBox(e)
        tb.bs.append(node.text, style)

    def _node_h2(self, node, e, style):
        if node.tail:
            tb = self.getTextBox(e)
            tb.bs.append(node.tail, style) # Must be style of the parent.

    def node_h3(self, node, e, style):
        tb = self.getTextBox(e)
        tb.bs.append(node.text, style)

    def _node_h3(self, node, e, style):
        if node.tail:
            tb = self.getTextBox(e)
            tb.bs.append(node.tail, style) # Must be style of the parent.

    def node_h4(self, node, e, style):
        tb = self.getTextBox(e)
        tb.bs.append(node.text, style)

    def _node_h4(self, node, e, style):
        if node.tail:
            tb = self.getTextBox(e)
            tb.bs.append(node.tail, style) # Must be style of the parent.

    def node_h5(self, node, e, style):
        tb = self.getTextBox(e)
        tb.bs.append(node.text, style)

    def _node_h5(self, node, e, style):
        if node.tail:
            tb = self.getTextBox(e)
            tb.bs.append(node.tail, style) # Must be style of the parent.

    def node_h6(self, node, e, style):
        tb = self.getTextBox(e)
        tb.bs.append(node.text, style)

    def _node_h6(self, node, e, style):
        if node.tail:
            tb = self.getTextBox(e)
            tb.bs.append(node.tail, style) # Must be style of the parent.

    def node_em(self, node, e, style):
        tb = self.getTextBox(e)
        tb.bs.append(node.text, style)

    def _node_em(self, node, e, style):
        if node.tail:
            tb = self.getTextBox(e)
            tb.bs.append(node.tail, style) # Must be style of the parent.

    def node_a(self, node, e, style):
        tb = self.getTextBox(e)
        tb.bs.append(node.text, style)

    def _node_a(self, node, e, style):
        if node.tail:
            tb = self.getTextBox(e)
            tb.bs.append(node.tail, style) # Must be style of the parent.

    def node_b(self, node, e, style):
        tb = self.getTextBox(e)
        tb.bs.append(node.text, style)

    def _node_b(self, node, e, style):
        if node.tail:
            tb = self.getTextBox(e)
            tb.bs.append(node.tail, style) # Must be style of the parent.

    def node_ul(self, node, e, style):
        tb = self.getTextBox(e)
        tb.bs.append(node.text, style)

    def _node_ul(self, node, e, style):
        if node.tail:
            tb = self.getTextBox(e)
            tb.bs.append(node.tail, style) # Must be style of the parent.

    def node_ol(self, node, e, style):
        tb = self.getTextBox(e)
        tb.bs.append(node.text, style)

    def _node_ol(self, node, e, style):
        if node.tail:
            tb = self.getTextBox(e)
            tb.bs.append(node.tail, style) # Must be style of the parent.

    def node_li(self, node, e, style):
        tb = self.getTextBox(e)
        tb.bs.append(node.text, style)

    def _node_li(self, node, e, style):
        if node.tail:
            tb = self.getTextBox(e)
            tb.bs.append(node.tail, style) # Must be style of the parent.

    def node_strong(self, node, e, style):
        tb = self.getTextBox(e)
        tb.bs.append(node.text, style)

    def _node_strong(self, node, e, style):
        if node.tail:
            tb = self.getTextBox(e)
            tb.bs.append(node.tail, style) # Must be style of the parent.

    def node_i(self, node, e, style):
        tb = self.getTextBox(e)
        tb.bs.append(node.text, style)

    def _node_i(self, node, e, style):
        if node.tail:
            tb = self.getTextBox(e)
            tb.bs.append(node.tail, style) # Must be style of the parent.

    def node_hr(self, node, e, style):
        tb = self.getTextBox(e)
        tb.bs.append(node.text, style)

    def _node_hr(self, node, e, style):
        if node.tail:
            tb = self.getTextBox(e)
            tb.bs.append(node.tail, style) # Must be style of the parent.

    def node_code(self, node, e, style):
        tb = self.getTextBox(e)
        tb.bs.append(node.text, style)

    def _node_code(self, node, e, style):
        if node.tail:
            tb = self.getTextBox(e)
            tb.bs.append(node.tail, style) # Must be style of the parent.

    def node_python(self, node, e, style):
        #tb = self.getTextBox(e)
        #tb.bs.append(node.text, style)
        pass

    def _node_python(self, node, e, style):
        if node.tail:
            tb = self.getTextBox(e)
            tb.bs.append(node.tail, style) # Must be style of the parent.

    def node_br(self, node, e, style):
        tb = self.getTextBox(e)
        tb.bs.append(node.text, style)

    def _node_br(self, node, e, styles):
        pass

    def node_blockquote(self, node, e, style):
        pass

    def _node_blockquote(self, node, e, style):
        pass


if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]