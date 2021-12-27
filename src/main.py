#Object file format from the book:
# LINK
# nsegs nsyms nrels
# - segments
# - symbols -
# - rels -
# - data -
import os
import sys
from collections import namedtuple

class Segment:
    #logicalAddy and sizeBytes are given in hex
    def __init__(self, name, logicalAddy, sizeBytes, flags):
        self.name = name
        self.logicalAddy = int(logicalAddy, 16)
        self.sizeBytes = int(sizeBytes, 16)
        self.flags = flags

    def __str__(self):
        return '{} {} {} {}'.format(self.name, hex(self.logicalAddy)[2:], hex(self.sizeBytes)[2:], self.flags)

class Symbol:
    def __init__(self, name, value, seg, type):
        self.name = name
        self.value = int(value, 16)
        self.seg = seg
        self.type = type

    def __str__(self):
        return '{} {} {} {}'.format(self.name, (hex(self.value))[2:], self.seg, self.type)

class Relocation:
    def __init__(self, loc, seg, ref, type):
        self.loc = int(loc, 16)
        self.seg = seg
        self.ref = int(ref, 16)
        self.type = type

    def __str__(self):
        return '{} {} {} {}'.format(hex(self.loc)[2:], self.seg, hex(self.ref)[2:], self.type)

print(os.getcwd())
with open("test1.o", 'r') as f:
    s = f.read()
    lines = s.split("\n")

if(not len(lines)):
    print("Read an empty file")

lines = [line.strip() for line in lines if len(line)]

#first line is the magic number LINK
if lines[0] != "LINK":
    print("Missing magic LINK line on first line")
    sys.exit(0)


(nsegs, nsyms, nrels) = [int(el) for el in lines[1].split()]

segments = []
for line in lines[2 : 2 + nsegs]:
    line = line.split()
    segments.append(Segment(line[0], line[1], line[2], line[3]))

symbols = []
for line in lines[2 + nsegs : 2 + nsegs + nsyms]:
    line = line.split()
    symbols.append(Symbol(line[0], line[1], line[2], line[3]))

relocations = []
for line in lines[2 + nsegs + nsyms: 2 + nsegs + nsyms + nrels]:
    line = line.split()
    relocations.append(Relocation(line[0], line[1], line[2], line[3]))

with open('test1-output.o', 'w') as f:
    f.write('LINK\n')
    f.write('{} {} {}\n'.format(nsegs, nsyms, nrels))
    for seg in segments:
        f.write(str(seg) + '\n')
    for sym in symbols:
        f.write(str(sym) + '\n')
    for rel in relocations:
        f.write(str(rel) + '\n')

