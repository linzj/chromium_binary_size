import sys, re
# use nm --print-size --size-sort --reverse-sort to generate report

class Symbols(object):
    def __init__(self, name):
        self.name = name
        self.symbols = dict()

    def add_symbol(self, name, size, addr):
        self.symbols[name] = (size, addr)

    def find_symbol_size(self, name):
        return self.symbols.get(name, ())

def print_symbol_diff_stat(symbols_a, symbols_b):
    great_stat = 0
    less_stat = 0
    great_count = 0
    less_count = 0
    eq_count = 0
    for name, size in symbols_a.symbols.items():
        size_b = symbols_b.find_symbol_size(name)
        if not size_b:
            continue
        size_b = size_b[0]
        size = size[0]
        if size > size_b:
            great_stat += size - size_b
            great_count += 1
        elif size == size_b:
            eq_count += 1
        else:
            less_stat += size_b - size
            less_count += 1
    print('{0} to {1}: great_stat {2}; less_stat {3}; great_count {4}; eq_count {5}; less_count {6}'.format(symbols_a.name, symbols_b.name, great_stat, less_stat, great_count, eq_count, less_count))


def print_symbol_nonexist_stat(symbols_a, symbols_b):
    count = 0
    size_stat = 0
    for name, size in symbols_a.symbols.items():
        size_b = symbols_b.find_symbol_size(name)
        if not size_b:
            count += 1
            size_stat += size[0]
            print('{0} {1} {2}'.format(name, *size))
    print('NON existent symbol: {0} to {1}: count {2}; size_stat {3}'.format(symbols_a.name, symbols_b.name, count, size_stat))

entry_re = re.compile('[0-9a-f]+\s+([0-9a-f]+)\s+\w\s+([^/]+)(.*)')
def read_symbol(f, name):
    symbols = Symbols(name)
    unname_size = 0
    total_size = 0
    while True:
        line = f.readline()
        if not line:
            break
        line = line.rstrip()
        m = entry_re.match(line)
        if not m:
            raise Exception('not matched line' + line)
        size = int(m.group(1), 16)
        total_size += size
        symbol_name = m.group(2).rstrip()
        symbols.add_symbol(symbol_name, size, m.group(3))
    print('uname_size for {0}: {1}; total_size: {2}'.format(name, unname_size, total_size))
    return symbols

def main():
    with open(sys.argv[1], 'r') as f:
        symbols_a = read_symbol(f, sys.argv[1])

    with open(sys.argv[2], 'r') as f:
        symbols_b = read_symbol(f, sys.argv[2])

    print_symbol_diff_stat(symbols_a, symbols_b)

    print_symbol_nonexist_stat(symbols_a, symbols_b)
    print_symbol_nonexist_stat(symbols_b, symbols_a)

if __name__ == '__main__':
    main()
