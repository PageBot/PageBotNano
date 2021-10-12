

a = False
b = 123
print(a or b or c)

c = 'glyph'

if 0:

    g = None
    print(g.width)
    if g is not None:
        print(g.width)
    else:
        print('No g')

g = None   
print(g is None or g.width)

a = 20
print(10 < a < 15)




d = {'a': 124, 'b': 345, 'c': 67}
print(d)

print(d.keys())
print(d.values())
print(d.items())

for key, value in d.items():
    print('key:', key, 'value:', value)
    
    
    