import sys

import re



def iter(comp_func, input):
    for line in input.readlines():
        #if re.search(pattern, line):
        if comp_func(line):
            yield line
            #print(line)

'''
argv:
  0 prog
  1 option:
      -p
      -l
      -s
'''
def config(argv):
    if len(argv) > 1 and argv[1] == '-p':
        pattern = argv[2]
        pattern = re.compile(pattern)

        comp_func = lambda line: re.search(pattern, line)
    else:
        pattern = argv[1]
        
        comp_func = lambda line: pattern == line

    return comp_func


def main(argv, input = sys.stdin, output = sys.stdout):
    comp_func = config(argv)

    for line in iter(comp_func, input):
        print(line, file=output)

if __name__ == '__main__':
    main(sys.argv)