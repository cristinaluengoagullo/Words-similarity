#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

BagOfWords = {}

with open(sys.argv[1], 'rb') as f:
    target = sys.argv[2]
    for line in f:
        if target in line:
            words = line.split()
            freq = int(words[0])
            for i in range(1,len(words)):
                word = words[i]
                if word != target: #and word in lexicon:
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
