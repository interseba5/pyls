"""Command line interface for the pyls package"""

import argparse
import os

from pyls.data.tree import FileSystemTree

parser = argparse.ArgumentParser(
    prog="pyls", description="list directory contents", add_help=False,
    epilog="\n\nAUTHOR\n\tWritten by Sebastiano Manfredini",
    formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-A", action="store_true",
                    help="do not ignore entries starting with .")
parser.add_argument("-l", action="store_true",
                    help="use a long listing format")
parser.add_argument("-r", action="store_true",
                    help="reverse order while sorting")
parser.add_argument("-t", action="store_true",
                    help="sort by time, oldest first")
parser.add_argument(
    "--filter", choices=['file', 'dir'],
    help="filter the output based on given option. "
    "Use 'file' to print only files. Use 'dir' to print only directories")

parser.add_argument(
    "-h", action="store_true",
    help="with -l, show human readable size like 1K 234M 2G etc.")
parser.add_argument('--help', action='help',
                    help='display this help and exit')
parser.add_argument('directory', nargs='?')


def main():
    """Function executed at startup"""
    args = parser.parse_args()
    tree = FileSystemTree(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "structure.json"))
    if tree.root:
        if not tree.change_directory(args.directory):
            print(
                f"error: cannot access '{args.directory}': "
                "No such file or directory")
        else:
            tree.print_children(
                show_all=args.A, long_listing=args.l, reverse_sorting=args.r,
                sort_by_time=args.t, filter_by=args.filter, humanize=args.h)


if __name__ == "__main__":
    main()
