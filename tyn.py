#!/usr/bin/env python

import argparse
from datetime import datetime
from glob import glob
import os
import sys


def lsfigs(args):
    """list figures in folder"""

    fig_fmt = '![{description}](./{path}/{base})'
    file_fmt = '[{description}](./{path}/{base})'

    if len(args) == 0:
        datestr = datetime.now().strftime('%Y%m%d')
        folder = '~/Projects/wiki/log/{}'.format(datestr)
        folder = os.path.expanduser(folder)
    elif len(args) == 1:
        folder, = args
    else:
        raise Exception('Too much input arguments')

    path = os.path.abspath(folder)
    _, path = os.path.split(path)

    if os.path.exists(folder):
        items = os.listdir(folder)
        for item in sorted(items):
            filename = os.path.join(folder, item)
            if os.path.isfile(filename):
                d = {}
                d['path'] = path
                d['base'] = base = os.path.basename(filename)
                d['description'], ext = os.path.splitext(base)
                if ext in ['png', 'jpg', 'jpeg', 'pdf']:
                    fmt = fig_fmt
                else:
                    fmt = file_fmt
                print(fmt.format(**d))


def main():
    """main"""

    parser = argparse.ArgumentParser(prog='tyn')
    parser.add_argument('command', help='command')
    parser.add_argument('args', nargs='*', help='arg0')
    args = parser.parse_args()

    command = args.command
    if command == 'lsfigs':
        lsfigs(args.args)
    else:
        raise Exception('Unknown command')


if __name__ == '__main__':
    sys.exit(main())
