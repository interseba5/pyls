"""Test suite for the pyls.data.tree module"""

import pytest

import tests.utils as ut
from pyls.data.tree import FileSystemTree
from pyls.utils.io import load_json_from_file


@pytest.fixture(name="tree")
def fixture_tree(mocker):
    """Fixture that build a tree using the tests.ut.mock_filesystem as structure.
    The current directory is the root directory

    Parameters
    ----------
    mocker 
        The mocker object provided by pytest-mock
    """
    mocker.patch("pyls.utils.io.load_json_from_file",
                 return_value=ut.mock_filesystem)
    tree = FileSystemTree("mock")
    tree.change_directory("")
    return tree


@pytest.fixture(name="tree_nocd")
def fixture_tree_nocd(mocker):
    """Fixture that build a tree using the tests.ut.mock_filesystem as structure.
    BE CAREFUL: this fixture does not call the tree.change_directory method

    Parameters
    ----------
    mocker 
        The mocker object provided by pytest-mock
    """
    mocker.patch("pyls.utils.io.load_json_from_file",
                 return_value=ut.mock_filesystem)
    tree = FileSystemTree("mock")
    return tree


def test_empty_tree(capfd, mocker):
    mock_open = mocker.mock_open(read_data='{}')
    mocker.patch("builtins.open", mock_open)
    mocker.patch("json.load", return_value={})
    actual_ret = load_json_from_file("test")
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
    assert out == ut.long_listing_result_all


def test_ls_long_listing(capfd, tree):
    tree.print_children(long_listing=True)
    out, _ = capfd.readouterr()
    assert out == ut.long_listing_result


def test_ls_long_listing_reversed(capfd, tree):
    tree.print_children(long_listing=True, reverse_sorting=True)
    out, _ = capfd.readouterr()
    assert out == ut.long_listing_result_reversed


def test_ls_long_listing_reversed_all(capfd, tree):
    tree.print_children(show_all=True, long_listing=True, reverse_sorting=True)
    out, _ = capfd.readouterr()
    assert out == ut.long_listing_result_reversed_all


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
    assert out == ut.ll_sort_by_time_ascending


def test_long_listing_sort_by_time_reverse(capfd, tree):
    tree.print_children(long_listing=True,
                        reverse_sorting=True, sort_by_time=True)
    out, _ = capfd.readouterr()
    assert out == ut.ll_sort_by_time_descending


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
    assert out == ut.ll_sort_by_time_reverse_only_file


def test_long_listing_sort_by_time_reverse_only_dir(capfd, tree):
    tree.print_children(long_listing=True,
                        reverse_sorting=True, sort_by_time=True, filter_by="dir")
    out, _ = capfd.readouterr()
    assert out == ut.ll_sort_by_time_reverse_only_dir


def test_change_directory_file(tree_nocd):
    tree_nocd.change_directory("parser/parser.go")
    assert tree_nocd.current_node.data.name == "parser.go"
    assert tree_nocd.current_node.data.permissions == "-rw-r--r--"
    assert tree_nocd.current_node.data.size == 1622
    assert tree_nocd.current_node.data.time_modified == 1700202950


def test_change_directory_file_with_dot(tree_nocd):
    tree_nocd.change_directory("./parser/parser.go")
    assert tree_nocd.current_node.data.name == "parser.go"
    assert tree_nocd.current_node.data.permissions == "-rw-r--r--"
    assert tree_nocd.current_node.data.size == 1622
    assert tree_nocd.current_node.data.time_modified == 1700202950


def test_change_directory_file_with_middle_dot(tree_nocd):
    tree_nocd.change_directory("./parser/./parser.go")
    assert tree_nocd.current_node.data.name == "parser.go"
    assert tree_nocd.current_node.data.permissions == "-rw-r--r--"
    assert tree_nocd.current_node.data.size == 1622
    assert tree_nocd.current_node.data.time_modified == 1700202950


def test_change_directory_directory(tree_nocd):
    tree_nocd.change_directory("parser")
    assert tree_nocd.current_node.data.name == "parser"
    assert tree_nocd.current_node.data.permissions == "drwxr-xr-x"
    assert tree_nocd.current_node.data.size == 4096
    assert tree_nocd.current_node.data.time_modified == 1700205662


def test_change_directory_directory_with_dot(tree_nocd):
    tree_nocd.change_directory("./token")
    assert tree_nocd.current_node.data.name == "token"
    assert tree_nocd.current_node.data.permissions == "drwxr-xr-x"
    assert tree_nocd.current_node.data.size == 4096
    assert tree_nocd.current_node.data.time_modified == 1699954070


def test_change_directory_directory_with_trailing_slash(tree_nocd):
    tree_nocd.change_directory("./token/")
    assert tree_nocd.current_node.data.name == "token"
    assert tree_nocd.current_node.data.permissions == "drwxr-xr-x"
    assert tree_nocd.current_node.data.size == 4096
    assert tree_nocd.current_node.data.time_modified == 1699954070
