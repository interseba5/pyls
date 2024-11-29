from time import strftime, localtime


class FileSystemNode:
    def __init__(self, name: str, size: int, time_modified: int, permissions: str):
        self.name = name
        self.size = size
        self.time_modified = strftime(
            '%Y-%m-%d %H:%M:%S', localtime(time_modified))
        self.permissions = permissions
