#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import sys, operator, math
from sys import argv
from operator import itemgetter
import numpy as np

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
	
def idfComputation(nContextsPresent, nContexts):
	if nContextsPresent > 0:
		df = nContextsPresent/nContexts
		return -math.log(df,10)
	return 0	
	
file = argv[1]
lex = lexicon(file)
numContexts = len(lex)

lex = sorted(lex.items(), key = operator.itemgetter(1), reverse = True)

with open('lexiconIdf.txt','wb') as file:
	for key, value in lex:
		w = key + '\t' + str(idfComputation(value,numContexts)) + '\n'
		file.write(w)
	