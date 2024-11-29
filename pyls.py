from data.tree import build_tree_from_json, print_children

root = build_tree_from_json(".\\test\\utils\\filesystem.json")

print_children(root)
