from data.tree import FileSystemTree
import argparse

parser = argparse.ArgumentParser(prog="pyls",
                                 description="list directory contents",
                                 epilog="\n\nAUTHOR\n\tWritten by Sebastiano Manfredini", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-A", action="store_true",
                    help="do not ignore entries starting with .")
parser.add_argument("-l", action="store_true",
                    help="use a long listing format")
parser.add_argument("-r", action="store_true",
                    help="reverse order while sorting")
parser.add_argument("-t", action="store_true",
                    help="sort by time, oldest first")
parser.add_argument("--filter", choices=['file', 'dir'],
                    help="filter the output based on given option. Use <file> to print only files. Use <dir> to print only directories")

args = parser.parse_args()
tree = FileSystemTree(".\\structure.json")
if tree is not None:
    tree.print_children(show_all=args.A, long_listing=args.l,
                        reverse_sorting=args.r, sort_by_time=args.t, filter_by=args.filter)
