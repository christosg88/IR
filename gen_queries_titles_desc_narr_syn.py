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
outfile_path = os.path.join(my_path, 'queries/IndriRunQuery.titles-desc-narr.syn')

# regular expression for matching the title line
title_re = re.compile(r"<title>(.*)")

# regular expression for matching the description line
desc_re = re.compile(r"<desc>")

# regular expression for matching the narration line
narr_re = re.compile(r"<narr>")

# regular expression for matching an empty line
empty_line_re = re.compile(r"\s*$")

# the ascending number of the query
number = 301
in_desc = False
in_narr = False
title = ''
desc = ''
narr = ''

with open(outfile_path, 'w') as outfile:
    with open(infile_path, 'r') as infile:
        outfile.writelines([
            '<parameters>\n',
            '<index>{0}</index>\n'.format(indices_path),
            '<rule>method:dirichlet,mu:1000</rule>\n',
            '<count>1000</count>\n',
            '<trecFormat>true</trecFormat>\n'])

        for line in infile:
            if re.match(empty_line_re, line):
                if in_narr:
                    text = remove_special_chars(title + desc + narr)
                    text = text.lower()

                    #take the text and split its words
                    words = nltk.word_tokenize(text)
                    text = ''
                    #identify if the word is noun,verb,adjective etc
                    identified_words = nltk.pos_tag(words)

                    # word is a tuple
                    for word in identified_words:
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

                        synonyms_set = set()
                        synonyms_set.add(word[0])
                        for synonym in synonyms:
                            synonyms_set.add(synonym.name().split('.')[0])
    
                        if len(synonyms_set) > 1:
                            text += '{' + ' '.join(synonyms_set) + '} '
                        else:
                            text += ' '.join(synonyms_set) + ' '

                    text = remove_special_chars(text)
                    outfile.writelines([
                        '<query> ',
                        '<type>indri</type> ',
                        '<number>{0}</number> '.format(number),
                        '<text>{0}</text> '.format(text),
                        '</query>\n'])
                    in_narr = False
                    title = ''
                    desc = ''
                    narr = ''
                    number += 1
                elif in_desc:
                    in_desc = False
            elif in_narr:
                narr += ' ' + line.strip()
            elif in_desc:
                desc += ' ' + line.strip()
            elif re.match(narr_re, line):
                in_narr = True
            elif re.match(desc_re, line):
                in_desc = True
            else:
                title_match = re.match(title_re, line)
                if title_match:
                    title = title_match.group(1).strip()

        outfile.write('</parameters>\n')
