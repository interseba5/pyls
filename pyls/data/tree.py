"""Module that contains all the class and method
related to the tree structure of the filesystem"""

import operator
import sys
from time import localtime, strftime
from typing import Optional

import pyls.utils.io as pylsio
from pyls.data.filesystem import FileSystemNode, FileSystemNodeType
from pyls.utils.formatters import humanize_size


class TreeNode:
    """A class used to represent a node of the filesystem tree

    Attributes
    ----------
    data : FileSystemNode
        the file or directory data attached to the node
    children : dict[str, TreeNode] | None
        dictionary name -> node of the node children if any.
        This value is None for the leaf
    """

    def __init__(self, name: str, size: int, time_modified: int,
                 permissions: str, node_type: FileSystemNodeType):
        """
        Parameters
        ----------
        name: str
            the name of the file/directory
        size: int
            the file/directory size
        time_modified: int
            unix epoch of the file/directory last modified time
        permissions: str
            string that represents the permissions
            attached to the file/directory
        """
        self.data = FileSystemNode(
            name=name, size=size, time_modified=time_modified,
            permissions=permissions, node_type=node_type)
        self.children: Optional[dict[str, TreeNode]] = None

    def __str__(self) -> str:
        return self.data.name

    def add_child(self, name: str, child) -> None:
        """Add a child to the node.

        Parameters
        ----------
        name: str
            the name of the file/directory
        child: TreeNode
            the child to add
        """
        if self.children is None:
            self.children = {}
        self.children[name] = child


class FileSystemTree:
    """A class used to represent the filesystem tree

    Attributes
    ----------
    root : TreeNode | None
        the root node of the tree
    current_node : TreeNode | None
        the current node in the tree.
        Used to allow the path traversal in the tree
    """

    def __init__(self, json_path):
        """Build the filesystem tree from a json file.
        The current_node is initialized as the root

        Parameters
        ----------
        json_path: str
            the path of the json file
        """
        self.root: Optional[TreeNode] = None
        self.build_tree_from_json(json_path)
        self.current_node = self.root

    def build_tree_from_json(self, json_path: str) -> None:
        """Build the filesystem tree from a json file.

        Parameters
        ----------
        json_path: str
            the path of the json file
        """
        queue: list[tuple[dict, TreeNode]] = []
        json_data = pylsio.load_json_from_file(json_path=json_path)
        if json_data:
            root = TreeNode(name=json_data["name"], size=json_data["size"],
                            permissions=json_data["permissions"],
                            time_modified=json_data["time_modified"],
                            node_type=FileSystemNodeType.DIRECTORY)
            FileSystemTree.enqueue(queue=queue, data=json_data, parent=root)
            while len(queue) > 0:
                current_data = queue.pop(0)
                node_data = current_data[0]
                parent_node = current_data[1]
                node_type = (FileSystemNodeType.DIRECTORY
                             if "contents" in node_data else
                             FileSystemNodeType.FILE)
                try:
                    current_node = TreeNode(
                        name=node_data["name"],
                        size=node_data["size"],
                        permissions=node_data["permissions"],
                        time_modified=node_data["time_modified"],
                        node_type=node_type)
                except KeyError:
                    print(
                        "There is some invalid data in your json file. "
                        "Ignoring it.",
                        file=sys.stderr)
                    continue
                parent_node.add_child(node_data["name"], current_node)
                if node_type == FileSystemNodeType.DIRECTORY:
                    FileSystemTree.enqueue(queue=queue, data=node_data,
                                           parent=current_node)
            self.root = root

    @staticmethod
    def enqueue(queue: list[tuple[dict, TreeNode]],
                data: dict, parent: TreeNode) -> None:
        """Static method that insert a tuple (dict, TreeNode) in a list

        Parameters
        ----------
        queue: list[tuple[dict, TreeNode]]
            list into enqueue
        data: dict
            first element of the tuple to enqueue.
            Represent the data that will be used to build the child
        parent: TreeNode
            second element of the tuple to enqueue.
            Represent the parent node of the child that will be built
        """
        for child_data in data["contents"]:
            queue.append((child_data, parent))

    @staticmethod
    def filter_children(
            filter_by: str, children: list[TreeNode]) -> list[TreeNode]:
        """Filter a list of TreeNode.
        The result will be a list with only file nodes or directory nodes

        Parameters
        ----------
        filter_by: str
            filter key. file to get only file nodes, dir
            to get only directory nodes
        children: list[TreeNode]
            list to filter

        Returns
        ----------
        filtered_children: list[TreeNode]
            list of filtered TreeNode
        """
        filtered_children = children
        if filter_by in ("file", "dir"):
            filter_by_enum = (FileSystemNodeType.FILE if filter_by == "file"
                              else FileSystemNodeType.DIRECTORY)
            filtered_children = [
                child for child in children
                if child.data.node_type == filter_by_enum]
        return filtered_children

    @staticmethod
    def sort_children(
            children: list[TreeNode],
            sort_by: str, reverse: bool) -> None:
        """Inplace sort the children parameter.

        Parameters
        ----------
        children : list[TreeNode]
            The list that will be sorted
        sort_by : str
            The attribute of the TreeNode class used to sort the list
        reverse : bool
            Wheter the sorting must be in descending or ascending order.
            True for descending
        """
        children.sort(key=operator.attrgetter(sort_by), reverse=reverse)

    def change_directory(self, path: Optional[str]) -> bool:
        """Change the current_node navigating the provided path

        Parameters
        ----------
        path: str | None
            The path to navigate

        Returns
        ----------
        result: bool
            True if the path is valid, False otherwise
        """
        fixed_path = path.replace("./", "") if path else path
        current_node = self.root
        if fixed_path and fixed_path != ".":
            splitted_path = filter(None, fixed_path.split("/"))
            for component in splitted_path:
                if component in current_node.children:
                    current_node = current_node.children[component]
                else:
                    return False
        self.current_node = current_node
        return True

    def print_children(self, show_all=False, long_listing=False,
                       reverse_sorting=False, sort_by_time=False,
                       filter_by: Optional[str] = None,
                       humanize=False) -> None:
        """Print the children of the curren_node

        Parameters
        ----------
        path: str | None
            The path to navigate
        """
        if self.root is None:
            return

        if self.current_node.children is None:
            children_list = [self.current_node]
        else:
            children_list = list(self.current_node.children.values())

        filtered_children = FileSystemTree.filter_children(
            filter_by, children_list)

        sort_key = "data.time_modified" if sort_by_time else "data.name"
        FileSystemTree.sort_children(children=filtered_children,
                                     sort_by=sort_key, reverse=reverse_sorting)

        strings_to_print: list[str] = []
        if humanize:
            size_max_length = max(
                map(lambda x: len(humanize_size(x.data.size)), filtered_children))
        else:
            size_max_length = len(
                str(max(filtered_children, key=operator.attrgetter("data.size")).data.size))

        for child in filtered_children:
            if (not show_all and not child.data.name.startswith(".")) or show_all:
                if long_listing:
                    formatted_time = strftime(
                        "%b %d %H:%M", localtime(child.data.time_modified))
                    formatted_size = humanize_size(
                        child.data.size) if humanize else child.data.size
                    strings_to_print.append(
                        f"{child.data.permissions} "
                        f"{formatted_size:>{size_max_length}} "
                        f"{formatted_time} {child.data.name}")
                else:
                    strings_to_print.append(child.data.name)
        join_operator = "\n" if long_listing else " "
        print(join_operator.join(strings_to_print))
