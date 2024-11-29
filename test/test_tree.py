from data.tree import print_children, build_tree_from_json

root = build_tree_from_json(".\\test\\utils\\filesystem.json")


def test_ls(capfd):
    print_children(
        root)
    out, _ = capfd.readouterr()
    assert out == "LICENSE README.md ast go.mod lexer main.go parser token\n"
