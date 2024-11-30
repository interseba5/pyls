class FileSystemNode:
    def __init__(self, name: str, size: int, time_modified: int, permissions: str):
        self.name = name
        self.size = size
        self.time_modified = time_modified
        self.permissions = permissions
