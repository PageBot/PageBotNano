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
#   codeblock.py
#
#   This source contains the class with knowledge about elements that
#   can be placed on a page.
#
import sys
import drawBot

if __name__ == "__main__":
    sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano_060.elements import Element
from pagebotnano_060.toolbox.color import noColor, color

class CodeBlock(Element):

    DEFAULT_CODE_STYLE = dict(font='Courier', fontSize=9, textFill=0.2, textStroke=noColor)

    def __init__(self, code, x=None, y=None, w=None, h=None, name=None, 
        fill=None, stroke=None, strokeWidth=None, tryExcept=False,
        placeCode=False):
        assert isinstance(code, str)
        self.code = code
        self.tryExcept = tryExcept # Showing Python errors or not.
        self.placeCode = placeCode

    def __repr__(self):
        return '<%s code=%s>' % (self.__class__.__name__, self.code.replace('\n',';')[:200] or 'None')

    def build(self, x, y, doc, page, parent=None):
        """Run the code block. If the view.showSourceCode is True, then just export the code
        for debugging."""
        if not view.showSourceCode:
            self.run()
        else:
            bs = BabelString(self.code, self.DEFAULT_CODE_STYLE)
            Text.build(bs, view, origin, drawElements, **kwargs)

    def run(self, targets=None, verbose=False):
        """Execute the code block. Answer a set of compiled methods, as found in the <code class="Python">...</code>,
        made by Markdown with
        ~~~
        cid = 'NameOfBlock'
        doc = Document(w=300, h=500)
        ~~~
        block code. In this case the MacDown and MarkDown extension libraries
        convert this codeblock to python snippets, such as
        <python>
        cid = 'NameOfBlock'
        page = doc.newPage()
        </python>
        This way authors can run PageBot generators controlled by content.
        Note that it is the author's responsibility not to overwrite global values
        that are owned by the calling composer instance.

        >>> from pagebotnano_060.document import Document
        >>> doc = Document()
        >>> page = doc.newPage()
        >>> code = 'a = 100 * 300'
        >>> cb = CodeBlock(code)
        >>> page.addElement(cb)
        >>> # Create globals dictionary for the script to work with
        >>> g = dict(doc=doc, page=page)
        >>> result = cb.run(g)
        >>> result is g # Result global dictionary is same object as g
        True
        >>> sorted(result.keys())
        ['__code__', 'a', 'doc', 'page']
        >>> cb.code = 'aa = 200 * a' # Change code of the code block, using global
        >>> result = cb.run(g) # And run again with the same globals dictionary
        >>> sorted(result.keys()), g['aa'] # Result is added to the globals
        (['__code__', 'a', 'aa', 'doc', 'page'], 6000000)
        """


        """

        if targets is None:
            if page is None:
                page = self.doc[1]

            targets = dict(composer=self, doc=self.doc, page=page, style=self.doc.styles,
                newText=newText)

            if page is not None:
                targets['box'] = page.select('main')

        elif page is not None:
            targets['page'] = page

        if 'errors' not in targets:
            targets['errors'] = []
        errors = targets['errors']

        if 'verbose' not in targets:
            targets['verbose'] = []
        verbose = targets['verbose']

        if galley is None:
            galley = page.galley


        """

        if targets is None:
            # If no globals defined, create a new empty dictionary as storage of result
            # and try to fill it in case we are part of a page, e.g. for debugging.
            assert self.doc is not None
            if not self.doc.pages:
                page = self.doc.newPage()
            page = self.doc.pages[-1] # Get the last page

            targets = dict(pub=self, doc=self.doc, page=page)
            if doc is not None:
                targets['doc'] = doc
        if not self.tryExcept: # For debugging show full error of code block run.
            exec(self.code, targets) # Execute code block, where result goes dict.
            if '__builtins__' in targets:
                del targets['__builtins__'] # We don't need this set of globals in the returned results.
        else:
            error = None
            try:
                exec(self.code, targets) # Execute code block, where result goes dict.
                if '__builtins__' in targets:
                    del targets['__builtins__'] # We don't need this set of globals in the results.
            except TypeError:
                error = 'TypeError'
            except NameError:
                error = 'NameError'
            except SyntaxError:
                error = 'SyntaxError'
            except AttributeError:
                error = 'AttributeError'
            except:
                error = 'Unknown Error'
            targets['__error__'] = error
            if error is not None:
                print(u'### %s ### %s' % (error, self.code))
            # TODO: insert more possible exec() errors here.

        # For convenience, store the last source code of the block in the result dict.
        if '__code__' not in targets:
            targets['__code__'] = self.code

        return targets # Answer the globals attribute, in case it was created.

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
