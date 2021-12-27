# Object file format from the book:
# LINK
# nsegs nsyms nrels
# - segments
# - symbols -
# - rels -
# - data -
import os
import sys

def hexify(num):
    # strip the leading 0x
    return hex(num)[2:]

class Segment:
    # logical_addy and size_bytes are given in hex
    def __init__(self, name, logical_addy, size_bytes, flags):
        self.name = name
        self.logicalAddy = int(logical_addy, 16)
        self.sizeBytes = int(size_bytes, 16)
        self.flags = flags

    def __str__(self):
        return '{} {} {} {}'.format(self.name, hexify(self.logicalAddy), hexify(self.sizeBytes), self.flags)

class Symbol:
    def __init__(self, name, value, seg, sym_type):
        self.name = name
        self.value = int(value, 16)
        self.seg = seg
        self.type = sym_type

    def __str__(self):
        return '{} {} {} {}'.format(self.name, hexify(self.value), self.seg, self.type)

class Relocation:
    def __init__(self, loc, seg, ref, relo_type):
        self.loc = int(loc, 16)
        self.seg = seg
        self.ref = int(ref, 16)
        self.type = relo_type

    def __str__(self):
        return '{} {} {} {}'.format(hexify(self.loc), self.seg, hexify(self.ref), self.type)


def read_obj_file(file):
    with open(file, 'r') as f:
        s = f.read()
        lines = s.split("\n")

    if not len(lines):
        print('Read an empty file')
        sys.exit(1)

    lines = [line.strip() for line in lines if len(line)]

    # first line is the magic number LINK
    if lines[0] != 'LINK':
        print('Missing magic LINK line on first line')
        sys.exit(1)

    (nsegs, nsyms, nrels) = [int(el) for el in lines[1].split()]

    if len(lines) != (nsegs + nsyms + nrels + 2):
        print('Unexpected number of lines found')
        sys.exit(1)

    segments = []
    seg_start = 2
    seg_end = seg_start + nsegs
    for line in lines[seg_start:seg_end]:
        line = line.split()
        segments.append(Segment(line[0], line[1], line[2], line[3]))

    symbols = []
    sym_start = seg_end
    sym_end = sym_start + nsyms
    for line in lines[sym_start:sym_end]:
        line = line.split()
        symbols.append(Symbol(line[0], line[1], line[2], line[3]))

    relocations = []
    relo_start = sym_end
    relo_end = sym_end + nrels
    for line in lines[relo_start:relo_end]:
        line = line.split()
        relocations.append(Relocation(line[0], line[1], line[2], line[3]))

    return segments, symbols, relocations


def write_obj_file(segments, symbols, relocations, output_file):
    with open(output_file, 'w') as f:
        f.write('LINK\n')
        f.write('{} {} {}\n'.format(len(segments), len(symbols), len(relocations)))
        for seg in segments:
            f.write(str(seg) + '\n')
        for sym in symbols:
            f.write(str(sym) + '\n')
        for rel in relocations:
            f.write(str(rel) + '\n')


def main(argv):
    if len(argv) == 1:
        obj_file = 'test1.o'
    else:
        obj_file = argv[1]

    segments, symbols, relocations = read_obj_file(obj_file)
    output_file = '{}-output.o'.format(os.path.splitext(obj_file)[0])
    write_obj_file(segments, symbols, relocations, output_file)


if __name__ == '__main__':
    main(sys.argv)
