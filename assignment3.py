#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import sys, operator, math
from sys import argv
from operator import itemgetter
import numpy as np

NUM_DISCARDS = 250

def lexicon(file):
	lexi = {}
	with open(file, 'r') as f:
		for line in f:
			words = line.split()
			freq = int(words[0])
			for i in range(1,len(words)):
				if lexi.has_key(words[i]):
					lexi[words[i]] += freq
				else:
					lexi[words[i]] = freq
	return lexi

def lexiconClean(lexi):
	lexiClean = {}
        clean = 0;
        for key, value in lexi:
                if clean > NUM_DISCARDS-1:
                        lexiClean[key] = value
                clean += 1
	return lexiClean

def bagsOfWords(target, inFile, lexi):
        contexts = {}
	with open(inFile, 'rb') as f:
		for line in f:
                        words = line.split()
                        freq = int(words[0])
                        for word1 in words[1:]:
                                if word1 == target or lexi.has_key(word1):
                                        if not contexts.has_key(word1):
                                                contexts[word1] = {}
                                        for word2 in words:
                                                if word1 != word2 and lexi.has_key(word2):
                                                        if not contexts[word1].has_key(word2):
                                                                contexts[word1][word2] = 0
                                                        contexts[word1][word2] += freq
        return contexts
                                                
def bagOfWords(inFile, word, lexi):
	BagOfWords = {}
	with open(inFile, 'rb') as f:
		for line in f:
                        words = line.split()
			if word in words:
				freq = int(words[0])
				for i in range(1,len(words)):
					w = words[i]
					if w != word and lexi.has_key(w):
						if not BagOfWords.get(w):
							BagOfWords[w] = 0
						BagOfWords[w] += freq
	return BagOfWords

def idfComputation(jWord, contexts, nContexts):
        nContextsPresent = len(contexts[jWord])
        if nContextsPresent > 0:
                df = nContextsPresent/nContexts
                return -math.log(df,10)
        return 0
	
def dijComputation(jWord, contexts, nContexts, tf):
        idf = idfComputation(jWord,contexts,nContexts)
        return tf*idf

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
        prod = norm1 * norm2
        if prod:
                sim = np.dot(v1,v2)/(norm1*norm2)
        else:
                sim = 0.0
        return sim	

def similarWords(word, lexi, contexts, nContexts):
	similars = {}
	dij1 = tfidfRepresentation(word,contexts,nContexts)
	for w, freq in lexi.iteritems():
		dij2 = tfidfRepresentation(w,contexts,nContexts)
                sim = similarity(dij1,dij2)
                similars[w] = float("{0:.4f}".format(sim))
	return similars

def printBagOfWords(word, bagOfWords):					
	print ''
	print '-------Bag of words for ' + word + '-------'
	print '{'
	for key, val in bagOfWords.iteritems():
		print '    ' + key + ': ' + str(val)
	print '}'
	print '-------------------------------------'
	
def printTfidf(tfidf):
	print ''
	print '-------- tfidf Representation -------'
	print '{'
	for key, val in tfidf.iteritems():
		print '    ' + key + ': ' + str(val)
	print '}'
	print '-------------------------------------'

inFile = argv[1]
target_word = argv[2]
lex = lexicon(inFile)
lex = sorted(lex.items(),key = operator.itemgetter(1),reverse = True)
lexClean = lexiconClean(lex)
numContexts = len(lexClean)
contexts = bagsOfWords(target_word,inFile,lexClean)
#bow = contextsPresent[target_word]
#for w,f in bow.iteritems():
#        print w + ' -> ' + str(f)
sim = similarWords(target_word,lexClean,contexts,numContexts)
sim = sorted(sim.items(),key = operator.itemgetter(1),reverse = True)	
for key, val in sim:
    print key + ' ' + str(val)




