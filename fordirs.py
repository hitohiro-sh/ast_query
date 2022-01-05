import sys

from pathlib import Path
import subprocess
from typing import Pattern

def main(argv):
    #print(argv)
    path = Path(argv[1])
    pattern = argv[2]
    cmd_templates = argv[3:]
    print(cmd_templates)
    if path.is_dir():
        for file in sorted(path.glob(pattern)):
            print(str(file))
            
            #cmd_template1 = cmd_templates[0]
            #cmd_template2 = cmd_templates[1]

            #cmd = cmd_template1.format(str(file)).split(' ')
            #print('cmd:', cmd)
            #ret = subprocess.run(cmd, stdout=subprocess.PIPE)
            #print(ret.stdout)
            #cmd = cmd_template2.format(str(file)).split(' ')
            #print(cmd)
            #ret = subprocess.run(cmd, input=ret.stdout)


if __name__ == '__main__':
    main(sys.argv)