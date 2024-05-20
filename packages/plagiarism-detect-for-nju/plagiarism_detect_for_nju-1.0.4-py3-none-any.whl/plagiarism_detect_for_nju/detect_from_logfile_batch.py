#! /usr/bin/env python3
import argparse
import enum
import shutil
from pathlib import Path
import subprocess
import os

END_DASH = '------------------------------------------------------\n'

CUT_STATE = enum.Enum("CUR_STATE", "GETTING BAD NOT_GET")

AC = ("正确\n", "Accepted\n")

suffix = '.c'

submits = {}


def main():
  parser = argparse.ArgumentParser(
      prog="plag4nju4cprog", description="plagiarism detect from hustoj's logfile, multi-process")
  parser.add_argument('log', type=str, action="store",
                      help='log file u want to cut')
  parser.add_argument('-d', '--dir', type=str, default=None,
                      help='target directory u want to place the cut files in. default to the same name as the log file')
  parser.add_argument('-s', '--suffix', type=str,
                      default=None, help='suffix you want to add. i have no idea what this will do.')
  parser.add_argument('-a', '--all', help='whether to include all pairs in result',
                      action='store_true', default=False)
  parser.add_argument("-o", "--old", default=False,
                      action='store_true', help="use old method for cpp code")
  parser.add_argument('-r', '--remove', action='store_true',
                      default=False, help='remove existing directory if set to true')
  parser.add_argument('-p', "--parallel", action="store_true",
                      default=False, help='turn on to parallel')
  parser.add_argument('-n', '--ntoks', type=int, default=100,
                      help='how many identical tokens will be recognized as copy. higher means more tolerant. default to 100')
  parser.add_argument('-j', '--jar_path', type=str,
                      default='./jplag.jar', help='where jplag jar is. u need to manage java environment yourself. default to "./jplag.jar"')
  args = parser.parse_args()
  logfile = args.log
  directory = args.dir
  include_all = args.all
  if args.suffix:
    global suffix
    suffix = args.suffix
  if not directory:
    directory = Path(logfile).stem
  cut_file(logfile, directory, args.remove)
  result_dir = Path(directory) / f'results-{args.ntoks}toks'
  if os.path.exists(result_dir):
    shutil.rmtree(result_dir)
  os.mkdir(result_dir)
  batch_detect(directory=directory, use_cpp2=not args.old, parallel=args.parallel,
               include_all=include_all, ntoks=args.ntoks, result_dir=result_dir, jar_path=args.jar_path)


def batch_detect(directory: str, use_cpp2: bool, parallel: bool, include_all: bool, ntoks: int, result_dir: Path, jar_path):
  pids = []
  for sub in Path(directory).iterdir():
    if sub and sub.is_dir():
      pid = subprocess.Popen(['java', '-jar', jar_path, '-t', str(ntoks),
                             '-l', 'cpp2' if use_cpp2 else 'cpp', sub.absolute(), "-r", result_dir / sub.stem, '-n', '-1' if include_all else '100'])
      pids.append(pid)
      if not parallel:
        subprocess.Popen.wait(pid)
  if parallel:
    for pid in pids:
      subprocess.Popen.wait(pid)


def cut_file(logfile: str, directory: str, remove: bool):
  cur_state = CUT_STATE.NOT_GET
  cur_name = ''
  cur_problem = 114514
  cur_file = []
  with open(logfile, 'r', encoding='utf8') as f:
    for line in f:
      if cur_state == CUT_STATE.NOT_GET:
        tokens = line.split(':')
        assert len(tokens) == 3, 'should be xx:xx:xx'
        name = tokens[0]
        problem = tokens[1]
        assert problem.startswith("Problem"), "i cant handle otherwise"
        cur_problem = int(problem[len("Problem"):])
        if not submits.get(cur_problem):
          submits[cur_problem] = {}
        cur_name = name
        state = tokens[-1]
        if state in AC:
          cur_state = CUT_STATE.GETTING
        else:
          cur_state = CUT_STATE.BAD
      elif cur_state == CUT_STATE.BAD:
        if line == END_DASH:
          cur_state = CUT_STATE.NOT_GET
      elif cur_state == CUT_STATE.GETTING:
        if line == END_DASH:
          cur_state = CUT_STATE.NOT_GET
          submits[cur_problem][cur_name] = cur_file[:]
          cur_file.clear()
        else:
          cur_file.append(line)
      else:
        assert False
  noneed = os.path.exists(directory)
  if noneed and remove:
    shutil.rmtree(directory)
    noneed = False
  if not noneed:
    os.mkdir(directory)
    for p in submits.keys():
      os.mkdir(Path(directory) / str(p))
    for pid, submit in submits.items():
      for name, lines in submit.items():
        with open(Path(os.path.curdir) / directory / str(pid) / (name + suffix), "w", encoding='utf8') as f:
          f.writelines(lines)


if __name__ == '__main__':
  main()
