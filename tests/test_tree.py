from tests.utils import mock_filesystem, long_listing_result, long_listing_result_all
from data.tree import FileSystemTree
import pytest


@pytest.fixture(name="tree")
def fixture_tree(mocker):
    mocker.patch.object(FileSystemTree, "load_json_from_file",
                        return_value=mock_filesystem)
    return FileSystemTree("mock")


def test_empty_tree(capfd, mocker):
    mock_open = mocker.mock_open(read_data='{}')
    mocker.patch("builtins.open", mock_open)
    mocker.patch("json.load", return_value={})
    actual_ret = FileSystemTree.load_json_from_file("test")
    _, err = capfd.readouterr()
    assert err == "The provided json filesystem is invalid\n"
    assert actual_ret == {}


def test_ls(capfd, tree):
    tree.print_children(show_all=False, long_listing=False)
    out, _ = capfd.readouterr()
    assert out == "LICENSE README.md ast go.mod lexer main.go parser token\n"


def test_ls_all(capfd, tree):
    tree.print_children(show_all=True, long_listing=False)
    out, _ = capfd.readouterr()
    assert out == ".gitignore LICENSE README.md ast go.mod lexer main.go parser token\n"


def test_ls_long_listing_all(capfd, tree):
    tree.print_children(show_all=True, long_listing=True)
    out, _ = capfd.readouterr()
    assert out == long_listing_result_all
