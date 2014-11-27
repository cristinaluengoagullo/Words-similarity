#!/usr/bin/python

import sys, operator

from sys import argv
from operator import itemgetter

lexicon = {}

def readInput(file):
	with open(file, 'r') as f:
		for line in f:
			count = 0
			for word in line.split():
				if count == 0:
					times = int(word)
					count += 1
				else:
					if lexicon.has_key(word):
						lexicon[word] += times
					else:
						lexicon[word] = times
	return
	
readInput(argv[1])
lexicon = sorted(lexicon.items(), key = operator.itemgetter(1), reverse = True)

#with open('lexicon.txt','wb') as file:					
#	for key, value in lexicon:							
#		w = key + '\t' + str(value) + '\n'				
#		file.write(w)									

lexiconClean = {}

with open('lexiconClean.txt','wb') as file:				
	clean = 0;
	for key, value in lexicon:
		if clean > 249:
			w = key + '\t' + str(value) + '\n'			
			file.write(w)								
			lexiconClean[key] = value
		clean += 1