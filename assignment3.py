#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, operator

from sys import argv
from operator import itemgetter

#Lexicon

aux = {}

def readInput(file):
	with open(file, 'r') as f:
		for line in f:
			count = 0
			for word in line.split():
				if count == 0:
					times = int(word)
					count += 1
				else:
					if aux.has_key(word):
						aux[word] += times
					else:
						aux[word] = times
	return
	
readInput(argv[1])
aux = sorted(aux.items(), key = operator.itemgetter(1), reverse = True)							

lexicon = {}
BagOfWords = {}

with open('lexiconClean.txt','wb') as file:				
	clean = 0;
	for key, value in aux:
		if clean > 249:
			w = key + '\t' + str(value) + '\n'			
			file.write(w)								
			lexicon[key] = value
		clean += 1

#Bag of Words
		
with open(sys.argv[1], 'rb') as f:
    target = sys.argv[2]
    for line in f:
        if target in line:
            words = line.split()
            freq = int(words[0])
            for i in range(1,len(words)):
                word = words[i]
                if word != target and lexicon.has_key(word):
                    if not BagOfWords.get(word):
                        BagOfWords[word] = 0
                    BagOfWords[word] += freq
					
print ''
print '-------Bag of words for ' + sys.argv[2] + '-------'
print '{'
for key,val in BagOfWords.iteritems():
    print '    ' + key + ': ' + str(val)
print '}'
print '-------------------------------------'