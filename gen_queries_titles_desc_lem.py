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
outfile_path = os.path.join(my_path, 'queries/IndriRunQuery.titles-desc.lem')

# regular expression for matching the title line
title_re = re.compile(r"<title>(.*)")

# regular expression for matching the description line
desc_re = re.compile(r"<desc>")

# regular expression for matching an empty line
empty_line_re = re.compile(r"\s*$")

# the ascending number of the query
number = 301
in_desc = False
title = ''
desc = ''

with open(outfile_path, 'w') as outfile:
    with open(infile_path, 'r') as infile:
        outfile.writelines([
            '<parameters>\n',
            '<index>{0}</index>\n'.format(indices_path),
            '<rule>method:dirichlet,mu:1000</rule>\n',
            '<count>1000</count>\n',
            '<trecFormat>true</trecFormat>\n'])

        for line in infile:
            if in_desc and re.match(empty_line_re, line):
                text = remove_special_chars(title + desc)
                text = text.lower()

                #take the text and split its words
                words = nltk.word_tokenize(text)
                text = ''

                # word is a tuple
                for word in words:
                    synonyms = wn.synsets(word)

                    if len(synonyms) == 0:
                        text += word + ' '
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
                in_desc = False
                title = ''
                desc = ''
                number += 1
            elif in_desc:
                desc += ' ' + line.strip()
            elif re.match(desc_re, line):
                in_desc = True
            else:
                title_match = re.match(title_re, line)
                if title_match:
                    title = title_match.group(1).strip()
    outfile.write('</parameters>\n')
