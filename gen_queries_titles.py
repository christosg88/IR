#!/usr/bin/env python3
from os import listdir
import os.path
import re

def remove_special_chars(s):
    # replace more than one characters
    s = s.replace('\'s', '').replace('  ', ' ')

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
outfile_path = os.path.join(my_path, 'queries/IndriRunQuery.titles')

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

                outfile.writelines([
                    '<query> ',
                    '<type>indri</type> ',
                    '<number>{0}</number> '.format(number),
                    '<text>{0}</text> '.format(title),
                    '</query>\n'])

                number += 1
    outfile.write('</parameters>\n')
