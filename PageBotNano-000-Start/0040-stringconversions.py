

filePath = '/Users/petr/Desktop/TYPETR-git/TYPETR-Responder/masters/Responder_P-ufo.Regular.ufo'
parts = filePath.split('/')
print(parts)
fileName = parts[-1]
print(fileName)

fileName = filePath.split('/')[-1]
print(fileName)

print(fileName.replace('.ufo', '.ttf'))

parts = fileName.split('.')
print('%s.%s' % ('.'.join(parts[:-1]), 'ttf'))

fileName = 'Responder_P-ufo.Regular.otf'
parts = fileName.split('.')
print('%s.%s' % ('.'.join(parts[:-1]), 'ttf'))


directory = 'masters'
f = 'Family Name'
s = 'Bold Italic'

fileName = '%s/%s-%s.ufo' % (directory, f.replace(' ','_'), s.replace(' ','_'))
print(fileName)

