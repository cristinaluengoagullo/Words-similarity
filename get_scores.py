#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, operator, math
from sys import argv

with open(argv[1], 'r') as f:
    with open('scores.txt','w') as fScores:
        for line in f:
            wordScore = line.split()
            score = wordScore[1]
            fScores.write(score + ' ')

