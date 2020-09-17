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
import re
import codecs

def parseMarkdownFile(path):
    """Regular expression based markdown parser.

    >>> path = '../../resources/test.md'
    >>> xml = parseMarkdownFile(path)
    >>> '<python>' in xml and '</python>' in xml
    True
    """
    f = codecs.open(path, mode="r", encoding="utf-8") # Save the XML as unicode.
    txt = f.read()
    f.close()
    txt = txt.replace('\r', '\n') # Just to be sure we have the right type of returns.
    return parseMarkdown(txt)

def parseMarkdown(txt):
    # Solve Python comments inside <code>...</code>
    txt = re.sub('(\\~{3}[^#].*)#([^~]*\\1)$', '\\1<<pythonComment>>\\2', txt, flags=re.MULTILINE)
    # ~~~ ... ~~~ --> <code> ... </code>
    txt = re.sub('\\~\\~\\~([^~]*).*$', '<python>\\1</python>', txt, flags=re.MULTILINE)
    # ![text](src) --> <img src="src" alt="text" />
    txt = re.sub('\\!\\[([^\\[]+)\\]\\(([^\\)]+)\\)', '<img src="\\2" alt="\\1"/>', txt, flags=re.MULTILINE)
    # [text](link) --> <a href="link">text</a>
    txt = re.sub('\\[([^\\[]+)\\]\\(([^\\)]+)\\)', '<a href="\\2">\\1</a>', txt, flags=re.MULTILINE)
    # ### Header --> <h3>Header</h3>
    txt = re.sub('^#{6}\\ ([^#].*)$', '<h6>\\1</h6>', txt, flags=re.MULTILINE)
    txt = re.sub('^#{5}\\ ([^#].*)$', '<h5>\\1</h5>', txt, flags=re.MULTILINE)
    txt = re.sub('^#{4}\\ ([^#].*)$', '<h4>\\1</h4>', txt, flags=re.MULTILINE)
    txt = re.sub('^#{3}\\ ([^#].*)$', '<h3>\\1</h3>', txt, flags=re.MULTILINE)
    txt = re.sub('^#{2}\\ ([^#].*)$', '<h2>\\1</h2>', txt, flags=re.MULTILINE)
    txt = re.sub('^#{1}\\ ([^#].*)$', '<h1>\\1</h1>', txt, flags=re.MULTILINE)
    # >...\n>... --> <blockquote>...</ul>
    txt = re.sub('^[\\>]*\\ (.*)', '<blockquote>\\1</blockquote>', txt, flags=re.MULTILINE)
    txt = txt.replace('</blockquote>\n<blockquote>', '<br/>\n')
    # *...\n*... --> <ul><li>...</li><li>...</li></ul>
    txt = re.sub('^[*]*\\ (.*)', '<ul><li>\\1</li></ul>', txt, flags=re.MULTILINE)
    txt = txt.replace('</ul>\n<ul>', '\n')
    # 1. ...\n2. ... --> <ol><li>...</li>\n<li>...</li></ul>
    txt = re.sub('^[1234567890]*\\.\\ (.*)', '<ol><li>\\1</li></ol>', txt, flags=re.MULTILINE)
    txt = txt.replace('</ol>\n<ol>', '\n')
    # **text** --> <b>text</b>
    txt = re.sub('(\\*\\*)(.*?)\\1', '<b>\\2</b>', txt, flags=re.MULTILINE)
    # __text__ --> <strong>text</strong>
    txt = re.sub('(\\_\\_)(.*?)\\1', '<strong>\\2</strong>', txt, flags=re.MULTILINE)
    # *text* --> <em>text</em> 
    txt = re.sub('(\\*)(.*?)\\1', '<em>\\2</em>', txt, flags=re.MULTILINE)
    # _text_ --> <i>text</i> 
    txt = re.sub('(\\_)(.*?)\\1', '<i>\\2</i>', txt, flags=re.MULTILINE)
    # `text` --> <code>text</code> 
    txt = re.sub('(`)(.*?)\\1', '<code>\\2</code>', txt, flags=re.MULTILINE)
    # ___ --> <hr /> 
    txt = re.sub('^---(.*)', '<hr/>', txt, flags=re.MULTILINE)
    # <p>...</p> 
    txt = re.sub('^([^<\n].*[^>]?)', '<p>\\1</p>', txt, flags=re.MULTILINE)
    txt = txt.replace('<br/>\n<p>', '<br/>\n')
    txt = txt.replace('</blockquote>\n</p>', '</blockquote>\n')
    # Restore the Python comment inside <code>...</code>
    txt = txt.replace('<<pythonComment>>', '#')
    # Does not work. Other pattern?
    while 1:
        txt1 = re.sub('(<python>[^<]*)</?p>([^</python>]*)', '\\1\\2', txt, flags=re.MULTILINE)
        if txt1 == txt:
            break
        txt = txt1
    return '<xml>%s</xml>' % txt


if __name__ == "__main__":
    # Running this document will execute all >>> comments as test of this source.
    import doctest
    doctest.testmod()[0]