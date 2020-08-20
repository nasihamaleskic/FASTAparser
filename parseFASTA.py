#!/usr/bin/env python

import sys
import argparse
import textwrap

parser = argparse.ArgumentParser()

parser.add_argument('file', type=argparse.FileType('r'), nargs='+')

parser.add_argument("-output", "--output")

parser.add_argument("-wrap", "--wrap", type=int)

args = parser.parse_args()

limit = args.wrap
outputfile = args.output

def read_fasta(fp):
        text, seq = None, []
        for line in fp:
            line = line.rstrip()
            if line.startswith(">"):
                if text: yield (text, ''.join(seq))
                text, seq = line, []
            else:
                seq.append(line)
        if text: yield (text, ''.join(seq))

def printFasta(seq):
    outFile = open(outputfile, 'w')
    for line in seq:
        wrapper = textwrap.TextWrapper(width=limit)
        string = wrapper.fill(text=seq)
        outFile.write(string)
        outFile.write('\n')
    outFile.close()

for f in args.file:
    print("File name:", f.name)
    print()
    for text, seq in read_fasta(f):
        if outputfile:
            printFasta(seq)
        ignore, rest = text.split(' ', 1)
        name, des = rest.split(' ', 1)
        print("ID:",name)
        print("Description:",des)
        print('Sequence length:', len(seq))
        print()
