from data.filesystem import FileSystemNode
import json
import sys
from typing import Optional
from time import strftime, localtime
import operator


class TreeNode:
    def __init__(self, name: str, size: int, time_modified: int, permissions: str):
        self.data = FileSystemNode(name, size, time_modified, permissions)
        self.children: dict[str, TreeNode] = {}

    def __str__(self) -> str:
        return self.data.name

    def add_child(self, name: str, child) -> None:
        self.children[name] = child


class FileSystemTree:
    def __init__(self, json_path):
        self.root = self.build_tree_from_json(json_path)

    def build_tree_from_json(self, json_path: str) -> Optional[TreeNode]:
        queue: list[tuple[dict, TreeNode]] = []
        json_data = self.load_json_from_file(json_path=json_path)
        if not json_data:
            return None
        root = TreeNode(name=json_data["name"], size=json_data["size"],
                        permissions=json_data["permissions"], time_modified=json_data["time_modified"])
        self.enqueue(queue=queue, data=json_data, parent=root)
        while len(queue) > 0:
            current_data = queue.pop(0)
            node_data = current_data[0]
            parent_node = current_data[1]
            current_node = TreeNode(name=node_data["name"], size=node_data["size"],
                                    permissions=node_data["permissions"], time_modified=node_data["time_modified"])
            parent_node.add_child(node_data["name"], current_node)
            if "contents" in node_data:
                self.enqueue(queue=queue, data=node_data, parent=current_node)
        return root

    @staticmethod
    def load_json_from_file(json_path: str) -> dict:
        json_data = {}
        try:
            with open(json_path, encoding="UTF-8") as json_file:
                json_data = json.load(json_file)
            if "size" not in json_data or "time_modified" not in json_data or "name" not in json_data or "permissions" not in json_data:
                raise ValueError
        except ValueError:
            print("The provided json filesystem is invalid", file=sys.stderr)
        return json_data

    def enqueue(self, queue: list[tuple[dict, TreeNode]], data: dict, parent: TreeNode) -> None:
        for child_data in data["contents"]:
            queue.append((child_data, parent))

    def print_children(self, show_all=False, long_listing=False, reverse_sorting=False, sort_by_time=False) -> None:
        if self.root is None:
            return

        sorted_children = list(self.root.children.values())
        sort_key = "data.time_modified" if sort_by_time else "data.name"

        sorted_children.sort(
            key=operator.attrgetter(sort_key), reverse=reverse_sorting)

        strings_to_print: list[str] = []
        for child in sorted_children:
            if (not show_all and not child.data.name.startswith(".")) or show_all:
                if long_listing:
                    formatted_time = strftime(
                        "%b %d %H:%M", localtime(child.data.time_modified))
                    strings_to_print.append(
                        f"{child.data.permissions} {child.data.size:>4} {formatted_time} {child.data.name}")
                else:
                    strings_to_print.append(child.data.name)
        join_operator = "\n" if long_listing else " "
        print(join_operator.join(strings_to_print))
