#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, operator, math

from sys import argv
from operator import itemgetter

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

def bagOfWords(file, word):
	BagOfWords = {}
	with open(file, 'rb') as f:
		target = word
		for line in f:
			if target in line:
				words = line.split()
				freq = int(words[0])
				for i in range(1,len(words)):
					word = words[i]
					if word != target and lexiconClean.has_key(word):
						if not BagOfWords.get(word):
							BagOfWords[word] = 0
						BagOfWords[word] += freq
	return BagOfWords

def lexiconClean(lexicon):
	lexiconClean = {}
	with open('lexiconClean.txt','wb') as file:				
		clean = 0;
		for key, value in lexicon:
			if clean > 249:
				w = key + '\t' + str(value) + '\n'			
				file.write(w)								
				lexiconClean[key] = value
			clean += 1
	return lexiconClean
	
def idfComputation(jWord, nContexts, lexicon):
	df = float(lexicon[jWord])/float(nContexts)
	return -math.log(df,10)
	
def dijComputation(jWord, nContexts, lexicon, tf):
	return tf*idfComputation(jWord,nContexts,lexicon)

def tfidfRepresentation(word, nContexts, lexicon):
	bow = bagOfWords(argv[1],word)
	dij = {}
	for jWord, freq in bow.iteritems():
		dij[jWord] = dijComputation(jWord,nContexts,lexicon,freq)
	return dij
	
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
	
lexicon = lexicon(argv[1])
lexicon = sorted(lexicon.items(), key = operator.itemgetter(1), reverse = True)							
lexiconClean = lexiconClean(lexicon)
bow = bagOfWords(argv[1],argv[2])
printBagOfWords(argv[2], bow)
numContexts = len(lexiconClean)
tfidf = tfidfRepresentation(argv[2],numContexts,lexiconClean)
printTfidf(tfidf)