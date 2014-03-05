#!/usr/bin/env python

import argparse
from datetime import datetime
import os
import sys

from tabulate import tabulate
from fabric.api import local

def parse_line(line, sep='|'):
    """ helper function for mdtable"""

    return [col.strip() for col in line.split(sep)[1:-1]]

def mdtable(args):
    """markdown pipe table outline"""

    if not len(args) == 1:
        raise Exception('Supply markdown table from command line')
    table_file, = args
    with open(table_file, 'r') as fh:
        lines = fh.readlines()

    headers = parse_line(lines[0])
    table = []
    for line in lines[2:]:
        table.append(parse_line(line))

    with open(table_file, 'w') as fh:
        fh.write(tabulate(table, headers=headers, tablefmt='pipe'))


def ddsk(args):
    """mount mac backup disk under ubuntu"""

    result = local('uname -n', capture=True)
    if not result == 'drum':
        raise Exception('This is not drum ...')

    local('sudo mount -t hfsplus -o force,rw /dev/sdb2 /mnt')
    local('sudo bindfs -u $(id -u) -g $(id -g) '
          '--create-for-user=501 --create-for-group=20 /mnt/Data ~/Data')

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
                if ext in ['.png', '.jpg', '.jpeg', '.pdf', '.svg']:
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
    elif command == 'ddsk':
        ddsk(args.args)
    elif command == 'mdtable':
        mdtable(args.args)
    else:
        raise Exception('Unknown command')


if __name__ == '__main__':
    sys.exit(main())

