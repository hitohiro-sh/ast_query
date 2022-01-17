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
    elif len(argv) > 1 and argv[1] == '-l':
        vs = argv[2].split(':')
        if len(vs) == 1:
            start = stop = int(vs[0])
        elif len(vs) == 2:
            if vs[0] != '':
                start = int(vs[0])
            else:
                start = -1
            if vs[1] != '':
                stop = int(vs[1])
            else:
                stop = -1
        pattern = re.compile(".+:(\d+):(\d+),")

        def search_line(line):
            m = re.search(pattern, line)
            if m:
                vs2 = m.groups()
                cur_start = int(vs2[0])
                cur_stop = int(vs2[1])
                if start < 0:
                    return cur_stop <= stop
                if stop < 0:
                    return start <= cur_start
                return start <= cur_start and cur_stop <= stop
            else:
                return False
        comp_func = lambda line: search_line(line)
    elif len(argv) > 1 and argv[1] == '-s':
        pattern = argv[2]
        
        comp_func = lambda line: pattern == line

    return comp_func


def main(argv, input = sys.stdin, output = sys.stdout):
    comp_func = config(argv)

    for line in iter(comp_func, input):
        print(line, file=output)

if __name__ == '__main__':
    main(sys.argv)