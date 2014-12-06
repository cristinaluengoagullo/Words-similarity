#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, operator, math
from sys import argv
from operator import itemgetter
import numpy as np

def lexicon(file):
	lexicon = {}
	with open(file, 'r') as f:
		for line in f:
			words = line.split()
			times = int(words[0])
			for i in range(1,len(words)):
				if lexicon.has_key(words[i]):
					lexicon[words[i]] += times
				else:
					lexicon[words[i]] = times
	return lexicon

def bagOfWords(file, word, lexicon):
	BagOfWords = {}
	with open(file, 'rb') as f:
		target = word
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
	return BagOfWords

def bagsOfWords(file,lexicon):
        bagsOfWords = {}
        for word, freq in lexicon.iteritems():
                bow = bagOfWords(file,word,lexicon)
                bagsOfWords[word] = bow
        return bagsOfWords

def lexiconClean(lexicon):
	lexiconClean = {}
	with open('lexiconClean.txt','wb') as file:				
		clean = 0;
		for key, value in sorted(lexicon.items(), key=lambda x: x[1], reverse=True):
			if clean > 249:
				w = key + '\t' + str(value) + '\n'			
				file.write(w)								
				lexiconClean[key] = value
			clean += 1
	return lexiconClean

def nContextsPresentComputation(word, contexts):
        count = 0
        for w, context in contexts.iteritems():
                if word in context:
                        count += 1
        return count

def idfComputation(jWord, contexts, nContexts):
        nContextsPresent = nContextsPresentComputation(jWord,contexts)
	df = float(nContextsPresent)/float(nContexts)
	return -math.log(df,10)
	
def dijComputation(jWord, contexts, nContexts, tf):
	return tf*idfComputation(jWord,contexts, nContexts)

def tfidfRepresentation(word, contexts, nContexts):
        bow = contexts[word]
        dij = {}
	for jWord, freq in bow.iteritems():
		dij[jWord] = dijComputation(jWord,contexts,nContexts,bow[jWord])
	return dij

def similarity(dij1, dij2):
	d1 = {}
	for key, val in dij1.iteritems():
		val2 = 0
		if dij2.has_key(key):
			val2 = dij2[key]
		d1[key] = (val,val2)
	for key, val2 in dij2.iteritems():
		if not d1.has_key(key):
			d1[key] = (0,val2)
	v1 = []
	v2 = []
	for key, (val1,val2) in d1.iteritems():
		v1.append(val1)
		v2.append(val2)
	norm1 = np.linalg.norm(v1)
	norm2 = np.linalg.norm(v2)
	sim = np.dot(v1,v2)/float(norm1*norm2)
	return sim	

def similarWords(word, contexts, lexicon, nContexts):
	similars = {}
	dij1 = tfidfRepresentation(word,contexts,nContexts)
	for w, freq in lexicon.iteritems():
		dij2 = tfidfRepresentation(w,contexts,nContexts)
		similars[w] = similarity(dij1,dij2)
	return similars

def printBagOfWords(word, bagOfWords):					
	print ''
	print '-------Bag of words for ' + word + '-------'
	print '{'
	for key, val in bagOfWords.iteritems():
		print '    ' + key + ': ' + str(val)
	print '}'
	print '-------------------------------------'
	return
	
def printTfidf(tfidf):
	print ''
	print '-------- tfidf Representation -------'
	print '{'
	for key, val in tfidf.iteritems():
		print '    ' + key + ': ' + str(val)
	print '}'
	print '-------------------------------------'
	return

file = argv[1]
target_word = argv[2]
lexicon = lexicon(file)
lexiconClean = lexiconClean(lexicon)
numContexts = len(lexiconClean)
bows = bagsOfWords(lexiconClean)
#bow = bagOfWords(argv[1],argv[2],lexiconClean)
#printBagOfWords(argv[2],bow)
#tfidf = tfidfRepresentation(argv[2],bows,numContexts)
#printTfidf(tfidf)
sim = similarWords(target_word,bows,lexiconClean,numContexts)
for key, val in sorted(sim.items(), key=lambda x: x[1], reverse=True):
    print key + ' ' + str(val)




