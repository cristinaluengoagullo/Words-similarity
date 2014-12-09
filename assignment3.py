#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import sys, operator, math
from sys import argv
from operator import itemgetter
import numpy as np

# Number of words to discard from the lexicon
NUM_DISCARDS = 250

# Function to build the lexicon (word: frequency of appearance)
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

# Function to preprocess the lexicon: top 250 most frequent words are deleted
def lexiconClean(lexi):
	lexiClean = {}
        clean = 0;
        for key, value in lexi:
                if clean > NUM_DISCARDS-1:
                        lexiClean[key] = value
                clean += 1
	return lexiClean

# Function to calculate the bags of words of all the words in the lexicon (the target
# word included, in case it doesn't appear in the lexicon after the preprocess).
# For each word, we compute its bag of words, which will be useful to compute the
# TF-IDF representation and the similarity between words
def bagsOfWords(target, inFile, lexi):
        contexts = {}
	with open(inFile, 'rb') as f:
		for line in f:
                        words = line.split()
                        freq = int(words[0])
                        # For each word, we save its context (words that appear in the same
                        # 5-grams as it)
                        for word1 in words[1:]:
                                if word1 == target or lexi.has_key(word1):
                                        if not contexts.has_key(word1):
                                                contexts[word1] = {}
                                        for word2 in words[1:]:
                                                # The context of a word will be the words that are
                                                # different from it, belong to the lexicon, and appear
                                                # in the same 5-grams as it
                                                if word1 != word2:
                                                        if not contexts[word1].has_key(word2):
                                                                contexts[word1][word2] = 0
                                                        contexts[word1][word2] += freq
        return contexts

# Function to compute the IDF weight. It is the negative logarithm of the division between the
# number of times the word appears in other contexts and the total number of contexts
def idfComputation(jWord, contexts, nContexts):
        nContextsPresent = len(contexts[jWord])
        if nContextsPresent > 0:
                df = nContextsPresent/nContexts
                return -math.log(df,10)
        return 0

# Function to compute the TF-IDF value of a word. It is the multiplication of the TF (number of
# times that the word appears in the context) and the IDF (explained above)
def dijComputation(jWord, contexts, nContexts, tf):
        idf = idfComputation(jWord,contexts,nContexts)
        return tf*idf

# Function to compute the TF-IDF representation of a given word
def tfidfRepresentation(word, contexts, lex, nContexts):
        bow = contexts[word]
        dij = {}
	for jWord, freq in bow.iteritems():
                if lex.has_key(jWord):
                        dij[jWord] = float("{0:.4f}".format(dijComputation(jWord,contexts,nContexts,bow[jWord])))
	return dij

# Function to compute the TF-IDF representation of all the words in the lexicon (used to optimize
# the calculation of the two most similar pair of words)
def tfidfsComputation(lex, contexts, nContexts):
        tfidf = {}
        for word,f in lex.iteritems():
                tfidf[word] = tfidfRepresentation(word,contexts,lex,nContexts)
        return tfidf

# Function to compute the similarity between two words from their vectorial representation.
# The formula applied is the cosine of the angle of the two vectors
def similarity(dij1, dij2):
	d1 = {}
        # Each vector will be filled with zeros in the positions where the other vector has a
        # word and the current vector hasn't
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
        # Final vectors filled with zeros in the corresponding positions
	for key, (val1,val2) in d1.iteritems():
		v1.append(val1)
		v2.append(val2)
        # Norm of the vectors
        norm1 = np.linalg.norm(v1) 
	norm2 = np.linalg.norm(v2)
        prod = norm1 * norm2
        # If the norm is different than 0 (they have words in common in their contexts),
        # then we compute the formula
        if prod:
                sim = np.dot(v1,v2)/(norm1*norm2)
        else:
                sim = 0.0
        return sim	

# Function to compute the similar words to a given word. It outputs a dictionary that
# contains the similar words along with their scores
def similarWords(word, lexi, contexts, nContexts):
        # We compute the TF-IDF representation of each pair of words and then we calculate
        # the similarity given their vectorial representations
	similars = {}
	dij1 = tfidfRepresentation(word,contexts,lexi,nContexts)
	for w, freq in lexi.iteritems():
		dij2 = tfidfRepresentation(w,contexts,lexi,nContexts)
                sim = similarity(dij1,dij2)
                similars[w] = float("{0:.4f}".format(sim))
	return similars

# Function to compute the most similar pair of words from the lexicon
def mostSimilarWords(lexi, tfidfs, nContexts):
        similars = {}
        # For each word in the lexicon, we compute its similarity scores
        # with each word in the lexicon
        for word1,f1 in lexi.iteritems():
                print word1
                dij1 = tfidfs[word1]
                for word2,f2 in lexi.iteritems():
                        if not similars.has_key(word2) or ((similars.has_key(word2) and not similars[word2].has_key(word1))):
                                dij2 = tfidfs[word2]
                                sim = similarity(dij1,dij2)
                                # Similarity values between equal words are not stored
                                if word1 != word2:
                                        if not similars.has_key(word1):
                                                similars[word1] = {}
                                        # We build a dictionary that contains, for each key, another dictionary with
                                        # the similar words to the key word and their scores
                                        similars[word1][word2] = sim
        # Once the dictionary is built, we iterate through it to find the highest similarity score
        maxSim = -1
        maxWord1 = ''
        maxWord2 = ''
        for word1, sims in similars.iteritems():
                for word2, val in sims.iteritems():
                        if val > maxSim and val != 1.0:
                                maxSim = val
                                maxWord1 = word1
                                maxWord2 = word2
        return (maxWord1,maxWord2,maxSim)

# Function to print the bag of words of a given word
def printBagOfWords(word, bagOfWords, lex):					
	print ''
	print '-------Bag of words for ' + word + '-------'
	print '{'
	for key, val in bagOfWords.iteritems():
		if lex.has_key(key):
			print '    ' + key + ': ' + str(val)
	print '}'
	print '-------------------------------------'

# Function to print the TF-IDF representation of a given word
def printTfidf(word, tfidf):
	print ''
	print '-------- tfidf Representation for ' + word + '  -------'
	print '{'
	for key, val in tfidf.iteritems():
		print '    ' + key + ': ' + str(val)
	print '}'
	print '-------------------------------------'

# Function to print the two most similar words from the lexicon
def printSimilarWords(word, sim):
        print '-------- Similar words to ' + word + '  -------'
        sim = sorted(sim.items(),key = operator.itemgetter(1),reverse = True)
        for key, val in sim:
                print key + ' ' + str(val)


# Main part of the program
inFile = argv[1]
if len(argv) < 4:
        target_word = ''
        choice = argv[2]
else:
        target_word = argv[2]
        choice = argv[3]
lex = lexicon(inFile)
lex = sorted(lex.items(),key = operator.itemgetter(1),reverse = True)
lexClean = lexiconClean(lex)
numContexts = len(lex)
contexts = bagsOfWords(target_word,inFile,lexClean)

# Choices
# Compute the bag of words of a given word
if choice == 'bow':
        bow = contexts[target_word]
        printBagOfWords(target_word,bow,lexClean)

# Compute the TF-IDF representation of a given word
if choice == 'tfidf':
        tfidf = tfidfRepresentation(target_word,contexts,numContexts)
        printTfidf(target_word,tfidf)

# Compute the similar words and their scores to a given word
if choice == 'similarity':
        sim = similarWords(target_word,lexClean,contexts,numContexts)
        printSimilarWords(target_word,sim)

# Compute the two most similar words from the lexicon
if choice == 'maxSimilarity':
        tfidfs = tfidfsComputation(lexClean,contexts,numContexts)
        (maxWord1,maxWord2,maxSim) = mostSimilarWords(lexClean,tfidfs,numContexts)
        print maxWord1 + ' and ' + maxWord2 + ' -> ' + str("{0:.4f}".format(maxSim))





