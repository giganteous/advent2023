#! /usr/bin/env python3

import argparse, importlib, os, re
from typing import Any, Callable
from baseday import BaseDay

# Parse arguments
parser = argparse.ArgumentParser(
                    prog='runner',
                    description='runs the puzzles')
parser.add_argument('--day', type=int, nargs='+',
                    help='the day to run')
parser.add_argument('--part', type=int,
                    help='the part to run')
parser.add_argument('--example', action='store_true',
                    help='use example input')
parser.add_argument('--input',
                    help='input file to use')
parser.add_argument('--run', action='store_true', help='actually run the days')
args = parser.parse_args()

# Load modules.
days: list[tuple[int, Callable[[Any, Any], BaseDay]]] = []

for entry in sorted(os.listdir('.')):
    match = re.match(r"^(day(\d\d))-", entry)
    if match is not None:
        name = match.group(1)
        dayno = int(match.group(2))
        if args.day is None or dayno in args.day:
            mod = importlib.import_module(entry + '.' + name)
            days.append((dayno, getattr(mod, name.capitalize())))

# Run modules.
to_run = []
for i, day in days:
    to_run.append(day(args.input, args.example))
if args.run:
    [instance.run(i, args.part) for instance in to_run]
