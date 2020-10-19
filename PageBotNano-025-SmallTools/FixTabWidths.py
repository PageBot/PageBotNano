
import os
PATH = 'masters/'

for fileName in os.listdir(PATH):
	if fileName.startswith('.'):
		continue
	print(fileName)