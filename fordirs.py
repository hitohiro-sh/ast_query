import sys

from pathlib import Path
import subprocess
from typing import Pattern

def main(argv : list[str]):
    print(argv)
    path = Path(argv[1])
    pattern = argv[2]

    # '<cmd> {}'        => replace {} to file
    # '<cmd1>' -p '<cmd2>' => pipe <cmd1> to <cmd2>
    cmd_templates = argv[3:]
    if path.is_dir():
        for file in sorted(path.glob(pattern)):
            print(str(file))
            from_pipe_flag = False
            ret = None
            if cmd_templates:
                print(cmd_templates)

                pipe_s = '-p'
                for i, cmd_t in enumerate(cmd_templates):
                    if cmd_t == pipe_s:
                        from_pipe_flag = True
                        continue
                    cmd = cmd_t.format(str(file)).split(' ')
                    print('cmd:', cmd)
                    if i+1 < len(cmd_templates) and cmd_templates[i+1] == pipe_s:
                        stdout_arg = subprocess.PIPE
                    else:
                        stdout_arg = None

                    if from_pipe_flag:
                        input_arg = ret.stdout
                    else:
                        input_arg = None

                    ret = subprocess.run(cmd, input=input_arg, stdout=stdout_arg)
                    from_pipe_flag = False

if __name__ == '__main__':
    main(sys.argv)