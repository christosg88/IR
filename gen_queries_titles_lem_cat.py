#!/usr/bin/env python3
from os import listdir
import os.path
import re

from nltk.corpus import wordnet as wn
import nltk

def remove_special_chars(s):
    # replace more than one characters
    s = s.replace('\'s', '').replace('  ', ' ').replace('_', ' ')

    # replace one character
    translation = str.maketrans({
        '&' :' and ',
        '(' :'',
        ')' :'',
        ',' :'',
        '-' :' ',
        '.' :'',
        '/' :' ',
        ':' :'',
        ';' :'',
        '\'':'',
        '\"':'',
        '?' :''})

    return s.translate(translation)


# the path to the directory containing the script
my_path = os.path.dirname(os.path.realpath(__file__))

# the topics should be in a directory called "topics" inside the scripts
# directory
topics_path = os.path.join(my_path, 'topics')

# the indices should be in a directory called "indices" inside the scripts
# directory
indices_path = os.path.join(my_path, 'indices')

# the queries will be generated from the topic file
infile_path = os.path.join(my_path, 'topics/topics.trec')

# the query file will be written to the same directory as the script
outfile_path = os.path.join(my_path, 'queries/IndriRunQuery.titles.lem.cat')

# regular expression for matching the title line
title_re = re.compile(r"<title>(.*)")

# the ascending number of the query
number = 301

with open(outfile_path, 'w') as outfile:
    with open(infile_path, 'r') as infile:
        outfile.writelines([
            '<parameters>\n',
            '<index>{0}</index>\n'.format(indices_path),
            '<rule>method:dirichlet,mu:1000</rule>\n',
            '<count>1000</count>\n',
            '<trecFormat>true</trecFormat>\n'])

        for line in infile:
            title_match = re.match(title_re, line)
            if title_match:
                title = remove_special_chars(title_match.group(1).strip())
                text = title
                text = text.lower()

                #take the title and split its words
                words = nltk.word_tokenize(text)
                text = ''
                #identify if the word is noun,verb,adjective etc
                words = nltk.pos_tag(words)

                # word is a tuple
                for word in words:
                    synonyms = []

                    # NN = noun,singular
                    # NNS = noun,plural
                    if word[1] == 'NN' or word[1]=='NNS':
                        synonyms = wn.synsets(word[0], pos=wn.NOUN)

                    # JJ = adjective
                    # JJR = adjective, comparative
                    # JJS = adjective, superlative
                    elif word[1]=='JJ' or word[1]=='JJR' or word[1]=='JJS':
                        synonyms = wn.synsets(word[0], pos=wn.ADJ)

                    # VB = verb,base form "take"
                    # VBD = verb,past tense "took"
                    # VBG = verb,gerund,present participle "taking"
                    # VBN = verb, past participle "taken"
                    # VBP = verb, present, non-3d "sing"
                    # VBZ = verb, 3rd person "sing-sings"
                    elif word[1]=='VBN' or word[1]=='VB' or  word[1]=='VBD' or word[1]=='VBG' or word[1]=='VBP' or word[1]=='VBZ':
                        synonyms = wn.synsets(word[0], pos=wn.VERB)

                    if len(synonyms) == 0:
                        text += word[0] + ' '
                    else:
                        lemmas = synonyms[0].lemma_names()
                        text += ' '.join(lemmas[0:2]) + ' '

                text = remove_special_chars(text)
                outfile.writelines([
                    '<query> ',
                    '<type>indri</type> ',
                    '<number>{0}</number> '.format(number),
                    '<text>{0}</text> '.format(text),
                    '</query>\n'])

                number += 1
    outfile.write('</parameters>\n')
