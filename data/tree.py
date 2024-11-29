from data.filesystem import FileSystemNode
import json


class TreeNode:
    def __init__(self, name: str, size: int, time_modified: int, permissions: str):
        self.data = FileSystemNode(name, size, time_modified, permissions)
        self.children: dict[str, TreeNode] = {}

    def __str__(self) -> str:
        return self.data.name

    def add_child(self, name: str, child) -> None:
        self.children[name] = child


def build_tree_from_json(json_path: str) -> TreeNode:
    queue: list[tuple[dict, TreeNode]] = []
    json_data = {}
    with open(json_path, encoding="UTF-8") as json_file:
        json_data = json.load(json_file)
    root = TreeNode(name=json_data["name"], size=json_data["size"],
                    permissions=json_data["permissions"], time_modified=json_data["time_modified"])
    enqueue(queue=queue, data=json_data, parent=root)
    while len(queue) > 0:
        current_data = queue.pop(0)
        node_data = current_data[0]
        parent_node = current_data[1]
        current_node = TreeNode(name=node_data["name"], size=node_data["size"],
                                permissions=node_data["permissions"], time_modified=node_data["time_modified"])
        parent_node.add_child(node_data["name"], current_node)
        if "contents" in node_data:
            enqueue(queue=queue, data=node_data, parent=current_node)
    return root


def enqueue(queue: list[tuple[dict, TreeNode]], data: dict, parent: TreeNode) -> None:
    for child_data in data["contents"]:
        queue.append((child_data, parent))
