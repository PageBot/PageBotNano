from pagebot.elements import *
from pagebot.document import Document
from pagebot.toolbox.color import color
from pagebot.toolbox.units import p, pt, em
from pagebot.fonttoolbox.objects.font import findFont

from indesigncontext.context import InDesignContext
from pagebotcocoa.contexts.drawbot.context import DrawBotContext

if 0:
    context = InDesignContext()
    EXPORT_PATHS = ['Image.js']
else:
    context = DrawBotContext()
    EXPORT_PATHS = ['_export/Image.pdf']

font = findFont('Upgrade-Medium') # Is available in Adobe 
styles = {}
styles['h0'] = dict(name='h0', font=font, fontSize=pt(48), leading=em(0.9), textFill=color(1, 0, 0))
styles['h1'] = dict(name='h1', font=font, fontSize=pt(24), leading=em(0.9), textFill=color(1, 0, 0))
doc = Document(w=510, h=720, context=context, autoPages=8, padding=p(4))
doc.styles = styles # Overwrite all default styles.
page = doc[2]
scaleType = None #SCALE_TYPE_FITWH # for non-proportional
e = Image('resources/images/cookbot10.jpg', parent=page, x=page.pl, y=page.pt, w=page.pw, h=page.pw, scaleImage=False, fill=color(0.5), scaleType=scaleType)
page = doc[3]
e = Image('resources/images/cookbot10.jpg', parent=page, x=page.pl, y=page.pt, w=page.pw, h=page.pw, scaleImage=False, fill=color(0.2), scaleType=scaleType)
e = newRect(parent=page, w=p(16), h=p(16), x=p(20), y=p(11), stroke=color(1, 0, 0), strokeWidth=p(2), fill=color(c=1, m=0.5, y=0, k=0, a=0.8))
e = newRect(parent=page, w=p(16), h=p(16), x=page.pl, y=page.pt, fill=color(1, 0, 0))
e = newRect(parent=page, w=p(16), h=p(16), x=page.pl+p(2), y=p(20), fill=color(c=0.5, m=1, y=0, k=0, a=0.5))
e = newOval(parent=page, w=p(16), h=p(16), x=p(24), y=p(22), fill=color(c=0.5, m=0, y=1, k=0, a=0.5))
e = newTextBox('ABCD EFGH IJKL MNOP', style=doc.styles['h1'], parent=page, w=p(16), h=p(8), x=p(34), y=p(22), padding=p(1), fill=color(c=0, m=0.5, y=1, k=0, a=0.5))
page = page.next        
e = Image('resources/images/cookbot10.jpg', parent=page, x=page.pl, y=page.pt, w=page.pw, h=page.pw, scaleImage=False, fill=color(0.5), scaleType=scaleType)
e = newOval(parent=page, w=p(16), h=p(16), x=p(24), y=p(22), fill=color(c=0.5, m=0, y=1, k=0, a=0.5))
e = newTextBox('@XYZ', style=doc.styles['h0'], parent=page, w=p(26), h=p(8), x=p(14), y=p(22), padding=p(1), fill=color(c=0, m=0.5, y=1, k=0, a=0.5))
page = page.next
e = Image('resources/images/cookbot10.jpg', parent=page, x=page.pl, y=page.pt, w=page.pw, h=page.pw, scaleImage=False, fill=color(0, 0, 1), scaleType=scaleType)
e = newRect(parent=page, w=p(16), h=p(16), x=p(24), y=p(22), fill=color(c=0.5, m=1, y=1, k=0, a=0.5))
e = newTextBox('@EEE', style=doc.styles['h0'], parent=page, w=p(26), h=p(8), x=p(14), y=p(22), padding=p(1), fill=color(c=0, m=0.5, y=1, k=0, a=0.5))
page = page.next
e = Image('resources/images/cookbot10.jpg', parent=page, x=page.pl, y=page.pt, w=page.pw, h=page.pw, scaleImage=False, fill=color(1, 0, 0), scaleType=scaleType)
e = newRect(parent=page, w=p(16), h=p(16), x=p(24), y=p(22), fill=color(c=0.5, m=1, y=1, k=0, a=0.5))
e = newTextBox('@EEE', style=doc.styles['h0'], parent=page, w=p(26), h=p(8), x=p(14), y=p(22), padding=p(1), fill=color(c=0, m=0.5, y=1, k=0, a=0.5))
for exportPath in EXPORT_PATHS:
    doc.export(exportPath)

