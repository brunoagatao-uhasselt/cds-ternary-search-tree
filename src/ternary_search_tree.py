from dataclasses import dataclass


@dataclass
class TreeNodeChildren:
    less_than: "TreeNode | None" = None
    equals: "TreeNode | None" = None
    larger_than: "TreeNode | None" = None


class TreeNode:
    def __init__(self, character: str):
        self.character = character
        self.terminates = False
        self.children = TreeNodeChildren()

    @property
    def character(self) -> str:
        return self._character

    @character.setter
    def character(self, character: str):
        if len(character) > 1:  # allow empty string
            raise ValueError("input must be a character string")
        self._character = character

    @property
    def terminates(self) -> bool:
        return self._terminates

    @terminates.setter
    def terminates(self, terminates: bool):
        self._terminates = terminates

    @property
    def children(self) -> TreeNodeChildren:
        return self._children

    @children.setter
    def children(self, children: TreeNodeChildren):
        self._children = children


class TernarySearchTree:
    def __init__(self, root: TreeNode | None = None) -> None:
        self.root = root

    @property
    def root(self) -> TreeNode | None:
        return self._root

    @root.setter
    def root(self, node: TreeNode | None):
        self._root = node
