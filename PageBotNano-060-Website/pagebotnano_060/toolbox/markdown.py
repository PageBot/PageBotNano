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
#   markdown.py
#
#   Instead of the TypeSetter class in other PageBotNano versions, here the
#   markdown parser will answer a list of PageData classes, that contain
#   all anchor content found in the markdown source. 
#
import re
import codecs

def parseMarkdownFile(path):
    """Regular expression based markdown parser.

    >>> path = '../../PublishingVariables.md'
    >>> pages = parseMarkdownFile(path)
    >>> pages
    {'index': <PageData id=index>, 'drawbot': <PageData id=drawbot>}
    """
    f = codecs.open(path, mode="r", encoding="utf-8") # Save the XML as unicode.
    md = f.read()
    f.close()
    md = md.replace('\r', '\n') # Just to be sure we have the right type of returns.
    md = parseMarkdown(md) # Now we have parsed html as result, parse again to split into pages and elements
    pages = parseMarkdownPages(md)
    return pages

def parseMarkdown(md):
    """
    '<h2>H2</h2>\\n<template type="tableOfContent"/>\\n'
    >>> md = '## H2\\nText with[^12] a footnote reference.\\n'
    >>> parseMarkdown(md)
    '<h2>H2</h2>\\n<p>Text with<footnote ref="12"/> a footnote reference.\\n</p>'
    >>> md = '## H2\\nText with[^litSmith1994] a literature reference.\\n'
    >>> parseMarkdown(md)
    '<h2>H2</h2>\\n<p>Text with<literature ref="Smith1994"/> a literature reference.\\n</p>'
    >>> md = '## H2\\n[^123]: This is the footnote text.\\n'
    >>> parseMarkdown(md)
    '<h2>H2</h2>\\n<footnote id="123"> This is the footnote text.</footnote>\\n'
    >>> md = '## H2\\n[^litSmith1994]: This is the literature text.\\n'
    >>> parseMarkdown(md)
    '<h2>H2</h2>\\n<literature id="Smith1994"> This is the literature text.</literature>\\n'

    """
    # Solve Python comments inside <code>...</code>
    md = re.sub('(\\~{3}[^#].*)#([^~]*\\1)$', '\\1<<pythonComment>>\\2', md, flags=re.MULTILINE)
    # ~~~ ... ~~~ --> <code> ... </code>
    md = re.sub('\\~\\~\\~([^~]*).*$', '<python>\\1</python>', md, flags=re.MULTILINE)
    # ![text](src) --> <img src="src" alt="text" />
    md = re.sub('\\!\\[([^\\[]+)\\]\\(([^\\)]+)\\)', '<img src="\\2" alt="\\1"/>', md, flags=re.MULTILINE)
    # [text](link) --> <a href="link">text</a>
    md = re.sub('\\[([^\\[]+)\\]\\(([^\\)]+)\\)', '<a href="\\2">\\1</a>', md, flags=re.MULTILINE)
    # [^litSmith1994]: --> <literature id="Smith1994">...</literature> # XML-based content tags
    md = re.sub('\\[\\^lit([^\\]]*)\\]\\:([^#].*)$', '<literature id="\\1">\\2</literature>', md, flags=re.MULTILINE)
    # [^1]: --> <footnote id="1">...</footnote> # XML-based content tags
    md = re.sub('\\[\\^([^\\]]*)\\]\\:([^#].*)$', '<footnote id="\\1">\\2</footnote>', md, flags=re.MULTILINE)
    # [^litSmith1994] --> <literature ref="Smith1994"/> # XML-based content tags
    md = re.sub('\\[\\^lit([^\\]]*)\\]', '<literature ref="\\1"/>', md, flags=re.MULTILINE)
    # [^1] --> <footnote ref="1"/> # XML-based content tags
    md = re.sub('\\[\\^([^\\]]*)\\]', '<footnote ref="\\1"/>', md, flags=re.MULTILINE)
    # ### Header --> <h3>Header</h3>
    md = re.sub('^#{6}\\ ([^#].*)$', '<h6>\\1</h6>', md, flags=re.MULTILINE)
    md = re.sub('^#{5}\\ ([^#].*)$', '<h5>\\1</h5>', md, flags=re.MULTILINE)
    md = re.sub('^#{4}\\ ([^#].*)$', '<h4>\\1</h4>', md, flags=re.MULTILINE)
    md = re.sub('^#{3}\\ ([^#].*)$', '<h3>\\1</h3>', md, flags=re.MULTILINE)
    md = re.sub('^#{2}\\ ([^#].*)$', '<h2>\\1</h2>', md, flags=re.MULTILINE)
    md = re.sub('^#{1}\\ ([^#].*)$', '<h1>\\1</h1>', md, flags=re.MULTILINE)
    # >...\n>... --> <blockquote>...</ul>
    md = re.sub('^[\\>]*\\ (.*)', '<blockquote>\\1</blockquote>', md, flags=re.MULTILINE)
    md = md.replace('</blockquote>\n<blockquote>', '<br/>\n')
    # *...\n*... --> <ul><li>...</li><li>...</li></ul>
    md = re.sub('^[*]*\\ (.*)', '<ul><li>\\1</li></ul>', md, flags=re.MULTILINE)
    md = md.replace('</ul>\n<ul>', '\n')
    # 1. ...\n2. ... --> <ol><li>...</li>\n<li>...</li></ul>
    md = re.sub('^[1234567890]*\\.\\ (.*)', '<ol><li>\\1</li></ol>', md, flags=re.MULTILINE)
    md = md.replace('</ol>\n<ol>', '\n')
    # **text** --> <b>text</b>
    md = re.sub('(\\*\\*)(.*?)\\1', '<b>\\2</b>', md, flags=re.MULTILINE)
    # __text__ --> <strong>text</strong>
    md = re.sub('(\\_\\_)(.*?)\\1', '<strong>\\2</strong>', md, flags=re.MULTILINE)
    # *text* --> <em>text</em> 
    md = re.sub('(\\*)(.*?)\\1', '<em>\\2</em>', md, flags=re.MULTILINE)
    # _text_ --> <i>text</i> 
    md = re.sub('(\\_)(.*?)\\1', '<i>\\2</i>', md, flags=re.MULTILINE)
    # `text` --> <code>text</code> 
    md = re.sub('(`)(.*?)\\1', '<code>\\2</code>', md, flags=re.MULTILINE)
    # ___ --> <hr /> 
    md = re.sub('^---(.*)', '<hr/>', md, flags=re.MULTILINE)
    # <p>...</p> 
    md = re.sub('^([^<\n].*[^>]?)', '<p>\\1</p>', md, flags=re.MULTILINE)
    md = md.replace('<br/>\n<p>', '<br/>\n')
    md = md.replace('</blockquote>\n</p>', '</blockquote>\n')
    # Restore the Python comment inside <code>...</code>
    md = md.replace('<<pythonComment>>', '#')
    # Does not work. Other pattern?
    while 1:
        md1 = re.sub('(<python>[^<]*)</?p>([^</python>]*)', '\\1\\2', md, flags=re.MULTILINE)
        if md1 == md:
            break
        md = md1

    return md

TAGS = ('site', 'page', 'template', 'logo', 'content')

class PageData:
    def __init__(self, md):
        self.elementData = {}
        self.md = md
        # Find meta data about this page
        self.name = self._find('name', 'Home')
        self.id = self._find('id', 'index')
        # Now split all other tags into elementData chunck of html code
        for tag, html in re.findall('{{([^ ]*)}}([^{{]*)', md):
            self.elementData[tag] = html

    def _find(self, tag, default):
        found = re.findall('{{%s ([^}]*)}}' % tag, self.md)
        if found:
            return found[0]
        return default

    def __repr__(self):
        return '<%s id=%s>' % (self.__class__.__name__, self.id)

def parseMarkdownPages(md):
    # Now convert into temporary template {{markers}} to easy split patterns
    # <site> --> <page id="main"/> # Select the current page with this identifier
    for tag in TAGS:
        # <page index>  # Select the current page with this identifier
        # <page contact> # Select the current page with this identifier
        md = re.sub('<%s>\\ *$' % tag, '{{%s}}\\n' % tag, md, flags=re.MULTILINE)
        md = re.sub('<%s>\\ *(.*$)' % tag, '{{%s}}{{name \\1}}\\n' % tag, md, flags=re.MULTILINE)
        md = re.sub('<%s\\ *([a-zA-Z0-9]*)>\\ *(.*$)' % tag, '{{%s}}{{id \\1}}{{name \\2}}\\n' % tag, md, flags=re.MULTILINE)

    pages = {}
    for pageMd in md.split('{{page}}'):
        page = PageData(pageMd)
        pages[page.id] = page
    return pages

"""
    # ==template index== --> <template id="main"/> # Select the current template if different than default
    # ==template contact== --> <template id="contact"/> 
    md = re.sub('\\=\\=template\\ ([a-zA-Z0-9]*)\\=\\=.*$', '<template id="\\1"/>', md, flags=re.MULTILINE)
    # ==pageName== --> <template type="cover"/> # XML-based page selector tags
    # ==frenchTitle== --> <template type="frenchTitle"/> 
    # ==title== --> <template type="title"/> 
    # ==tableOfContent== --> <template type="tableOfContent"/> 
    # ==chapter== --> <template type="chapter"/> 
    # ==page== --> <template type="page"/> 
    # ==index== --> <template type="index"/> 
    # ==colophon== --> <template type="colophon"/> 
"""

if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]