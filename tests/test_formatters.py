"""Test suite for the pyls.utils.formatters module"""

from pyls.utils.formatters import humanize_size


def test_humanize_size_zero():
    """Test the humanization of size 0"""
    assert humanize_size(0) == "0"


def test_humanize_size_byte():
    """Test the humanization of byte size"""
    assert humanize_size(533) == "533"


def test_humanize_size_kilobyte():
    """Test the humanization of kilobyte size"""
    assert humanize_size(1622) == "1.6K"
    assert humanize_size(1342) == "1.4K"
    assert humanize_size(2040) == "2.0K"
    assert humanize_size(20400) == "20K"


def test_humanize_size_megabyte():
    """Test the humanization of megabyte size"""
    assert humanize_size(2890251) == "2.8M"
    assert humanize_size(13783228) == "14M"
    assert humanize_size(137832280) == "132M"


def test_humanize_size_gigabyte():
    """Test the humanization of gigabyte size"""
    assert humanize_size(1378322800) == "1.3G"


def test_humanize_size_verybig():
    """Test the humanization of a very big size over the last allowed unit"""
    assert humanize_size(1378322800000000000000000) == "1195505E"
