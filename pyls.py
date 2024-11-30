from data.tree import FileSystemTree
import argparse

parser = argparse.ArgumentParser(prog='pyls',
                                 description='list directory contents')
parser.add_argument('-A', action='store_true',
                    help="do not ignore entries starting with .")

args = parser.parse_args()
tree = FileSystemTree(".\\filesystem.json")
if tree is not None:
    tree.print_children(show_all=args.A)
