from tests.utils import *
from pyls.data.tree import FileSystemTree
import pytest


@pytest.fixture(name="tree")
def fixture_tree(mocker):
    mocker.patch.object(FileSystemTree, "load_json_from_file",
                        return_value=mock_filesystem)
    tree = FileSystemTree("mock")
    tree.change_directory("")
    return tree


def test_empty_tree(capfd, mocker):
    mock_open = mocker.mock_open(read_data='{}')
    mocker.patch("builtins.open", mock_open)
    mocker.patch("json.load", return_value={})
    actual_ret = FileSystemTree.load_json_from_file("test")
    _, err = capfd.readouterr()
    assert err == "The provided json filesystem is invalid\n"
    assert actual_ret == {}


def test_ls(capfd, tree):
    tree.print_children()
    out, _ = capfd.readouterr()
    assert out == "LICENSE README.md ast go.mod lexer main.go parser token\n"


def test_ls_all(capfd, tree):
    tree.print_children(show_all=True)
    out, _ = capfd.readouterr()
    assert out == ".gitignore LICENSE README.md ast go.mod lexer main.go parser token\n"


def test_ls_long_listing_all(capfd, tree):
    tree.print_children(show_all=True, long_listing=True)
    out, _ = capfd.readouterr()
    assert out == long_listing_result_all


def test_ls_long_listing(capfd, tree):
    tree.print_children(long_listing=True)
    out, _ = capfd.readouterr()
    assert out == long_listing_result


def test_ls_long_listing_reversed(capfd, tree):
    tree.print_children(long_listing=True, reverse_sorting=True)
    out, _ = capfd.readouterr()
    assert out == long_listing_result_reversed


def test_ls_long_listing_reversed_all(capfd, tree):
    tree.print_children(show_all=True, long_listing=True, reverse_sorting=True)
    out, _ = capfd.readouterr()
    assert out == long_listing_result_reversed_all


def test_ls_reversed(capfd, tree):
    tree.print_children(reverse_sorting=True)
    out, _ = capfd.readouterr()
    assert out == "token parser main.go lexer go.mod ast README.md LICENSE\n"


def test_ls_all_reversed(capfd, tree):
    tree.print_children(show_all=True, reverse_sorting=True)
    out, _ = capfd.readouterr()
    assert out == "token parser main.go lexer go.mod ast README.md LICENSE .gitignore\n"


def test_long_listing_sort_by_time(capfd, tree):
    tree.print_children(long_listing=True, sort_by_time=True)
    out, _ = capfd.readouterr()
    assert out == ll_sort_by_time_ascending


def test_long_listing_sort_by_time_reverse(capfd, tree):
    tree.print_children(long_listing=True,
                        reverse_sorting=True, sort_by_time=True)
    out, _ = capfd.readouterr()
    assert out == ll_sort_by_time_descending


def test_ls_sort_by_time(capfd, tree):
    tree.print_children(sort_by_time=True)
    out, _ = capfd.readouterr()
    assert out == "LICENSE README.md go.mod main.go token lexer ast parser\n"


def test_ls_sort_by_time_reverse(capfd, tree):
    tree.print_children(reverse_sorting=True, sort_by_time=True)
    out, _ = capfd.readouterr()
    assert out == "parser ast lexer token main.go go.mod LICENSE README.md\n"


def test_long_listing_sort_by_time_reverse_only_file(capfd, tree):
    tree.print_children(long_listing=True,
                        reverse_sorting=True, sort_by_time=True, filter_by="file")
    out, _ = capfd.readouterr()
    assert out == ll_sort_by_time_reverse_only_file


def test_long_listing_sort_by_time_reverse_only_dir(capfd, tree):
    tree.print_children(long_listing=True,
                        reverse_sorting=True, sort_by_time=True, filter_by="dir")
    out, _ = capfd.readouterr()
    assert out == ll_sort_by_time_reverse_only_dir
