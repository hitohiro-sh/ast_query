# naive pretty print for S-exp like structure.

import sys
import io

def main(argv):
    with open(argv[1]) as input:
        stack = []
        out = io.StringIO()
        prev_c = ''
        for line in input.readlines():
            for c in line:
                if c == '(':
                    out.write('\n')
                    out.write(' ' * len(stack))
                    out.write(c)
                    stack.append(c)
                    prev_c = c
                elif c == ')':
                    out.write(c)
                    stack.pop()
                    prev_c = c
                elif c.isspace():
                    if prev_c == '(' or prev_c == ')' or prev_c.isspace():
                        continue
                    out.write(' ')
                else:
                    out.write(c)
                    prev_c = c
        print(out.getvalue())
    pass

if __name__ == '__main__':
    main(sys.argv)