
l = [32,32,23,232,3] # list (dynamic)
t = (43,34,34,34,34) # tuple (static)
t = {23:43,45:34,1:34,0:4,4:34} # tuple (static)

print(l)
print(t)
#for n in l:
#    print(n)
#for n in t:
#    print(n)
    
print(l[3], l)
l[3] = 500
print(l[3], l)

print(t[3], t)
t[3] = 500
print(t[3], t)
