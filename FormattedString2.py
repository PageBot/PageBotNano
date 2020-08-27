

# d = {12: 123, 23: 34, 'aKey abcd': 234}
# d = dict(aKey='Some thing', font='Verdana')

h1Size = 50
h1Leading = h1Size*1.3
h2Size = h1Size*0.8 # 100-20?   100*0.8?
intpSize = (h1Size + h2Size)/2
refSize = h1Size*0.6
subColor = (1, 0, 1)
# -------------------------------------------------
headStyle = dict(font='Georgia', fontSize=h1Size, fill=(1, 0, 0), lineHeight=h1Leading) #h1
subStyle = dict(font='Verdana', fontSize=h2Size, fill=subColor) #h1
interpolatedSpaceStyle = dict(font='Verdana', fontSize=intpSize, fill=(1, 0, 1))
literatureReferenceStyle = dict(font='Verdana', fontSize=refSize, fill=(0, 0, 0.5), baselineShift=10, lineHeight=170)
# -------------------------------------------------
fs = FormattedString('Hello formatted string ', **headStyle)

fs += FormattedString('and more', **subStyle)

fs += FormattedString(' ', **interpolatedSpaceStyle)

fs += FormattedString('[and more]', **literatureReferenceStyle)

fs += FormattedString('ABCD ', **headStyle)


w = 800
tw, th = textSize(fs, width=w)
print(tw, th)
text(fs, (100, 100))
overfill = textBox(fs, (100, 500, w, th))

print(overfill)
