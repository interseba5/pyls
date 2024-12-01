"""Test suite for the pyls.data.tree module"""

import pytest

import tests.utils as ut
from pyls.data.filesystem import FileSystemNodeType
from pyls.data.tree import FileSystemTree


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


def test_ls(capfd, tree):
    """Test the print_children ignoring dotted file
    and with the short format"""
    tree.print_children()
    out, _ = capfd.readouterr()
    assert out == "LICENSE README.md ast go.mod lexer main.go parser token\n"


def test_ls_all(capfd, tree):
    """Test print_children showing all files (-A)"""
    tree.print_children(show_all=True)
    out, _ = capfd.readouterr()
    assert out == ".gitignore LICENSE README.md ast go.mod lexer main.go parser token\n"


def test_ls_long_listing_all(capfd, tree):
    """Test print_children showing all files (-A)
    and with the long listing format (-l)"""
    tree.print_children(show_all=True, long_listing=True)
    out, _ = capfd.readouterr()
    assert out == ut.long_listing_result_all


def test_ls_long_listing(capfd, tree):
    """Test print_children with the long listing format (-l)
    ignoring dotted file"""
    tree.print_children(long_listing=True)
    out, _ = capfd.readouterr()
    assert out == ut.long_listing_result


def test_ls_long_listing_reversed(capfd, tree):
    """Test print_children with the long listing format (-l)
    ignoring dotted file, in reverse order"""
    tree.print_children(long_listing=True, reverse_sorting=True)
    out, _ = capfd.readouterr()
    assert out == ut.long_listing_result_reversed


def test_ls_long_listing_reversed_all(capfd, tree):
    """Test print_children showing all files (-A)
    and with the long listing format (-l), in reverse order"""
    tree.print_children(show_all=True, long_listing=True, reverse_sorting=True)
    out, _ = capfd.readouterr()
    assert out == ut.long_listing_result_reversed_all


def test_ls_reversed(capfd, tree):
    """Test the print_children ignoring dotted file
    and with the short format, in reverse order"""
    tree.print_children(reverse_sorting=True)
    out, _ = capfd.readouterr()
    assert out == "token parser main.go lexer go.mod ast README.md LICENSE\n"


def test_ls_all_reversed(capfd, tree):
    """Test print_children showing all files (-A), in reverse order"""
    tree.print_children(show_all=True, reverse_sorting=True)
    out, _ = capfd.readouterr()
    assert out == "token parser main.go lexer go.mod ast README.md LICENSE .gitignore\n"


def test_long_listing_sort_by_time(capfd, tree):
    """Test print_children with the long listing format (-l)
    ignoring dotted file with the values sorted by time"""
    tree.print_children(long_listing=True, sort_by_time=True)
    out, _ = capfd.readouterr()
    assert out == ut.ll_sort_by_time_ascending


def test_long_listing_sort_by_time_reverse(capfd, tree):
    """Test print_children with the long listing format (-l)
    ignoring dotted file with the values sorted by time, in reverse order"""
    tree.print_children(long_listing=True,
                        reverse_sorting=True, sort_by_time=True)
    out, _ = capfd.readouterr()
    assert out == ut.ll_sort_by_time_descending


def test_ls_sort_by_time(capfd, tree):
    """Test the print_children ignoring dotted file
    and with the short format with the values sorted by time"""
    tree.print_children(sort_by_time=True)
    out, _ = capfd.readouterr()
    assert out == "LICENSE README.md go.mod main.go token lexer ast parser\n"


def test_ls_sort_by_time_reverse(capfd, tree):
    """Test the print_children ignoring dotted file
    and with the short format with the values sorted by time,
    in reverse order"""
    tree.print_children(reverse_sorting=True, sort_by_time=True)
    out, _ = capfd.readouterr()
    assert out == "parser ast lexer token main.go go.mod LICENSE README.md\n"


def test_long_listing_sort_by_time_reverse_only_file(capfd, tree):
    """Test print_children with the long listing format (-l)
    ignoring dotted file with the values sorted by timeand in reverse order.
    Furthermore, the values are filtered by file"""
    tree.print_children(
        long_listing=True, reverse_sorting=True, sort_by_time=True,
        filter_by="file")
    out, _ = capfd.readouterr()
    assert out == ut.ll_sort_by_time_reverse_only_file


def test_long_listing_sort_by_time_reverse_only_dir(capfd, tree):
    """Test print_children with the long listing format (-l)
    ignoring dotted file with the values sorted by time and in reverse order.
    Furthermore, the values are filtered by dir"""
    tree.print_children(
        long_listing=True, reverse_sorting=True, sort_by_time=True,
        filter_by="dir")
    out, _ = capfd.readouterr()
    assert out == ut.ll_sort_by_time_reverse_only_dir


def test_change_directory_file(tree_nocd):
    """Test change_directory with a file path"""
    tree_nocd.change_directory("parser/parser.go")
    assert tree_nocd.current_node.data.name == "parser.go"
    assert tree_nocd.current_node.data.permissions == "-rw-r--r--"
    assert tree_nocd.current_node.data.size == 1622
    assert tree_nocd.current_node.data.time_modified == 1700202950


def test_change_directory_file_with_dot(tree_nocd):
    """Test change_directory with a file path with leading ./ sequence"""
    tree_nocd.change_directory("./parser/parser.go")
    assert tree_nocd.current_node.data.name == "parser.go"
    assert tree_nocd.current_node.data.permissions == "-rw-r--r--"
    assert tree_nocd.current_node.data.size == 1622
    assert tree_nocd.current_node.data.time_modified == 1700202950


def test_change_directory_file_with_middle_dot(tree_nocd):
    """Test change_directory with a file path with at the start
    and in the middle the ./ sequence"""
    tree_nocd.change_directory("./parser/./parser.go")
    assert tree_nocd.current_node.data.name == "parser.go"
    assert tree_nocd.current_node.data.permissions == "-rw-r--r--"
    assert tree_nocd.current_node.data.size == 1622
    assert tree_nocd.current_node.data.time_modified == 1700202950


def test_change_directory_directory(tree_nocd):
    """Test change_directory with a directory path"""
    tree_nocd.change_directory("parser")
    assert tree_nocd.current_node.data.name == "parser"
    assert tree_nocd.current_node.data.permissions == "drwxr-xr-x"
    assert tree_nocd.current_node.data.size == 4096
    assert tree_nocd.current_node.data.time_modified == 1700205662


def test_change_directory_directory_with_dot(tree_nocd):
    """Test change_directory with a directory path with leading ./ sequence"""
    tree_nocd.change_directory("./token")
    assert tree_nocd.current_node.data.name == "token"
    assert tree_nocd.current_node.data.permissions == "drwxr-xr-x"
    assert tree_nocd.current_node.data.size == 4096
    assert tree_nocd.current_node.data.time_modified == 1699954070


def test_change_directory_directory_with_trailing_slash(tree_nocd):
    """Test change_directory with a directory path with leading ./ sequence
    and a trailing slash"""
    tree_nocd.change_directory("./token/")
    assert tree_nocd.current_node.data.name == "token"
    assert tree_nocd.current_node.data.permissions == "drwxr-xr-x"
    assert tree_nocd.current_node.data.size == 4096
    assert tree_nocd.current_node.data.time_modified == 1699954070


def test_change_directory_file_with_trailing_slash(tree_nocd):
    """Test change_directory with a file  path with a trailing slash
    Must return False"""
    result = tree_nocd.change_directory("parser/parser.go/")
    assert not result


def test_change_directory_invalidfile(tree_nocd):
    """Test change_directory with a file path"""
    result = tree_nocd.change_directory("test")
    assert not result


def test_build_tree_from_json_invalid_data(capfd, mocker):
    """Test build_tree_from_json with a children with invalid data"""
    mocker.patch("pyls.utils.io.load_json_from_file",
                 return_value=ut.mock_invalid_object)
    tree = FileSystemTree("mock")
    _, err = capfd.readouterr()
    assert len(tree.root.children) == 1
    assert err == "There is some invalid data in your json file. Ignoring it.\n"


def test_build_tree_from_json(mocker):
    """Test build_tree_from_json with a file, a dir and an empty dir"""
    mocker.patch("pyls.utils.io.load_json_from_file",
                 return_value=ut.mock_valid_object)
    tree = FileSystemTree("mock")
    assert len(tree.root.children) == 3
    assert tree.root.data.node_type == FileSystemNodeType.DIRECTORY
    emptydir = tree.root.children["testemptydir"]
    file = tree.root.children["testfile"]
    testdir = tree.root.children["testdir"]
    assert emptydir.data.name == "testemptydir"
    assert emptydir.data.node_type == FileSystemNodeType.DIRECTORY
    assert file.data.name == "testfile"
    assert file.data.node_type == FileSystemNodeType.FILE
    assert testdir.data.name == "testdir"
    assert testdir.data.node_type == FileSystemNodeType.DIRECTORY
    assert len(testdir.children) == 1
    testnesteddir = testdir.children["testnesteddir"]
    assert len(testnesteddir.children) == 1
    assert testnesteddir.data.node_type == FileSystemNodeType.DIRECTORY
    testnestedfile = testnesteddir.children["testnestedfile"]
    assert testnestedfile.data.node_type == FileSystemNodeType.FILE
