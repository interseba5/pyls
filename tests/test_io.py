"""Test suite for the pyls.utils.io module"""

from pyls.utils.io import load_json_from_file
from tests.utils import mock_object


def test_load_file(mocker):
    "Test load_json_from_file"
    mock_open = mocker.mock_open(read_data='{}')
    mocker.patch("builtins.open", mock_open)
    mocker.patch("json.load", return_value=mock_object)
    actual_ret = load_json_from_file("test")
    assert actual_ret == mock_object


def test_load_invalid_object(capfd, mocker):
    "Test load_json_from_file"
    mock_open = mocker.mock_open(read_data='{}')
    mocker.patch("builtins.open", mock_open)
    mocker.patch("json.load", return_value={"key": "value"})
    actual_ret = load_json_from_file("test")
    _, err = capfd.readouterr()
    assert err == "The provided json filesystem is invalid\n"
    assert actual_ret == {}


def test_load_invalid_file(capfd, mocker):
    "Test load_json_from_file with an invalid file"
    mock_open = mocker.mock_open(read_data='{}')
    mocker.patch("builtins.open", mock_open)
    mocker.patch("json.load", side_effect=ValueError)
    actual_ret = load_json_from_file("test")
    _, err = capfd.readouterr()
    assert err == "The provided json filesystem is invalid\n"
    assert actual_ret == {}


def test_load_not_existing_file(capfd, mocker):
    "Test load_json_from_file with a not existing file"
    mock_open = mocker.mock_open(read_data='{}')
    mocker.patch("builtins.open", mock_open)
    mocker.patch("json.load", side_effect=FileNotFoundError)
    actual_ret = load_json_from_file("test")
    _, err = capfd.readouterr()
    assert err == "There is no test file\n"
    assert actual_ret == {}
