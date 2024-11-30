"""Module containing all the classes and method related to the filesystem of pyls"""
from dataclasses import dataclass


@dataclass
class FileSystemNode:
    """A dataclass used to represent node of the pyls filesystem

    Attributes
    ----------
    name : str
        the file/directory name
    size: int
        the file/directory size
    time_modified: int
        the unix epoch of the file/directory last modification time
    permissions: str
        the permissions attached to the file/directory
    """
    name: str
    size: int
    time_modified: int
    permissions: str
