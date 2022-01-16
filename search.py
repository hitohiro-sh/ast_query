import sys

import re

def main(argv):
    if len(argv) > 1 and argv[1] == '-p':
        pattern = argv[2]
        pattern = re.compile(pattern)

        comp_func = lambda line: re.search(pattern, line)
    else:
        pattern = argv[1]
        
        comp_func = lambda line: pattern == line

    output = sys.stdin

    for line in output.readlines():
        #if re.search(pattern, line):
        if comp_func(line):
            print(line)

if __name__ == '__main__':
    main(sys.argv)